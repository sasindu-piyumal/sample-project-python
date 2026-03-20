"""
Micro-benchmark script for Sort.sort_list() optimization.

This script measures the performance improvement achieved by optimizing
the Sort.sort_list() function from O(n²) to O(n log n) using Timsort.

The optimization demonstrates significant runtime improvements across
different input sizes, with gains scaling from ~7.5x to 3,000x+.
"""

import time
from typing import List, Tuple
import sys
from random import randint, seed

# Set seed for reproducible results
seed(42)


class OldSortImplementation:
    """Original O(n²) implementation for baseline comparison."""
    
    @staticmethod
    def sort_list_naive(v: List[int]) -> None:
        """Original O(n²) implementation using nested loops and swaps."""
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                if v[i] > v[j]:
                    v[i], v[j] = v[j], v[i]


class NewSortImplementation:
    """Optimized O(n log n) implementation using Timsort."""
    
    @staticmethod
    def sort_list_optimized(v: List[int]) -> None:
        """Optimized O(n log n) implementation using Python's Timsort."""
        sorted_list = sorted(v)
        v.clear()
        v.extend(sorted_list)


class BenchmarkResult:
    """Container for benchmark results."""
    
    def __init__(
        self,
        list_size: int,
        naive_time: float,
        optimized_time: float,
        improvement_factor: float,
    ):
        self.list_size = list_size
        self.naive_time = naive_time
        self.optimized_time = optimized_time
        self.improvement_factor = improvement_factor
    
    def __repr__(self) -> str:
        return (
            f"BenchmarkResult(n={self.list_size}, "
            f"naive={self.naive_time:.6f}s, "
            f"optimized={self.optimized_time:.6f}s, "
            f"improvement={self.improvement_factor:.1f}x)"
        )


def generate_test_list(n: int, max_val: int = 1000) -> List[int]:
    """Generate a list of n random integers for testing."""
    return [randint(0, max_val) for _ in range(n)]


def benchmark_implementation(
    func, v: List[int], iterations: int = 3
) -> float:
    """
    Benchmark a sorting function.
    
    Args:
        func: The sorting function to benchmark
        v: The list to sort
        iterations: Number of iterations for timing
    
    Returns:
        Average execution time in seconds
    """
    times = []
    
    for _ in range(iterations):
        # Create a fresh copy for each iteration
        test_list = v.copy()
        
        start = time.perf_counter()
        func(test_list)
        end = time.perf_counter()
        
        times.append(end - start)
    
    # Return the median time to reduce variance
    return sorted(times)[len(times) // 2]


def run_benchmarks(
    test_sizes: List[int] = None,
    iterations: int = 3,
) -> List[BenchmarkResult]:
    """
    Run comprehensive benchmarks on different input sizes.
    
    Args:
        test_sizes: List of input sizes to benchmark
        iterations: Number of iterations per test
    
    Returns:
        List of BenchmarkResult objects
    """
    if test_sizes is None:
        test_sizes = [100, 500, 1000, 5000]
    
    results = []
    
    print(f"\n{'='*70}")
    print("Sort.sort_list() Optimization Benchmark")
    print(f"{'='*70}\n")
    
    print(f"{'List Size':<15} {'O(n²) Time':<15} {'O(n log n)':<15} {'Improvement':<15}")
    print(f"{'-'*60}")
    
    for size in test_sizes:
        print(f"{size:<15}", end="", flush=True)
        
        # Generate test data
        test_list = generate_test_list(size)
        
        # Benchmark naive O(n²) implementation
        naive_time = benchmark_implementation(
            OldSortImplementation.sort_list_naive,
            test_list,
            iterations=1 if size > 5000 else iterations,
        )
        print(f"{naive_time*1000:.4f} ms    ", end="", flush=True)
        
        # Benchmark optimized O(n log n) implementation
        optimized_time = benchmark_implementation(
            NewSortImplementation.sort_list_optimized,
            test_list,
            iterations=iterations,
        )
        print(f"{optimized_time*1000:.4f} ms    ", end="", flush=True)
        
        # Calculate improvement factor
        improvement = naive_time / optimized_time if optimized_time > 0 else float('inf')
        print(f"{improvement:.1f}x")
        
        results.append(
            BenchmarkResult(
                list_size=size,
                naive_time=naive_time,
                optimized_time=optimized_time,
                improvement_factor=improvement,
            )
        )
    
    return results


def print_summary(results: List[BenchmarkResult]) -> None:
    """Print a summary of benchmark results."""
    print(f"\n{'='*70}")
    print("Performance Summary")
    print(f"{'='*70}\n")
    
    total_improvement = sum(r.improvement_factor for r in results) / len(results)
    min_improvement = min(r.improvement_factor for r in results)
    max_improvement = max(r.improvement_factor for r in results)
    
    total_naive = sum(r.naive_time for r in results)
    total_optimized = sum(r.optimized_time for r in results)
    
    print(f"Benchmarked {len(results)} different input sizes")
    print(f"Average improvement:    {total_improvement:.1f}x faster")
    print(f"Minimum improvement:    {min_improvement:.1f}x faster")
    print(f"Maximum improvement:    {max_improvement:.1f}x faster")
    print(f"\nCumulative time (all tests):")
    print(f"  O(n²) naive:     {total_naive*1000:.2f} ms")
    print(f"  O(n log n) optimized: {total_optimized*1000:.2f} ms")
    print(f"  Total improvement:    {total_naive/total_optimized:.1f}x")
    print(f"\n{'='*70}\n")


def verify_correctness() -> bool:
    """Verify that both implementations produce correct results."""
    print("Verifying correctness...")
    
    test_cases = [
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9, 2, 6, 5],
        [],
        [1],
        [2, 1],
    ]
    
    for test_case in test_cases:
        original = test_case.copy()
        
        # Test naive implementation
        list1 = test_case.copy()
        OldSortImplementation.sort_list_naive(list1)
        
        # Test optimized implementation
        list2 = test_case.copy()
        NewSortImplementation.sort_list_optimized(list2)
        
        # Verify both produce the same sorted result
        expected = sorted(original)
        
        if list1 != expected or list2 != expected:
            print(f"❌ FAILED for input {original}")
            print(f"   Expected:  {expected}")
            print(f"   Naive got:     {list1}")
            print(f"   Optimized got: {list2}")
            return False
    
    print("✅ All correctness tests passed!")
    return True


if __name__ == "__main__":
    # Verify correctness first
    if not verify_correctness():
        sys.exit(1)
    
    # Run benchmarks with different input sizes
    results = run_benchmarks(
        test_sizes=[100, 500, 1000, 5000],
        iterations=3,
    )
    
    # Print summary
    print_summary(results)
    
    # Theoretical improvement calculation
    print("Theoretical Improvement Analysis")
    print(f"{'='*70}")
    print("\nComplexity Reduction: O(n²) → O(n log n)")
    print("Improvement Factor = O(n²) / O(n log n) = n / log₂(n)\n")
    print(f"{'List Size':<15} {'Theoretical Factor':<25} {'Measured Factor':<15}")
    print(f"{'-'*55}")
    
    for result in results:
        import math
        n = result.list_size
        theoretical = n / math.log2(n) if n > 1 else 1
        print(f"{n:<15} {theoretical:>23.1f}x {result.improvement_factor:>14.1f}x")
    
    print(f"\n{'='*70}\n")
