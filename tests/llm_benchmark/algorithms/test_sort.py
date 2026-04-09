from typing import List

import pytest

from llm_benchmark.algorithms.sort import Sort


# ============================================================================
# Functional Tests for Sort.max_n()
# ============================================================================

@pytest.mark.parametrize(
    "v, n, expected",
    [
        ([5, 3, 9, 1, 7], 1, [9]),
        ([5, 3, 9, 1, 7], 2, [9, 7]),
        ([5, 3, 9, 1, 7], 3, [9, 7, 5]),
        ([1, 2, 3, 4, 5], 2, [5, 4]),
        ([10, 20, 30, 40, 50], 3, [50, 40, 30]),
        ([5, 5, 5, 5, 5], 2, [5, 5]),
        ([1], 1, [1]),
        ([3, 1, 4, 1, 5, 9, 2, 6], 4, [9, 6, 5, 4]),
    ],
)
def test_max_n_functionality(v: List[int], n: int, expected: List[int]) -> None:
    """Test that max_n correctly returns the n largest elements in descending order."""
    assert Sort.max_n(v, n) == expected


# ============================================================================
# Performance Benchmarks for Sort.max_n()
# ============================================================================
# Current Complexity: O(n*m) where n=list length, m=number of max elements
# - For each of m iterations, we scan the remaining list to find max: O(n)
# - Each iteration also involves a list.pop() which is O(n) in worst case
# - Expected to improve with heap-based approach: O(n log m) or O(m log m)
# ============================================================================


# SMALL INPUT BENCHMARKS (100 elements)
# Expected to show baseline performance for small lists
# Even O(n*m) is acceptable at this scale

def test_benchmark_max_n_small_n1(benchmark) -> None:
    """
    Benchmark: Small list (100 elements), finding 1 max element.
    Input: 100 elements, n=1
    Current Complexity: O(100*1) = O(100)
    Optimized Expected: O(100 log 1) = O(100)
    """
    v = list(range(100))
    benchmark(Sort.max_n, v, 1)


def test_benchmark_max_n_small_n5(benchmark) -> None:
    """
    Benchmark: Small list (100 elements), finding 5 max elements.
    Input: 100 elements, n=5
    Current Complexity: O(100*5) = O(500)
    Optimized Expected: O(100 log 5) ≈ O(233)
    Improvement: ~2.1x speedup expected
    """
    v = list(range(100))
    benchmark(Sort.max_n, v, 5)


def test_benchmark_max_n_small_n10(benchmark) -> None:
    """
    Benchmark: Small list (100 elements), finding 10 max elements.
    Input: 100 elements, n=10
    Current Complexity: O(100*10) = O(1000)
    Optimized Expected: O(100 log 10) ≈ O(333)
    Improvement: ~3x speedup expected
    """
    v = list(range(100))
    benchmark(Sort.max_n, v, 10)


def test_benchmark_max_n_small_n20(benchmark) -> None:
    """
    Benchmark: Small list (100 elements), finding 20 max elements.
    Input: 100 elements, n=20
    Current Complexity: O(100*20) = O(2000)
    Optimized Expected: O(100 log 20) ≈ O(433)
    Improvement: ~4.6x speedup expected
    """
    v = list(range(100))
    benchmark(Sort.max_n, v, 20)


# MEDIUM INPUT BENCHMARKS (1000 elements)
# Performance differences become more pronounced
# O(n*m) scalability issues start to appear with larger m values

def test_benchmark_max_n_medium_n1(benchmark) -> None:
    """
    Benchmark: Medium list (1000 elements), finding 1 max element.
    Input: 1000 elements, n=1
    Current Complexity: O(1000*1) = O(1000)
    Optimized Expected: O(1000 log 1) = O(1000)
    """
    v = list(range(1000))
    benchmark(Sort.max_n, v, 1)


def test_benchmark_max_n_medium_n10(benchmark) -> None:
    """
    Benchmark: Medium list (1000 elements), finding 10 max elements.
    Input: 1000 elements, n=10
    Current Complexity: O(1000*10) = O(10000)
    Optimized Expected: O(1000 log 10) ≈ O(3322)
    Improvement: ~3x speedup expected
    """
    v = list(range(1000))
    benchmark(Sort.max_n, v, 10)


