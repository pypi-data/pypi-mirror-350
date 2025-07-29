import asyncio
import functools
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

    def _make_hashable(self, obj: Any) -> Any:
        """Convert unhashable types to hashable equivalents."""
        if isinstance(obj, (str, int, float, bool, type(None), bytes)):
            return obj
        elif isinstance(obj, (list, tuple)):
            return tuple(self._make_hashable(item) for item in obj)
        elif isinstance(obj, dict):
            return tuple(sorted((k, self._make_hashable(v)) for k, v in obj.items()))
        elif isinstance(obj, set):
            return tuple(sorted(self._make_hashable(item) for item in obj))
        elif isinstance(obj, frozenset):
            return frozenset(self._make_hashable(item) for item in obj)
        else:
            # For complex objects (dataclasses, pydantic, etc)
            # Try common patterns first

            # Check if it's already hashable
            try:
                hash(obj)
                return obj
            except TypeError:
                pass

            # Try __dict__ for dataclasses/pydantic models
            if hasattr(obj, "__dict__"):
                return (obj.__class__.__name__, self._make_hashable(obj.__dict__))

            # Try __slots__
            if hasattr(obj, "__slots__"):
                slot_values = tuple((slot, self._make_hashable(getattr(obj, slot, None))) for slot in obj.__slots__ if hasattr(obj, slot))
                return (obj.__class__.__name__, slot_values)

            # Last resort: use repr (but this is slow and might not be stable)
            return repr(obj)

    def _get_cache_key(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function arguments efficiently."""
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Filter out ignored parameters
        filtered_args = {name: value for name, value in bound_args.arguments.items() if name not in self.ignore_params}

        # Build hashable key components
        key_parts = [
            func.__module__,
            func.__qualname__,
        ]

        # Convert args to hashable format
        for name in sorted(filtered_args.keys()):
            value = filtered_args[name]
            hashable_value = self._make_hashable(value)
            key_parts.append((name, hashable_value))

        # Try to use Python's hash directly (fast path)
        try:
            # Use a fixed string prefix to avoid collisions with other uses of hash()
            cache_key = f"alru:{hash(tuple(key_parts))}"
            return cache_key
        except TypeError:
            # Fallback for unhashable types that slipped through
            # Use repr as last resort, but don't hash it with SHA
            key_str = "|".join(f"{part}" if isinstance(part, str) else repr(part) for part in key_parts)
            # Use Python's hash with the string - much faster than SHA256
            # Add length to reduce collision probability
            return f"alru:{len(key_str)}:{hash(key_str)}"

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

    def _deep_getsizeof(self, obj: Any, seen: Optional[set] = None) -> int:
        """Calculate deep size of an object including all referenced objects."""
        size = sys.getsizeof(obj)

        if seen is None:
            seen = set()

        obj_id = id(obj)
        if obj_id in seen:
            return 0  # Avoid counting the same object twice

        seen.add(obj_id)

        if isinstance(obj, dict):
            size += sum(self._deep_getsizeof(k, seen) + self._deep_getsizeof(v, seen) for k, v in obj.items())
        elif isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(self._deep_getsizeof(item, seen) for item in obj)
        elif hasattr(obj, "__dict__"):
            size += self._deep_getsizeof(obj.__dict__, seen)
        elif hasattr(obj, "__slots__"):
            size += sum(self._deep_getsizeof(getattr(obj, slot, None), seen) for slot in obj.__slots__ if hasattr(obj, slot))

        return size

    async def get_cache_stats(self) -> CacheStats:
        """Get cache statistics."""
        async with self._lock:
            await self._cleanup_expired()

            total_bytes = 0

            # Calculate size of cache entries
            for key, entry in self.cache.items():
                # Size of the key
                total_bytes += sys.getsizeof(key)
                # Size of the CacheEntry object
                total_bytes += sys.getsizeof(entry)
                # Deep size of the cached value
                total_bytes += self._deep_getsizeof(entry.value)
                # Size of timestamp and access_count
                total_bytes += sys.getsizeof(entry.timestamp)
                total_bytes += sys.getsizeof(entry.access_count)

            # OrderedDict overhead (approximate)
            total_bytes += sys.getsizeof(self.cache)

            # Pending futures
            total_bytes += sys.getsizeof(self._pending)
            for k, v in self._pending.items():
                total_bytes += sys.getsizeof(k) + sys.getsizeof(v)

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
        """Call the cached function with proper deduplication for concurrent calls."""
        cache_key = self._cache._get_cache_key(self._func, args, kwargs)

        # First check without holding the lock for performance
        cached_result = await self._cache.get(cache_key)
        if cached_result is not _MISSING:
            return cached_result

        # Need to handle concurrent calls properly
        async with self._cache._lock:
            # Double-check after acquiring lock
            if cache_key in self._cache.cache:
                entry = self._cache.cache[cache_key]
                if not entry.is_expired(self._cache.ttl):
                    self._cache.cache.move_to_end(cache_key)
                    entry.access_count += 1
                    self._cache.hits += 1
                    return entry.value

            # Check if computation is already in progress
            if cache_key in self._cache._pending:
                future = self._cache._pending[cache_key]

        # Wait outside the lock if computation is in progress
        if cache_key in self._cache._pending:
            try:
                return await future
            except Exception:
                raise

        # Create future for this computation
        future = asyncio.Future()
        async with self._cache._lock:
            # Final check before starting computation
            if cache_key not in self._cache._pending:
                self._cache._pending[cache_key] = future
            else:
                # Someone else started computation while we were waiting
                future = self._cache._pending[cache_key]

        # If we're not the one computing, wait for result
        if future != self._cache._pending.get(cache_key):
            return await future

        try:
            result = await self._func(*args, **kwargs)
            await self._cache.set(cache_key, result)
            if not future.done():
                future.set_result(result)
            return result
        except Exception as e:
            if not future.done():
                future.set_exception(e)
            raise
        finally:
            async with self._cache._lock:
                self._cache._pending.pop(cache_key, None)

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
