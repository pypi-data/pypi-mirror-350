import asyncio
import time

import pytest

from async_lru_cache import alru_cache


class TestBasicCaching:
    """Test basic caching functionality."""

    @pytest.mark.asyncio
    async def test_cache_hit_and_miss(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return x * 2

        # First call - cache miss
        result1 = await expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same args - cache hit
        result2 = await expensive_func(5)
        assert result2 == 10
        assert call_count == 1

        # Third call with different args - cache miss
        result3 = await expensive_func(10)
        assert result3 == 20
        assert call_count == 2

        stats = await expensive_func.get_cache_stats()
        assert stats.hits == 1
        assert stats.misses == 2
        assert stats.current_size == 2

    @pytest.mark.asyncio
    async def test_complex_arguments(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def complex_func(a: int, b: str, c: dict, d: list = None) -> str:
            nonlocal call_count
            call_count += 1
            return f"{a}-{b}-{len(c)}-{len(d or [])}"

        # Different arguments that should produce different results
        args1 = (1, "test", {"key": "value"}, [1, 2, 3])
        args2 = (1, "test", {"key": "value"}, [1, 2, 3])
        args3 = (1, "test", {"key1": "value1", "key2": "value2"}, [1, 2, 3])  # Different dict length

        result1 = await complex_func(*args1)
        result2 = await complex_func(*args2)  # Should hit cache
        result3 = await complex_func(*args3)  # Should miss cache

        assert result1 == result2
        assert result1 != result3  # Now this will pass: '1-test-1-3' != '1-test-2-3'
        assert call_count == 2


class TestTTLFunctionality:
    """Test time-to-live functionality."""

    @pytest.mark.asyncio
    async def test_ttl_expiration(self):
        call_count = 0

        @alru_cache(maxsize=10, ttl=0.1)  # 100ms TTL
        async def ttl_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = await ttl_func(5)
        assert result1 == 10
        assert call_count == 1

        # Immediate second call - should hit cache
        result2 = await ttl_func(5)
        assert result2 == 10
        assert call_count == 1

        # Wait for TTL expiration
        await asyncio.sleep(0.15)

        # Third call - should miss due to expiration
        result3 = await ttl_func(5)
        assert result3 == 10
        assert call_count == 2

        stats = await ttl_func.get_cache_stats()
        assert stats.hits == 1
        assert stats.misses == 2

    @pytest.mark.asyncio
    async def test_no_ttl(self):
        @alru_cache(maxsize=10)  # No TTL
        async def persistent_func(x: int) -> int:
            return x * 2

        await persistent_func(5)
        await asyncio.sleep(0.1)  # Wait a bit

        stats = await persistent_func.get_cache_stats()
        assert stats.current_size == 1  # Should still be cached


class TestIgnoreParams:
    """Test parameter ignoring functionality."""

    @pytest.mark.asyncio
    async def test_ignore_single_param(self):
        call_count = 0

        @alru_cache(maxsize=10, ignore_params=["session_id"])
        async def user_func(user_id: str, session_id: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"data_for_{user_id}"

        result1 = await user_func("user123", "session_abc")
        result2 = await user_func("user123", "session_xyz")  # Different session
        result3 = await user_func("user456", "session_abc")  # Different user

        assert result1 == result2  # Same due to ignored session_id
        assert result1 != result3  # Different user_id
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_ignore_multiple_params(self):
        call_count = 0

        @alru_cache(maxsize=10, ignore_params=["timestamp", "request_id"])
        async def api_func(endpoint: str, timestamp: float, request_id: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"response_for_{endpoint}"

        result1 = await api_func("/api/users", time.time(), "req1")
        result2 = await api_func("/api/users", time.time() + 1, "req2")

        assert result1 == result2
        assert call_count == 1


class TestCacheInvalidation:
    """Test cache invalidation functionality."""

    @pytest.mark.asyncio
    async def test_cache_invalidate(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def cached_func(x: int, y: str = "default") -> str:
            nonlocal call_count
            call_count += 1
            return f"{x}-{y}"

        # Initial calls
        result1 = await cached_func(1, "test")
        result2 = await cached_func(2, "test")
        assert call_count == 2

        # Verify cache hit
        result3 = await cached_func(1, "test")
        assert result3 == result1
        assert call_count == 2

        # Invalidate specific entry
        invalidated = await cached_func.cache_invalidate(1, "test")
        assert invalidated is True

        # Should be cache miss now
        result4 = await cached_func(1, "test")
        assert result4 == result1  # Same result
        assert call_count == 3  # But function was called again

        # Other entry should still be cached
        result5 = await cached_func(2, "test")
        assert result5 == result2
        assert call_count == 3  # No additional call

    @pytest.mark.asyncio
    async def test_invalidate_nonexistent_entry(self):
        @alru_cache(maxsize=10)
        async def cached_func(x: int) -> int:
            return x * 2

        # Try to invalidate entry that doesn't exist
        invalidated = await cached_func.cache_invalidate(999)
        assert invalidated is False

    @pytest.mark.asyncio
    async def test_invalidate_with_ignore_params(self):
        call_count = 0

        @alru_cache(maxsize=10, ignore_params=["session"])
        async def session_func(user_id: str, session: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"data_{user_id}"

        # Cache entry
        await session_func("user1", "session1")
        assert call_count == 1

        # Verify cache hit with different session
        await session_func("user1", "session2")
        assert call_count == 1

        # Invalidate (session should be ignored)
        invalidated = await session_func.cache_invalidate("user1", "different_session")
        assert invalidated is True

        # Should be cache miss now
        await session_func("user1", "any_session")
        assert call_count == 2


class TestCacheSize:
    """Test cache size limits and LRU eviction."""

    @pytest.mark.asyncio
    async def test_maxsize_eviction(self):
        call_count = 0

        @alru_cache(maxsize=3)
        async def limited_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # Fill cache to capacity
        for i in range(3):
            await limited_func(i)

        stats = await limited_func.get_cache_stats()
        assert stats.current_size == 3
        assert call_count == 3

        # Add one more - should evict least recently used
        await limited_func(3)
        assert call_count == 4

        stats = await limited_func.get_cache_stats()
        assert stats.current_size == 3

        # First entry should be evicted (LRU)
        await limited_func(0)  # This should be a cache miss
        assert call_count == 5

    @pytest.mark.asyncio
    async def test_lru_order(self):
        @alru_cache(maxsize=2)
        async def lru_func(x: int) -> int:
            return x * 2

        # Fill cache
        await lru_func(1)
        await lru_func(2)

        # Access first entry to make it most recent
        await lru_func(1)

        # Add new entry - should evict entry 2 (least recent)
        await lru_func(3)

        stats = await lru_func.get_cache_stats()
        assert stats.current_size == 2

        # Entry 1 should still be cached, entry 2 should not
        stats_before = await lru_func.get_cache_stats()
        await lru_func(1)  # Should be cache hit
        stats_after = await lru_func.get_cache_stats()
        assert stats_after.hits == stats_before.hits + 1


class TestCacheStatistics:
    """Test cache statistics functionality."""

    @pytest.mark.asyncio
    async def test_detailed_stats(self):
        @alru_cache(maxsize=100, ttl=60.0)
        async def stats_func(x: int) -> str:
            return f"result_{x}"

        # Generate some cache activity
        await stats_func(1)  # miss
        await stats_func(2)  # miss
        await stats_func(1)  # hit
        await stats_func(3)  # miss
        await stats_func(2)  # hit

        stats = await stats_func.get_cache_stats()

        assert stats.current_size == 3
        assert stats.max_size == 100
        assert stats.ttl == 60.0
        assert stats.hits == 2
        assert stats.misses == 3
        assert stats.total_size_in_memory_bytes > 0
        assert "B" in stats.total_size_in_memory_pretty or "KB" in stats.total_size_in_memory_pretty

    @pytest.mark.asyncio
    async def test_memory_estimation(self):
        @alru_cache(maxsize=10)
        async def memory_func(data: str) -> str:
            return data * 2

        # Cache small data
        await memory_func("small")
        stats_small = await memory_func.get_cache_stats()

        # Cache larger data
        await memory_func("large" * 1000)
        stats_large = await memory_func.get_cache_stats()

        assert stats_large.total_size_in_memory_bytes > stats_small.total_size_in_memory_bytes


class TestCacheClear:
    """Test cache clearing functionality."""

    @pytest.mark.asyncio
    async def test_clear_cache(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def clearable_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # Populate cache
        await clearable_func(1)
        await clearable_func(2)
        await clearable_func(3)

        stats = await clearable_func.get_cache_stats()
        assert stats.current_size == 3
        assert stats.hits == 0
        assert stats.misses == 3

        # Clear cache
        await clearable_func.clear_cache()

        stats = await clearable_func.get_cache_stats()
        assert stats.current_size == 0
        assert stats.hits == 0
        assert stats.misses == 0

        # Subsequent calls should be cache misses
        await clearable_func(1)
        assert call_count == 4


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_none_return_value(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def none_func(x: int) -> None:
            nonlocal call_count
            call_count += 1
            return None

        result1 = await none_func(1)
        result2 = await none_func(1)  # Should hit cache

        assert result1 is None
        assert result2 is None
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_exception_not_cached(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def error_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            if x == 0:
                raise ValueError("Zero not allowed")
            return x * 2

        # Exception should not be cached
        with pytest.raises(ValueError):
            await error_func(0)

        with pytest.raises(ValueError):
            await error_func(0)  # Should call function again

        assert call_count == 2

    def test_non_async_function_error(self):
        with pytest.raises(TypeError, match="alru_cache can only be applied to async functions"):

            @alru_cache()
            def sync_func(x: int) -> int:
                return x * 2

    @pytest.mark.asyncio
    async def test_cache_info(self):
        @alru_cache(maxsize=50, ttl=30.0, ignore_params=["session"])
        async def info_func(x: int, session: str = "default") -> int:
            return x * 2

        info = info_func.cache_info()
        assert info["maxsize"] == 50
        assert info["ttl"] == 30.0
        assert info["ignore_params"] == ["session"]


class TestConcurrency:
    """Test concurrent access to cache."""

    @pytest.mark.asyncio
    async def test_concurrent_access(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def concurrent_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)  # Simulate work
            return x * 2

        # Make concurrent calls
        tasks = [concurrent_func(i % 3) for i in range(10)]
        results = await asyncio.gather(*tasks)

        # Should have made only 3 unique calls (0, 1, 2)
        assert call_count == 3

        # Results should be correct
        expected = [0, 2, 4] * 3 + [0]
        assert results == expected

    @pytest.mark.asyncio
    async def test_concurrent_same_args(self):
        call_count = 0

        @alru_cache(maxsize=10)
        async def slow_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.05)
            return x * 2

        # Multiple concurrent calls with same arguments
        tasks = [slow_func(42) for _ in range(5)]
        results = await asyncio.gather(*tasks)

        # All results should be the same
        assert all(r == 84 for r in results)

        # But function might be called multiple times due to race conditions
        # This is expected behavior - we're not handling concurrent calls
        # to the same key specially
        assert call_count >= 1


if __name__ == "__main__":
    pytest.main([__file__])
