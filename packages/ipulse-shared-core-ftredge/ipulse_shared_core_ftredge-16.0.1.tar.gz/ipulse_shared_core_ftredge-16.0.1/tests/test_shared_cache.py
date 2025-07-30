"""Tests for the SharedCache implementation."""

import time
import unittest
import logging
from ipulse_shared_core_ftredge.cache.shared_cache import SharedCache

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestSharedCache(unittest.TestCase):
    """Test cases for SharedCache."""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = SharedCache[str](
            name="TestCache",
            ttl=0.5,  # Short TTL for faster testing
            enabled=True,
            logger=logger
        )

    def test_cache_set_get(self):
        """Test basic cache set and get operations."""
        # Set a value
        self.cache.set("test_key", "test_value")

        # Get the value
        cached_value = self.cache.get("test_key")

        # Verify value was cached
        self.assertEqual(cached_value, "test_value")

    def test_cache_ttl_expiration(self):
        """Test cache TTL expiration."""
        # Set a value
        self.cache.set("expiring_key", "expiring_value")

        # Verify it's initially cached
        self.assertEqual(self.cache.get("expiring_key"), "expiring_value")

        # Wait for TTL to expire
        time.sleep(0.6)  # Slightly longer than TTL (0.5s)

        # Verify value is no longer cached
        self.assertIsNone(self.cache.get("expiring_key"))

    def test_cache_invalidate(self):
        """Test cache invalidation."""
        # Set multiple values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")

        # Invalidate specific key
        self.cache.invalidate("key1")

        # Verify key1 is gone but key2 remains
        self.assertIsNone(self.cache.get("key1"))
        self.assertEqual(self.cache.get("key2"), "value2")

    def test_cache_invalidate_all(self):
        """Test invalidating all cache entries."""
        # Set multiple values
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")

        # Invalidate all
        self.cache.invalidate_all()

        # Verify both keys are gone
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))

    def test_cache_get_or_set(self):
        """Test get_or_set functionality."""
        # Define a counter to verify how many times the loader is called
        counter = [0]

        def data_loader():
            counter[0] += 1
            return f"loaded_value_{counter[0]}"

        # First call should use data_loader
        value1, was_cached1 = self.cache.get_or_set("loader_key", data_loader)

        # Second call should use cached value
        value2, was_cached2 = self.cache.get_or_set("loader_key", data_loader)

        # Verify results
        self.assertEqual(value1, "loaded_value_1")
        self.assertEqual(value2, "loaded_value_1")  # Same value from cache
        self.assertFalse(was_cached1)  # First call was not cached
        self.assertTrue(was_cached2)   # Second call was cached
        self.assertEqual(counter[0], 1)  # Loader called exactly once

    def test_cache_disabled(self):
        """Test cache behavior when disabled."""
        # Create disabled cache
        disabled_cache = SharedCache[str](
            name="DisabledCache",
            ttl=1.0,
            enabled=False,
            logger=logger
        )

        # Set a value
        disabled_cache.set("disabled_key", "disabled_value")

        # Attempt to get - should return None since cache is disabled
        cached_value = disabled_cache.get("disabled_key")
        self.assertIsNone(cached_value)

    def test_cache_generic_typing(self):
        """Test cache with different data types."""
        # Integer cache
        int_cache = SharedCache[int](name="IntCache", ttl=1.0, enabled=True)
        int_cache.set("int_key", 123)
        self.assertEqual(int_cache.get("int_key"), 123)

        # Dictionary cache
        dict_cache = SharedCache[dict](name="DictCache", ttl=1.0, enabled=True)
        dict_cache.set("dict_key", {"a": 1, "b": 2})
        self.assertEqual(dict_cache.get("dict_key"), {"a": 1, "b": 2})

    def test_cache_stats(self):
        """Test cache statistics."""
        # Add some data
        self.cache.set("stats_key1", "stats_value1")
        self.cache.set("stats_key2", "stats_value2")

        # Get stats
        stats = self.cache.get_stats()

        # Verify stats
        self.assertEqual(stats["name"], "TestCache")
        self.assertEqual(stats["enabled"], True)
        self.assertEqual(stats["ttl_seconds"], 0.5)
        self.assertEqual(stats["item_count"], 2)
        self.assertIn("stats_key1", stats["first_20_keys"])
        self.assertIn("stats_key2", stats["first_20_keys"])
        self.assertEqual(stats["total_keys"], 2)


if __name__ == "__main__":
    unittest.main()
