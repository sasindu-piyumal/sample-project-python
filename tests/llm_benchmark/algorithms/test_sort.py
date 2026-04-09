from typing import List

import pytest

from llm_benchmark.algorithms.sort import Sort


class TestSortListBasic:
    """Test basic functionality of Sort.sort_list()"""

    def test_empty_list(self) -> None:
        """Test that an empty list remains empty"""
        lst: List[int] = []
        Sort.sort_list(lst)
        assert lst == []

    def test_single_element(self) -> None:
        """Test that a single element list remains unchanged"""
        lst: List[int] = [42]
        Sort.sort_list(lst)
        assert lst == [42]

    def test_already_sorted_list(self) -> None:
        """Test that an already sorted list remains sorted"""
        lst: List[int] = [1, 2, 3, 4, 5]
        Sort.sort_list(lst)
        assert lst == [1, 2, 3, 4, 5]

    def test_reverse_sorted_list(self) -> None:
        """Test that a reverse sorted list is sorted in ascending order"""
        lst: List[int] = [5, 4, 3, 2, 1]
        Sort.sort_list(lst)
        assert lst == [1, 2, 3, 4, 5]

    def test_unsorted_list(self) -> None:
        """Test that an unsorted list is sorted correctly"""
        lst: List[int] = [3, 1, 4, 1, 5, 9, 2, 6]
        Sort.sort_list(lst)
        assert lst == [1, 1, 2, 3, 4, 5, 6, 9]


class TestSortListEdgeCases:
    """Test edge cases and special scenarios"""

    def test_duplicate_values(self) -> None:
        """Test sorting with duplicate values"""
        lst: List[int] = [5, 2, 5, 1, 2, 3, 2]
        Sort.sort_list(lst)
        assert lst == [1, 2, 2, 2, 3, 5, 5]

    def test_all_same_values(self) -> None:
        """Test sorting when all values are identical"""
        lst: List[int] = [7, 7, 7, 7, 7]
        Sort.sort_list(lst)
        assert lst == [7, 7, 7, 7, 7]

    def test_negative_numbers(self) -> None:
        """Test sorting with negative numbers"""
        lst: List[int] = [-3, -1, -5, -2, -4]
        Sort.sort_list(lst)
        assert lst == [-5, -4, -3, -2, -1]

    def test_mixed_positive_and_negative(self) -> None:
        """Test sorting with mixed positive and negative values"""
        lst: List[int] = [3, -1, 4, -5, 0, 2, -3]
        Sort.sort_list(lst)
        assert lst == [-5, -3, -1, 0, 2, 3, 4]

    def test_with_zero(self) -> None:
        """Test sorting with zero values"""
        lst: List[int] = [3, 0, -2, 1, 0, -1]
        Sort.sort_list(lst)
        assert lst == [-2, -1, 0, 0, 1, 3]

    def test_large_numbers(self) -> None:
        """Test sorting with large numbers"""
        lst: List[int] = [1000000, 999999, 1000001, 500000]
        Sort.sort_list(lst)
        assert lst == [500000, 999999, 1000000, 1000001]

    def test_two_elements_ascending(self) -> None:
        """Test sorting two elements in ascending order"""
        lst: List[int] = [1, 2]
        Sort.sort_list(lst)
        assert lst == [1, 2]

    def test_two_elements_descending(self) -> None:
        """Test sorting two elements in descending order"""
        lst: List[int] = [2, 1]
        Sort.sort_list(lst)
        assert lst == [1, 2]


class TestSortListInPlaceBehavior:
    """Test that sorting occurs in-place (original list object is modified)"""

    def test_returns_none(self) -> None:
        """Test that sort_list returns None (not a new list)"""
        lst: List[int] = [3, 1, 2]
        result = Sort.sort_list(lst)
        assert result is None

    def test_original_list_reference_modified(self) -> None:
        """Test that the original list object reference is modified, not replaced"""
        lst: List[int] = [5, 3, 1, 4, 2]
        original_id = id(lst)
        Sort.sort_list(lst)
        # Verify the list object is the same (same memory reference)
        assert id(lst) == original_id
        # Verify the contents are sorted
        assert lst == [1, 2, 3, 4, 5]

    def test_in_place_modification_does_not_create_copy(self) -> None:
        """Test that sorting modifies the original list, not a copy"""
        lst: List[int] = [4, 2, 3, 1]
        original_id = id(lst)
        Sort.sort_list(lst)
        # Verify same object
        assert id(lst) == original_id
        # Verify modification occurred
        assert lst == [1, 2, 3, 4]

    def test_external_reference_reflects_changes(self) -> None:
        """Test that external references to the list see the sorted contents"""
        lst: List[int] = [3, 1, 2]
        external_ref = lst  # Create another reference to the same list
        Sort.sort_list(lst)
        # Both references should point to the same sorted list
        assert external_ref == [1, 2, 3]
        assert external_ref is lst  # Same object in memory

    def test_multiple_calls_cumulative_effect(self) -> None:
        """Test that multiple calls to sort_list work correctly on already sorted lists"""
        lst: List[int] = [5, 3, 1, 4, 2]
        original_id = id(lst)
        Sort.sort_list(lst)
        assert lst == [1, 2, 3, 4, 5]
        # Call again on already sorted list
        Sort.sort_list(lst)
        assert id(lst) == original_id
        assert lst == [1, 2, 3, 4, 5]


class TestSortListCorrectness:
    """Test correctness of sorting output"""

    @pytest.mark.parametrize(
        "input_list, expected",
        [
            ([3, 1, 2], [1, 2, 3]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
            ([5, 1, 3, 2, 4], [1, 2, 3, 4, 5]),
            ([10, -5, 0, 3, -2], [-5, -2, 0, 3, 10]),
            ([1, 1, 1, 1], [1, 1, 1, 1]),
            ([2, 1, 2, 1], [1, 1, 2, 2]),
            ([], []),
            ([42], [42]),
            ([-1, -2, -3], [-3, -2, -1]),
        ],
    )
    def test_various_lists_sorted_correctly(
        self, input_list: List[int], expected: List[int]
    ) -> None:
        """Test various list configurations are sorted correctly"""
        Sort.sort_list(input_list)
        assert input_list == expected

    def test_output_is_sorted_ascending(self) -> None:
        """Test that output is sorted in ascending order"""
        lst: List[int] = [9, 2, 7, 1, 5, 3, 8, 4, 6]
        Sort.sort_list(lst)
        # Verify each element is <= the next element
        for i in range(len(lst) - 1):
            assert lst[i] <= lst[i + 1]

    def test_output_contains_same_elements(self) -> None:
        """Test that the sorted list contains all original elements"""
        original: List[int] = [7, 2, 9, 1, 5, 3, 8]
        lst = original.copy()
        Sort.sort_list(lst)
        # Verify same elements (counts matter for duplicates)
        assert sorted(original) == sorted(lst)
        assert original.count(x) == lst.count(x) for x in set(original)

    def test_stability_not_required(self) -> None:
        """Test that sort handles values correctly (stability not required)"""
        lst: List[int] = [3, 1, 3, 2]
        Sort.sort_list(lst)
        assert lst == [1, 2, 3, 3]

    def test_long_list(self) -> None:
        """Test sorting a longer list"""
        lst: List[int] = list(range(100, 0, -1))  # [100, 99, ..., 2, 1]
        Sort.sort_list(lst)
        assert lst == list(range(1, 101))  # [1, 2, ..., 99, 100]
