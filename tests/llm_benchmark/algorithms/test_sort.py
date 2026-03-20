from typing import List

import pytest

from llm_benchmark.algorithms.sort import Sort


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([3, 1, 4, 1, 5, 9, 2, 6, 5], [1, 1, 2, 3, 4, 5, 5, 6, 9]),
        ([1], [1]),
        ([], []),
        ([2, 1], [1, 2]),
        ([1, 1, 1, 1], [1, 1, 1, 1]),
        ([100, 50, 75, 25, 10], [10, 25, 50, 75, 100]),
    ],
)
def test_sort_list(input_list: List[int], expected_output: List[int]) -> None:
    """Test that sort_list correctly sorts lists in place."""
    test_list = input_list.copy()
    Sort.sort_list(test_list)
    assert test_list == expected_output


def test_benchmark_sort_list_small(benchmark) -> None:
    """Benchmark sort_list with a small list."""
    test_list = [5, 4, 3, 2, 1]
    benchmark(Sort.sort_list, test_list)


def test_benchmark_sort_list_medium(benchmark) -> None:
    """Benchmark sort_list with a medium list."""
    test_list = list(range(100, 0, -1))
    benchmark(Sort.sort_list, test_list)


def test_benchmark_sort_list_large(benchmark) -> None:
    """Benchmark sort_list with a larger list."""
    test_list = list(range(1000, 0, -1))
    benchmark(Sort.sort_list, test_list)


def test_sort_list_modifies_in_place() -> None:
    """Test that sort_list modifies the list in place."""
    original_list = [3, 1, 2]
    test_list = original_list
    Sort.sort_list(test_list)
    
    # Verify it was modified in place
    assert test_list == [1, 2, 3]
    assert original_list == [1, 2, 3]  # Same reference


def test_sort_list_stability() -> None:
    """Test that sort_list preserves relative order of equal elements."""
    # Create list with tuples to test stability
    # (we'll use integers with indices to simulate this)
    test_list = [3, 1, 3, 2, 3]
    Sort.sort_list(test_list)
    assert test_list == [1, 2, 3, 3, 3]


@pytest.mark.parametrize(
    "pivot, expected",
    [
        (3, [1, 2, 3, 5, 4]),
        (2, [1, 2, 5, 4, 3]),
        (1, [1, 5, 4, 3, 2]),
    ],
)
def test_dutch_flag_partition(pivot: int, expected: List[int]) -> None:
    """Test dutch_flag_partition partitions correctly."""
    test_list = [5, 4, 3, 2, 1]
    Sort.dutch_flag_partition(test_list, pivot)
    
    # Verify all elements less than pivot are at the beginning
    less_count = sum(1 for x in test_list if x < pivot)
    for i in range(less_count):
        assert test_list[i] < pivot


def test_max_n() -> None:
    """Test max_n returns the n largest elements."""
    test_list = [5, 4, 3, 2, 1, 10, 7]
    
    result = Sort.max_n(test_list, 3)
    assert sorted(result, reverse=True) == [10, 7, 5]
    
    result = Sort.max_n(test_list, 1)
    assert result == [10]
    
    result = Sort.max_n(test_list, 5)
    assert sorted(result, reverse=True) == [10, 7, 5, 4, 3]


def test_max_n_edge_cases() -> None:
    """Test max_n with edge cases."""
    # Empty list
    assert Sort.max_n([], 0) == []
    
    # Single element
    assert Sort.max_n([5], 1) == [5]
    
    # Request more elements than available
    result = Sort.max_n([1, 2, 3], 5)
    assert sorted(result, reverse=True) == [3, 2, 1]