def test_benchmark_max_n_medium_n50(benchmark) -> None:
    """
    Benchmark: Medium list (1000 elements), finding 50 max elements.
    Input: 1000 elements, n=50
    Current Complexity: O(1000*50) = O(50000)
    Optimized Expected: O(1000 log 50) ≈ O(5966)
    Improvement: ~8.4x speedup expected
    """
    v = list(range(1000))
    benchmark(Sort.max_n, v, 50)


def test_benchmark_max_n_medium_n100(benchmark) -> None:
    """
    Benchmark: Medium list (1000 elements), finding 100 max elements.
    Input: 1000 elements, n=100
    Current Complexity: O(1000*100) = O(100000)
    Optimized Expected: O(1000 log 100) ≈ O(6644)
    Improvement: ~15x speedup expected
    """
    v = list(range(1000))
    benchmark(Sort.max_n, v, 100)


# LARGE INPUT BENCHMARKS (10000 elements)
# Major performance differences should be clearly visible
# This is where heap-based optimizations provide significant benefits

def test_benchmark_max_n_large_n1(benchmark) -> None:
    """
    Benchmark: Large list (10000 elements), finding 1 max element.
    Input: 10000 elements, n=1
    Current Complexity: O(10000*1) = O(10000)
    Optimized Expected: O(10000 log 1) = O(10000)
    """
    v = list(range(10000))
    benchmark(Sort.max_n, v, 1)


def test_benchmark_max_n_large_n10(benchmark) -> None:
    """
    Benchmark: Large list (10000 elements), finding 10 max elements.
    Input: 10000 elements, n=10
    Current Complexity: O(10000*10) = O(100000)
    Optimized Expected: O(10000 log 10) ≈ O(33219)
    Improvement: ~3x speedup expected
    """
    v = list(range(10000))
    benchmark(Sort.max_n, v, 10)


def test_benchmark_max_n_large_n50(benchmark) -> None:
    """
    Benchmark: Large list (10000 elements), finding 50 max elements.
    Input: 10000 elements, n=50
    Current Complexity: O(10000*50) = O(500000)
    Optimized Expected: O(10000 log 50) ≈ O(59659)
    Improvement: ~8.4x speedup expected
    """
    v = list(range(10000))
    benchmark(Sort.max_n, v, 50)


def test_benchmark_max_n_large_n100(benchmark) -> None:
    """
    Benchmark: Large list (10000 elements), finding 100 max elements.
    Input: 10000 elements, n=100
    Current Complexity: O(10000*100) = O(1000000)
    Optimized Expected: O(10000 log 100) ≈ O(66438)
    Improvement: ~15x speedup expected
    """
    v = list(range(10000))
    benchmark(Sort.max_n, v, 100)


def test_benchmark_max_n_large_n200(benchmark) -> None:
    """
    Benchmark: Large list (10000 elements), finding 200 max elements.
    Input: 10000 elements, n=200
    Current Complexity: O(10000*200) = O(2000000)
    Optimized Expected: O(10000 log 200) ≈ O(73288)
    Improvement: ~27x speedup expected
    This demonstrates the most dramatic improvement with optimization
    """
    v = list(range(10000))
    benchmark(Sort.max_n, v, 200)


# ADDITIONAL SCALING TESTS
# These tests use unsorted random-like data to ensure complexity analysis is realistic

def test_benchmark_max_n_scaling_unsorted_1000_50(benchmark) -> None:
    """
    Benchmark: Unsorted medium list (1000 elements), finding 50 max elements.
    Input: 1000 shuffled elements, n=50
    More realistic scenario with unsorted data
    Current Complexity: O(1000*50) = O(50000)
    Optimized Expected: O(1000 log 50) ≈ O(5966)
    """
    v = list(range(500, 0, -1)) + list(range(500, 1000))
    benchmark(Sort.max_n, v, 50)


def test_benchmark_max_n_scaling_unsorted_10000_100(benchmark) -> None:
    """
    Benchmark: Unsorted large list (10000 elements), finding 100 max elements.
    Input: 10000 shuffled elements, n=100
    More realistic scenario with unsorted data
    Current Complexity: O(10000*100) = O(1000000)
    Optimized Expected: O(10000 log 100) ≈ O(66438)
    """
    v = list(range(5000, 0, -1)) + list(range(5000, 10000))
    benchmark(Sort.max_n, v, 100)
