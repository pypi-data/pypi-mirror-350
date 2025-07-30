from unittest import TestCase

# Tests another import - e.g call from multiple files in real life => should still be the same cache
from tests.data import MyTestClass, reset_counter
from tests.data import sync_func
from tests.data import sync_func as sync_func_second_import
from tests.data import (
    sync_func_clear_arg_cache,
    sync_func_clear_cache,
    sync_func_use_cache,
    sync_func_with_dict,
    sync_func_with_list,
    sync_func_with_object,
)


class TestLruCache(TestCase):
    def test_lru_cache_with_cache_usage(self) -> None:
        # Arrange
        reset_counter()

        # Act
        result1 = sync_func_second_import("one", "one")
        result2 = sync_func_second_import("two", "two")
        result3 = sync_func_second_import("three", "three")

        result1_second = sync_func("one", "one")
        result2_second = sync_func("two", "two")
        result3_second = sync_func("three", "three")

        result4 = sync_func("four", "four")
        result_after_reached_max = sync_func("one", "one")

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
        reset_counter()

        # Act
        result1 = sync_func_use_cache("one", "one", lru_use_cache=False)
        result2 = sync_func_use_cache("two", "two", lru_use_cache=False)
        result3 = sync_func_use_cache("three", "three", lru_use_cache=False)

        result1_second = sync_func_use_cache("one", "one", lru_use_cache=False)
        result2_second = sync_func_use_cache("two", "two", lru_use_cache=False)
        result3_second = sync_func_use_cache("three", "three", lru_use_cache=False)

        # Assert
        self.assertEqual(result1, "one-one-1")
        self.assertEqual(result2, "two-two-2")
        self.assertEqual(result3, "three-three-3")

        self.assertEqual(result1_second, "one-one-4")
        self.assertEqual(result2_second, "two-two-5")
        self.assertEqual(result3_second, "three-three-6")

    def test_lru_cache_with_clear_cache(self) -> None:
        # Arrange
        reset_counter()

        # Act
        result1 = sync_func_clear_cache("one", "one", lru_clear_cache=False)
        result2 = sync_func_clear_cache("two", "two", lru_clear_cache=False)

        result1_second = sync_func_clear_cache("one", "one", lru_clear_cache=False)
        result2_second = sync_func_clear_cache("two", "two", lru_clear_cache=False)

        result1_third = sync_func_clear_cache("one", "one", lru_clear_cache=True)  # Clear
        result2_third = sync_func_clear_cache("two", "two", lru_clear_cache=False)

        result1_fourth = sync_func_clear_cache("one", "one", lru_clear_cache=False)
        result2_fourth = sync_func_clear_cache("two", "two", lru_clear_cache=False)

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
        reset_counter()

        # Act
        result1 = sync_func_clear_arg_cache("one", "one", lru_clear_arg_cache=True)  # May not fail, if not yet cached
        result2 = sync_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False)

        result1_second = sync_func_clear_arg_cache("one", "one", lru_clear_arg_cache=False)
        result2_second = sync_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False)

        result1_third = sync_func_clear_arg_cache("one", "one", lru_clear_arg_cache=True)  # Clear for args: one, one
        result2_third = sync_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False)

        result1_fourth = sync_func_clear_arg_cache("one", "one", lru_clear_arg_cache=False)
        result2_fourth = sync_func_clear_arg_cache("two", "two", lru_clear_arg_cache=False)

        # Assert
        self.assertEqual(result1, "one-one-1")
        self.assertEqual(result2, "two-two-2")

        self.assertEqual(result1_second, "one-one-1")
        self.assertEqual(result2_second, "two-two-2")

        self.assertEqual(result1_third, "one-one-3")
        self.assertEqual(result2_third, "two-two-2")

        self.assertEqual(result1_fourth, "one-one-3")
        self.assertEqual(result2_fourth, "two-two-2")

    def test_lru_cache_with_list(self) -> None:
        # Arrange
        reset_counter()

        # Act
        result1 = sync_func_with_list(["one", "two"])
        result2 = sync_func_with_list(["one", "two"])
        result3 = sync_func_with_list(["three", "four"])

        # Assert
        self.assertEqual(result1, 1)
        self.assertEqual(result2, 1)
        self.assertEqual(result3, 2)

    def test_lru_cache_with_dict(self) -> None:
        # Arrange
        reset_counter()

        # Act
        result1 = sync_func_with_dict({"keyOne": "valueOne", "keyTwo": "valueTwo"})
        result2 = sync_func_with_dict({"keyOne": "valueOne", "keyTwo": "valueTwo"})
        result3 = sync_func_with_dict({"keyOne": "otherValueOne", "keyTwo": "valueTwo"})

        # Assert
        self.assertEqual(result1, 1)
        self.assertEqual(result2, 1)
        self.assertEqual(result3, 2)

    def test_lru_cache_with_object(self) -> None:
        # Arrange
        reset_counter()
        object_one = MyTestClass("object_one")
        similar_object_one = MyTestClass("object_one")  # Test with different reference
        object_two = MyTestClass("object_two")

        # Act
        result1 = sync_func_with_object(object_one)
        result2 = sync_func_with_object(object_one)
        result3 = sync_func_with_object(similar_object_one)
        result4 = sync_func_with_object(object_two)

        # Assert
        self.assertEqual(result1, 1)
        self.assertEqual(result2, 1)
        self.assertEqual(result3, 1)
        self.assertEqual(result4, 2)
