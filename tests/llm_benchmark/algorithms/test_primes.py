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


# ---------------------------------------------------------------------------
# is_prime_ineff — correctness and benchmark
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "n, expected",
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (10, False),
        (17, True),
        (26, False),
        # Larger values that exercised the old O(n × 11 000) code-path
        (97, True),
        (100, False),
        (1700, False),
        (1699, True),
    ],
)
def test_is_prime_ineff(n: int, expected: bool) -> None:
    """Verify is_prime_ineff returns correct results after optimisation."""
    assert Primes.is_prime_ineff(n) == expected


def test_benchmark_is_prime_ineff(benchmark) -> None:
    """Micro-benchmark: is_prime_ineff on a large prime (1699).

    Previously this called the O(n × 11 000) implementation; now it should
    complete in O(√n) time, making the benchmark orders of magnitude faster.
    """
    benchmark(Primes.is_prime_ineff, 1699)


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
