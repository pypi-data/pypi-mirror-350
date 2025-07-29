import asyncio
import functools
import hashlib
import inspect
import sys
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])

# Sentinel value to distinguish between None and missing cache entries
_MISSING = object()


@dataclass
class CacheEntry:
    """Cache entry with value and metadata."""

    value: Any
    timestamp: float
    access_count: int = 0

    def is_expired(self, ttl: Optional[float]) -> bool:
        """Check if entry is expired based on TTL."""
        if ttl is None:
            return False
        return time.time() - self.timestamp > ttl


@dataclass
class CacheStats:
    """Cache statistics."""

    current_size: int
    max_size: int
    ttl: Optional[float]
    hits: int
    misses: int
    total_size_in_memory_bytes: int
    total_size_in_memory_pretty: str


class AsyncLRUCache:
    """Async LRU Cache implementation."""

    def __init__(self, maxsize: int = 1024, ttl: Optional[float] = None, ignore_params: Optional[List[str]] = None):
        self.maxsize = maxsize
        self.ttl = ttl
        self.ignore_params = set(ignore_params or [])
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self._lock = asyncio.Lock()
        # Track ongoing computations to prevent duplicate work
        self._pending: Dict[str, asyncio.Future] = {}

    def _get_cache_key(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function arguments, respecting ignore_params."""
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Filter out ignored parameters
        filtered_args = {name: value for name, value in bound_args.arguments.items() if name not in self.ignore_params}

        # Create a deterministic string representation
        key_data = f"{func.__module__}.{func.__qualname__}:{repr(sorted(filtered_args.items()))}"
        return hashlib.sha256(key_data.encode()).hexdigest()

    def _estimate_size(self, obj: Any) -> int:
        """Estimate memory size of an object."""
        try:
            return sys.getsizeof(obj)
        except (TypeError, AttributeError):
            # Fallback for objects that don't support getsizeof
            return len(str(obj)) * 2  # Rough estimate

    def _format_bytes(self, bytes_size: int) -> str:
        """Format bytes into human-readable string."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"

    async def get(self, key: str) -> Any:
        """Get value from cache. Returns _MISSING if not found."""
        async with self._lock:
            if key in self.cache:
                entry = self.cache[key]
                if entry.is_expired(self.ttl):
                    del self.cache[key]
                    self.misses += 1
                    return _MISSING

                # Move to end (most recently used)
                self.cache.move_to_end(key)
                entry.access_count += 1
                self.hits += 1
                return entry.value

            self.misses += 1
            return _MISSING

    async def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        async with self._lock:
            # Remove expired entries first
            await self._cleanup_expired()

            # If at capacity, remove least recently used
            while len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)

            # Add new entry
            entry = CacheEntry(value=value, timestamp=time.time())
            self.cache[key] = entry

    async def _cleanup_expired(self) -> None:
        """Remove expired entries from cache."""
        if self.ttl is None:
            return

        expired_keys = [key for key, entry in self.cache.items() if entry.is_expired(self.ttl)]

        for key in expired_keys:
            del self.cache[key]

    async def get_cache_stats(self) -> CacheStats:
        """Get cache statistics."""
        async with self._lock:
            await self._cleanup_expired()

            total_bytes = sum(self._estimate_size(entry.value) + self._estimate_size(key) for key, entry in self.cache.items())

            return CacheStats(
                current_size=len(self.cache),
                max_size=self.maxsize,
                ttl=self.ttl,
                hits=self.hits,
                misses=self.misses,
                total_size_in_memory_bytes=total_bytes,
                total_size_in_memory_pretty=self._format_bytes(total_bytes),
            )

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

    async def invalidate(self, key: str) -> bool:
        """Invalidate a specific cache entry by key."""
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    async def invalidate_by_func_args(self, func: Callable, args: tuple, kwargs: dict) -> bool:
        """Invalidate cache entry by function arguments."""
        key = self._get_cache_key(func, args, kwargs)
        return await self.invalidate(key)


class AsyncLRUCacheWrapper:
    """Wrapper that provides the cached function with additional methods."""

    def __init__(self, func: F, cache: AsyncLRUCache):
        self._func = func
        self._cache = cache
        functools.update_wrapper(self, func)

    async def __call__(self, *args, **kwargs) -> Any:
        """Call the cached function with deduplication for concurrent calls."""
        cache_key = self._cache._get_cache_key(self._func, args, kwargs)

        # Try to get from cache
        cached_result = await self._cache.get(cache_key)
        if cached_result is not _MISSING:
            return cached_result

        # Check if there's already a pending computation for this key
        if cache_key in self._cache._pending:
            # Wait for the ongoing computation
            future = self._cache._pending[cache_key]
            try:
                return await future
            except Exception:
                # If the pending computation failed, we'll let this call fail too
                raise

        # Create a future for this computation
        future = asyncio.Future()
        self._cache._pending[cache_key] = future

        try:
            # Call original function
            result = await self._func(*args, **kwargs)

            # Store in cache only if successful
            await self._cache.set(cache_key, result)

            # Set the future result
            if not future.done():
                future.set_result(result)

            return result
        except Exception as e:
            # Set the future exception only if someone is waiting
            if not future.done():
                future.set_exception(e)
            raise
        finally:
            # Remove from pending
            self._cache._pending.pop(cache_key, None)

            # Cancel the future if it wasn't used
            if not future.done():
                future.cancel()

    async def get_cache_stats(self) -> CacheStats:
        """Get cache statistics."""
        return await self._cache.get_cache_stats()

    async def clear_cache(self) -> None:
        """Clear the cache."""
        await self._cache.clear()

    async def cache_invalidate(self, *args, **kwargs) -> bool:
        """
        Invalidate cache entry for specific function arguments.

        Args:
            *args, **kwargs: Same arguments as the original function

        Returns:
            bool: True if entry was found and invalidated, False otherwise
        """
        return await self._cache.invalidate_by_func_args(self._func, args, kwargs)

    def cache_info(self) -> Dict[str, Any]:
        """Get cache info (sync version for compatibility)."""
        return {"maxsize": self._cache.maxsize, "ttl": self._cache.ttl, "ignore_params": list(self._cache.ignore_params)}

    # Preserve original function attributes
    def __getattr__(self, name: str) -> Any:
        return getattr(self._func, name)


def alru_cache(maxsize: int = 1024, ttl: Optional[float] = None, ignore_params: Optional[List[str]] = None) -> Callable[[F], AsyncLRUCacheWrapper]:
    """
    Async LRU Cache decorator.

    Args:
        maxsize: Maximum number of entries in cache (default: 1024)
        ttl: Time to live in seconds (default: None - no expiration)
        ignore_params: List of parameter names to ignore when generating cache keys

    Returns:
        Decorated function with caching capabilities
    """

    def decorator(func: F) -> AsyncLRUCacheWrapper:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("alru_cache can only be applied to async functions")

        cache = AsyncLRUCache(maxsize=maxsize, ttl=ttl, ignore_params=ignore_params)
        wrapper = AsyncLRUCacheWrapper(func, cache)

        return cast(AsyncLRUCacheWrapper, wrapper)

    return decorator
