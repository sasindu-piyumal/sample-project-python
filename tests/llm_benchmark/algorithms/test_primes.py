from typing import List

import pytest

from llm_benchmark.algorithms.primes import Primes


@pytest.mark.parametrize(
    "n, is_prime",
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (10, False),
        (17, True),
        (26, False),
    ],
)
def test_is_prime(n: int, is_prime: bool) -> None:
    assert Primes.is_prime(n) == is_prime


def test_benchmark_is_prime(benchmark) -> None:
    benchmark(Primes.is_prime, 17)


@pytest.mark.parametrize(
    "n, S", [(0, 0), (1, 0), (2, 0), (3, 2), (4, 5), (10, 17), (100, 1060)]
)
def test_sum_primes(n: int, S: int) -> None:
    assert Primes.sum_primes(n) == S


def test_benchmark_sum_primes(benchmark) -> None:
    benchmark(Primes.sum_primes, 20)


@pytest.mark.parametrize(
    "n, factors",
    [
        (0, []),
        (1, []),
        (2, [2]),
        (3, [3]),
        (4, [2, 2]),
        (10, [2, 5]),
        (17, [17]),
        (84, [2, 2, 3, 7]),
    ],
)
def test_prime_factors(n: int, factors: List[int]) -> None:
    assert Primes.prime_factors(n) == factors


def test_benchmark_prime_factors(benchmark) -> None:
    benchmark(Primes.prime_factors, 84)


# ============================================================================
# COMPREHENSIVE EDGE CASE TESTING WITH CACHING VERIFICATION
# ============================================================================
# These tests combine expanded edge case coverage with cache correctness
# verification, creating synergistic validation that catches both boundary
# condition failures AND cache consistency issues.

class TestPrimesEdgeCasesWithCaching:
    """Comprehensive edge case tests with caching verification."""

    def setup_method(self):
        """Clear cache before each test."""
        Primes.clear_cache()

    def teardown_method(self):
        """Clear cache after each test for isolation."""
        Primes.clear_cache()

    # ========================================================================
    # EDGE CASE: Negative Numbers
    # ========================================================================
    @pytest.mark.parametrize(
        "n, is_prime",
        [
            (-1, False),
            (-2, False),
            (-17, False),
            (-100, False),
        ],
    )
    def test_is_prime_negative_numbers(self, n: int, is_prime: bool) -> None:
        """Test that negative numbers are never prime."""
        result1 = Primes.is_prime(n)
        result2 = Primes.is_prime(n)  # Cache hit
        assert result1 == is_prime
        assert result2 == is_prime
        assert result1 == result2  # Cache consistency

    # ========================================================================
    # EDGE CASE: Large Prime Numbers
    # ========================================================================
    @pytest.mark.parametrize(
        "n, is_prime",
        [
            (97, True),
            (101, True),
            (997, True),
            (1009, True),
            (1013, True),
            (10007, True),
        ],
    )
    def test_is_prime_large_primes(self, n: int, is_prime: bool) -> None:
        """Test large prime numbers for correctness and cache consistency."""
        result1 = Primes.is_prime(n)
        result2 = Primes.is_prime(n)  # Cache hit
        assert result1 == is_prime
        assert result2 == is_prime

    # ========================================================================
    # EDGE CASE: Large Composite Numbers
    # ========================================================================
    @pytest.mark.parametrize(
        "n, is_prime",
        [
            (100, False),
            (1000, False),
            (9999, False),
            (10000, False),
        ],
    )
    def test_is_prime_large_composites(self, n: int, is_prime: bool) -> None:
        """Test large composite numbers with cache verification."""
        result1 = Primes.is_prime(n)
        result2 = Primes.is_prime(n)  # Cache hit
        assert result1 == is_prime
        assert result2 == is_prime

    # ========================================================================
    # EDGE CASE: Prime Factors of Edge Cases
    # ========================================================================
    @pytest.mark.parametrize(
        "n, factors",
        [
            (-1, []),
            (1, []),
            (2, [2]),
            (10, [2, 5]),
            (100, [2, 2, 5, 5]),
            (1000, [2, 2, 2, 5, 5, 5]),
        ],
    )
    def test_prime_factors_edge_cases(self, n: int, factors: List[int]) -> None:
        """Test prime factorization edge cases with cache consistency."""
        result1 = Primes.prime_factors(n)
        result2 = Primes.prime_factors(n)  # Cache hit
        assert result1 == factors
        assert result2 == factors

    # ========================================================================
    # EDGE CASE: Sum of Primes at Boundaries
    # ========================================================================
    @pytest.mark.parametrize(
        "n, S",
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 2),
            (11, 28),
            (20, 77),
            (100, 1060),
            (200, 4227),
        ],
    )
    def test_sum_primes_edge_cases(self, n: int, S: int) -> None:
        """Test sum of primes across different ranges with cache checks."""
        result1 = Primes.sum_primes(n)
        result2 = Primes.sum_primes(n)  # Cache hit
        assert result1 == S
        assert result2 == S

    # ========================================================================
    # CACHE CONSISTENCY: Verify cache hits match fresh computation
    # ========================================================================
    def test_cache_consistency_is_prime(self) -> None:
        """Verify that cached is_prime results match fresh computation."""
        test_values = [2, 3, 5, 7, 11, 97, 100, 101, 1009]
        for n in test_values:
            Primes.clear_cache()
            result1 = Primes.is_prime(n)
            result2 = Primes.is_prime(n)  # Should hit cache
            assert result1 == result2, f"Cache mismatch for is_prime({n})"

    def test_cache_consistency_prime_factors(self) -> None:
        """Verify that cached prime_factors results match fresh computation."""
        test_values = [2, 10, 100, 84, 1000]
        for n in test_values:
            Primes.clear_cache()
            result1 = Primes.prime_factors(n)
            result2 = Primes.prime_factors(n)  # Should hit cache
            assert result1 == result2, f"Cache mismatch for prime_factors({n})"

    # ========================================================================
    # CACHE BEHAVIOR: Verify cache clear and reset
    # ========================================================================
    def test_cache_clear_resets_state(self) -> None:
        """Verify that clearing cache properly resets internal state."""
        # Populate cache
        Primes.is_prime(17)
        Primes.is_prime(19)
        stats_before = Primes.get_cache_stats()
        
        # Clear cache
        Primes.clear_cache()
        stats_after = Primes.get_cache_stats()
        
        # After clear, cache should be empty
        assert stats_after["cache_size"] == 0
        assert stats_after["cache_memory_estimate"] >= 0

    # ========================================================================
    # CACHE CONSISTENCY ACROSS RANGES: Large range caching
    # ========================================================================
    def test_large_range_cache_consistency(self) -> None:
        """Verify cache consistency across large ranges of numbers."""
        Primes.clear_cache()
        
        # Sum primes twice over a large range
        result1 = Primes.sum_primes(1000)
        result2 = Primes.sum_primes(1000)  # May hit cache
        
        assert result1 == result2
        
        # Verify cache has entries
        stats = Primes.get_cache_stats()
        assert stats["cache_size"] > 0
