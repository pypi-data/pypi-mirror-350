import asyncio
from unittest import TestCase

# Tests another import - e.g call from multiple files in real life => should still be the same cache
from tests.data import async_func
from tests.data import async_func as async_func_second_import
from tests.data import async_func_clear_arg_cache, async_func_clear_cache, async_func_use_cache, reset_counter


class TestLruCache(TestCase):
    def test_lru_cache_with_cache_usage(self) -> None:
        # Arrange
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reset_counter()

        # Act
        result1 = loop.run_until_complete(async_func_second_import("one", "one"))
        result2 = loop.run_until_complete(async_func_second_import("two", "two"))
        result3 = loop.run_until_complete(async_func_second_import("three", "three"))

        result1_second = loop.run_until_complete(async_func("one", "one"))
        result2_second = loop.run_until_complete(async_func("two", "two"))
        result3_second = loop.run_until_complete(async_func("three", "three"))

        result4 = loop.run_until_complete(async_func("four", "four"))
        result_after_reached_max = loop.run_until_complete(async_func("one", "one"))

        # Assert
        self.assertEqual(result1, "one-one-1")
        self.assertEqual(result2, "two-two-2")
        self.assertEqual(result3, "three-three-3")

        self.assertEqual(result1_second, "one-one-1")
        self.assertEqual(result2_second, "two-two-2")
        self.assertEqual(result3_second, "three-three-3")

        self.assertEqual(result4, "four-four-4")
        # Now the counter has to be increased (indicating a method call) because one-one isn't cached anymore
        # due to the cache limit of 3 items
        self.assertEqual(result_after_reached_max, "one-one-5")

    def test_lru_cache_with_disabled_cache(self) -> None:
        # Arrange
        loop = asyncio.get_event_loop()
        reset_counter()

        # Act
        result1 = loop.run_until_complete(async_func_use_cache("one", "one", lru_use_cache=False))
        result2 = loop.run_until_complete(async_func_use_cache("two", "two", lru_use_cache=False))
        result3 = loop.run_until_complete(async_func_use_cache("three", "three", lru_use_cache=False))

        result1_second = loop.run_until_complete(async_func_use_cache("one", "one", lru_use_cache=False))
        result2_second = loop.run_until_complete(async_func_use_cache("two", "two", lru_use_cache=False))
        result3_second = loop.run_until_complete(async_func_use_cache("three", "three", lru_use_cache=False))

        # Assert
        self.assertEqual(result1, "one-one-1")
        self.assertEqual(result2, "two-two-2")
        self.assertEqual(result3, "three-three-3")

        self.assertEqual(result1_second, "one-one-4")
        self.assertEqual(result2_second, "two-two-5")
        self.assertEqual(result3_second, "three-three-6")

    def test_lru_cache_with_clear_cache(self) -> None:
        # Arrange
        loop = asyncio.get_event_loop()
        reset_counter()

        # Act
        result1 = loop.run_until_complete(async_func_clear_cache("one", "one", lru_clear_cache=False))
        result2 = loop.run_until_complete(async_func_clear_cache("two", "two", lru_clear_cache=False))

        result1_second = loop.run_until_complete(async_func_clear_cache("one", "one", lru_clear_cache=False))
        result2_second = loop.run_until_complete(async_func_clear_cache("two", "two", lru_clear_cache=False))

        result1_third = loop.run_until_complete(async_func_clear_cache("one", "one", lru_clear_cache=True))  # Clear
        result2_third = loop.run_until_complete(async_func_clear_cache("two", "two", lru_clear_cache=False))

        result1_fourth = loop.run_until_complete(async_func_clear_cache("one", "one", lru_clear_cache=False))
        result2_fourth = loop.run_until_complete(async_func_clear_cache("two", "two", lru_clear_cache=False))

        # Assert
        self.assertEqual(result1, "one-one-1")
        self.assertEqual(result2, "two-two-2")

        self.assertEqual(result1_second, "one-one-1")
        self.assertEqual(result2_second, "two-two-2")

        self.assertEqual(result1_third, "one-one-3")
        self.assertEqual(result2_third, "two-two-4")

        self.assertEqual(result1_fourth, "one-one-3")
        self.assertEqual(result2_fourth, "two-two-4")

    def test_lru_cache_with_clear_arg_cache(self) -> None:
        # Arrange
        loop = asyncio.get_event_loop()
        reset_counter()

        # Act
        result1 = loop.run_until_complete(
            async_func_clear_arg_cache("one", "one", lru_clear_arg_cache=True)
        )  # May not fail if not yet cached
        result2 = loop.run_until_complete(async_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False))

        result1_second = loop.run_until_complete(async_func_clear_arg_cache("one", "one", lru_clear_arg_cache=False))
        result2_second = loop.run_until_complete(async_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False))

        result1_third = loop.run_until_complete(
            async_func_clear_arg_cache("one", "one", lru_clear_arg_cache=True)
        )  # Clear for args: one, one
        result2_third = loop.run_until_complete(async_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False))

        result1_fourth = loop.run_until_complete(async_func_clear_arg_cache("one", "one", lru_clear_arg_cache=False))
        result2_fourth = loop.run_until_complete(async_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False))

        # Assert
        self.assertEqual(result1, "one-one-1")
        self.assertEqual(result2, "two-two-2")

        self.assertEqual(result1_second, "one-one-1")
        self.assertEqual(result2_second, "two-two-2")

        self.assertEqual(result1_third, "one-one-3")
        self.assertEqual(result2_third, "two-two-2")

        self.assertEqual(result1_fourth, "one-one-3")
        self.assertEqual(result2_fourth, "two-two-2")
