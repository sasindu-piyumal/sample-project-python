from typing import List

import pytest

from llm_benchmark.algorithms.sort import Sort


@pytest.mark.parametrize(
    "v, expected",
    [
        ([1], [1]),
        ([1, 2, 3], [1, 2, 3]),
        ([3, 2, 1], [1, 2, 3]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([3, 3, 2, 2, 4, 3, 0, 5], [0, 2, 2, 3, 3, 3, 4, 5]),
        ([1, 1, 1], [1, 1, 1]),
    ],
)
def test_sort_list(v: List[int], expected: List[int]) -> None:
    """Test that sort_list correctly sorts in place"""
    Sort.sort_list(v)
    assert v == expected


def test_benchmark_sort_list(benchmark) -> None:
    """Benchmark the sort_list function"""
    v = [5, 4, 3, 2, 1]
    benchmark(Sort.sort_list, v)


@pytest.mark.parametrize(
    "v, pivot, expected_partitions",
    [
        # Single element
        ([1], 1, ([], [1], [])),
        # All less than pivot
        ([1, 2, 3], 5, ([1, 2, 3], [], [])),
        # All greater than pivot
        ([4, 5, 6], 2, ([], [], [4, 5, 6])),
        # All equal to pivot
        ([3, 3, 3], 3, ([], [3, 3, 3], [])),
        # Mixed
        ([5, 3, 2, 4, 3], 3, ([2], [3, 3], [5, 4])),
    ],
)
def test_dutch_flag_partition(v: List[int], pivot: int, expected_partitions) -> None:
    """Test that dutch_flag_partition correctly partitions around pivot"""
    Sort.dutch_flag_partition(v, pivot)
    
    less_count, equal_count = 0, 0
    
    # Count values less than, equal to, and greater than pivot
    for val in v:
        if val < pivot:
            less_count += 1
        elif val == pivot:
            equal_count += 1
    
    # Verify partitioning: all less values come first, then equal, then greater
    for i in range(less_count):
        assert v[i] < pivot
    
    for i in range(less_count, less_count + equal_count):
        assert v[i] == pivot
    
    for i in range(less_count + equal_count, len(v)):
        assert v[i] > pivot


def test_benchmark_dutch_flag_partition(benchmark) -> None:
    """Benchmark the dutch_flag_partition function"""
    v = [5, 3, 2, 4, 3]
    benchmark(Sort.dutch_flag_partition, v, 3)


@pytest.mark.parametrize(
    "v, n, expected",
    [
        ([1, 2, 3, 4, 5], 1, [5]),
        ([1, 2, 3, 4, 5], 3, [5, 4, 3]),
        ([5, 4, 3, 2, 1], 2, [5, 4]),
        ([1, 1, 1, 1, 1], 2, [1, 1]),
        ([10, 20, 30, 40, 50], 4, [50, 40, 30, 20]),
    ],
)
def test_max_n(v: List[int], n: int, expected: List[int]) -> None:
    """Test that max_n returns the n largest values"""
    result = Sort.max_n(v, n)
    assert sorted(result, reverse=True) == sorted(expected, reverse=True)
    assert len(result) == len(expected)


def test_benchmark_max_n(benchmark) -> None:
    """Benchmark the max_n function"""
    benchmark(Sort.max_n, [1, 2, 3, 4, 5], 3)
