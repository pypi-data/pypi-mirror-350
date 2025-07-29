# Async LRU Cache

A high-performance, fully asynchronous LRU (Least Recently Used) cache decorator for Python async functions. Built specifically for asyncio applications with comprehensive caching features.

⚠️ AI slop warning

[![Python 3.9+](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Fully Async**: Built from the ground up for asyncio, no blocking operations
- 🎯 **Type Safe**: Complete typing support with full IDE code completion
- ⚡ **High Performance**: Efficient LRU implementation with O(1) cache operations
- 🔧 **Highly Configurable**: Customizable cache size, TTL, and parameter filtering
- 📊 **Detailed Statistics**: Comprehensive cache performance metrics and memory usage
- 🎛️ **Flexible Control**: Manual cache invalidation and clearing capabilities
- 🛡️ **Thread Safe**: Proper async locking for concurrent access
- 💾 **Memory Efficient**: Smart memory estimation and pretty-printed size reporting

## 📦 Installation

```bash
uv add async-lru-cache
```

Or, if you're lame:

```bash
pip install async-lru-cache
```

## 🎛️ API Reference

### Decorator Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `maxsize` | `int` | `1024` | Maximum number of cache entries |
| `ttl` | `float \| None` | `None` | Time-to-live in seconds (None = no expiration) |
| `ignore_params` | `List[str] \| None` | `None` | Parameter names to ignore when generating cache keys |

### Cache Methods

All cached functions automatically get these additional methods:

#### `await func.get_cache_stats() -> CacheStats`

Returns detailed cache statistics:

```python
@dataclass
class CacheStats:
    current_size: int                    # Current number of cached entries
    max_size: int                       # Maximum cache size
    ttl: Optional[float]                # Time-to-live setting
    hits: int                          # Number of cache hits
    misses: int                        # Number of cache misses
    total_size_in_memory_bytes: int    # Estimated memory usage in bytes
    total_size_in_memory_pretty: str   # Human-readable memory usage
```

#### `await func.cache_invalidate(*args, **kwargs) -> bool`

Invalidate a specific cache entry:

```python
@alru_cache()
async def my_func(x: int, y: str) -> str:
    return f"{x}-{y}"

# Cache an entry
result = await my_func(1, "test")

# Invalidate the specific entry
success = await my_func.cache_invalidate(1, "test")  # Returns True
```

#### `await func.clear_cache() -> None`

Clear all cache entries and reset statistics:

```python
await my_func.clear_cache()
stats = await my_func.get_cache_stats()
# stats.current_size == 0, stats.hits == 0, stats.misses == 0
```

#### `func.cache_info() -> Dict[str, Any]`

Get cache configuration (synchronous):

```python
info = my_func.cache_info()
# {'maxsize': 1024, 'ttl': None, 'ignore_params': []}
```

## 📚 Examples

### Basic Usage with Different Data Types

```python
from async_lru_cache import alru_cache
import asyncio
from typing import List, Dict, Any

@alru_cache(maxsize=100)
async def process_data(
    numbers: List[int], 
    config: Dict[str, Any], 
    multiplier: float = 1.0
) -> List[float]:
    """Cache works with complex data types."""
    await asyncio.sleep(0.1)  # Simulate processing
    return [n * multiplier for n in numbers]

async def example_basic():
    # Works with lists, dicts, and any hashable arguments
    result1 = await process_data([1, 2, 3], {"mode": "fast"}, 2.0)
    result2 = await process_data([1, 2, 3], {"mode": "fast"}, 2.0)  # Cache hit
    
    print(f"Results equal: {result1 == result2}")  # True
    
    stats = await process_data.get_cache_stats()
    print(f"Memory usage: {stats.total_size_in_memory_pretty}")
```

### TTL (Time-To-Live) Caching

```python
@alru_cache(maxsize=50, ttl=60.0)  # Cache for 60 seconds
async def fetch_stock_price(symbol: str) -> float:
    """Fetch stock price with 1-minute cache."""
    await asyncio.sleep(0.5)  # Simulate API call
    # In real scenario, fetch from API
    return 100.0 + hash(symbol) % 50

async def example_ttl():
    # First call - fetches from "API"
    price1 = await fetch_stock_price("AAPL")
    
    # Second call within 60 seconds - cache hit
    price2 = await fetch_stock_price("AAPL")
    
    # Wait for cache expiration
    await asyncio.sleep(61)
    
    # Third call - cache miss, fetches again
    price3 = await fetch_stock_price("AAPL")
    
    stats = await fetch_stock_price.get_cache_stats()
    print(f"Hits: {stats.hits}, Misses: {stats.misses}")
```

### Ignoring Specific Parameters

```python
@alru_cache(maxsize=100, ignore_params=["request_id", "timestamp"])
async def get_user_permissions(
    user_id: str, 
    resource: str, 
    request_id: str,
    timestamp: float
) -> List[str]:
    """Cache user permissions, ignoring request metadata."""
    await asyncio.sleep(0.2)  # Simulate database query
    return ["read", "write"] if user_id == "admin" else ["read"]

async def example_ignore_params():
    import time
    
    # These calls will hit the same cache entry despite different
    # request_id and timestamp values
    perms1 = await get_user_permissions("admin", "document", "req-1", time.time())
    perms2 = await get_user_permissions("admin", "document", "req-2", time.time() + 1)
    perms3 = await get_user_permissions("admin", "document", "req-3", time.time() + 2)
    
    # Only the first call actually executed the function
    stats = await get_user_permissions.get_cache_stats()
    print(f"Function calls: {stats.misses}")  # Should be 1
```

### Manual Cache Invalidation

```python
@alru_cache(maxsize=200)
async def get_user_profile(user_id: str) -> Dict[str, Any]:
    """Get user profile with manual cache control."""
    await asyncio.sleep(0.3)
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "last_updated": time.time()
    }

async def update_user_profile(user_id: str, new_data: Dict[str, Any]):
    """Update user profile and invalidate cache."""
    # Update in database...
    await asyncio.sleep(0.1)
    
    # Invalidate the specific cache entry
    invalidated = await get_user_profile.cache_invalidate(user_id)
    print(f"Cache invalidated: {invalidated}")

async def example_invalidation():
    # Cache the profile
    profile1 = await get_user_profile("user123")
    
    # This would normally be a cache hit
    profile2 = await get_user_profile("user123")
    
    # Update profile and invalidate cache
    await update_user_profile("user123", {"name": "Updated Name"})
    
    # This will be a cache miss and fetch fresh data
    profile3 = await get_user_profile("user123")
    
    stats = await get_user_profile.get_cache_stats()
    print(f"Total calls: {stats.hits + stats.misses}")
```

### Advanced Cache Statistics and Monitoring

```python
@alru_cache(maxsize=1000, ttl=3600)
async def expensive_computation(data: str, iterations: int = 1000) -> str:
    """Simulate expensive computation."""
    await asyncio.sleep(iterations * 0.001)
    return f"processed_{data}_x{iterations}"

async def example_monitoring():
    # Perform various operations
    tasks = [
        expensive_computation("dataset1", 100),
        expensive_computation("dataset2", 200),
        expensive_computation("dataset1", 100),  # Cache hit
        expensive_computation("dataset3", 150),
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Get detailed statistics
    stats = await expensive_computation.get_cache_stats()
    
    print("📊 Cache Statistics:")
    print(f"   Current size: {stats.current_size}/{stats.max_size}")
    print(f"   Hit rate: {stats.hits/(stats.hits + stats.misses):.2%}")
    print(f"   Memory usage: {stats.total_size_in_memory_pretty}")
    print(f"   TTL: {stats.ttl}s" if stats.ttl else "   TTL: No expiration")
    
    # Get basic cache info
    info = expensive_computation.cache_info()
    print(f"\n⚙️  Configuration:")
    print(f"   Max size: {info['maxsize']}")
    print(f"   TTL: {info['ttl']}")
    print(f"   Ignored params: {info['ignore_params']}")
```

### Production Example: API Response Caching

```python
import aiohttp
from async_lru_cache import alru_cache
from typing import Optional

class APIClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    @alru_cache(maxsize=500, ttl=300, ignore_params=["request_timeout"])
    async def fetch_weather(
        self, 
        city: str, 
        units: str = "metric",
        request_timeout: float = 10.0
    ) -> Dict[str, Any]:
        """Fetch weather data with caching."""
        url = f"https://api.weather.com/weather/{city}"
        params = {"units": units}
        
        async with self.session.get(
            url, 
            params=params, 
            timeout=request_timeout
        ) as response:
            return await response.json()
    
    @alru_cache(maxsize=1000, ttl=3600)
    async def fetch_user_data(self, user_id: str) -> Dict[str, Any]:
        """Fetch user data with longer cache."""
        url = f"https://api.example.com/users/{user_id}"
        async with self.session.get(url) as response:
            return await response.json()
    
    async def invalidate_user_cache(self, user_id: str):
        """Invalidate user cache after updates."""
        await self.fetch_user_data.cache_invalidate(user_id)

async def production_example():
    async with APIClient() as client:
        # These calls will be cached for 5 minutes
        weather1 = await client.fetch_weather("London", "metric", 5.0)
        weather2 = await client.fetch_weather("London", "metric", 10.0)  # Cache hit!
        
        # User data cached for 1 hour
        user = await client.fetch_user_data("12345")
        
        # After user update, invalidate cache
        await client.invalidate_user_cache("12345")
        
        # Get cache statistics
        weather_stats = await client.fetch_weather.get_cache_stats()
        user_stats = await client.fetch_user_data.get_cache_stats()
        
        print(f"Weather cache: {weather_stats.hits} hits, {weather_stats.misses} misses")
        print(f"User cache: {user_stats.hits} hits, {user_stats.misses} misses")
```

## 🚀 Performance Considerations

### Memory Usage

The cache automatically estimates memory usage of stored objects. For optimal performance:

- Use reasonable `maxsize` values based on your memory constraints
- Monitor memory usage with `get_cache_stats()`
- Consider TTL for data that becomes stale

### Concurrency

- The cache uses async locks for thread safety
- Multiple concurrent calls with the same arguments may result in multiple function executions
- This is intentional to avoid blocking async operations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.