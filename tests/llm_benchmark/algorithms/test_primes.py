from threading import Event, Lock, Thread, current_thread
from typing import List

import pytest

import llm_benchmark.algorithms.primes as primes_module
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


def test_sum_primes_preserves_existing_cache_entries() -> None:
    Primes.clear_cache()
    with primes_module._cache_lock:
        primes_module._prime_cache[3] = False

    assert Primes.sum_primes(10) == 17
    assert Primes.is_prime(3) is False


def test_sum_primes_populates_cache() -> None:
    Primes.clear_cache()

    assert Primes.sum_primes(10) == 17
    assert Primes.get_cache_stats()["cache_size"] == 10
    assert Primes.is_prime(7) is True
    assert Primes.is_prime(8) is False


def test_clear_cache_invalidates_in_progress_sum_primes(monkeypatch) -> None:
    Primes.clear_cache()
    publication_ready = Event()
    resume_publication = Event()
    real_lock = Lock()
    worker = None
    worker_lock_acquisitions = 0

    class PublicationPausingLock:
        def __enter__(self):
            nonlocal worker_lock_acquisitions
            if current_thread() is worker:
                worker_lock_acquisitions += 1
                if worker_lock_acquisitions == 2:
                    publication_ready.set()
                    assert resume_publication.wait(timeout=5)
            real_lock.acquire()

        def __exit__(self, *args):
            real_lock.release()

    monkeypatch.setattr(primes_module, "_cache_lock", PublicationPausingLock())
    worker = Thread(target=Primes.sum_primes, args=(100,))
    worker.start()

    assert publication_ready.wait(timeout=5)
    Primes.clear_cache()
    resume_publication.set()
    worker.join(timeout=5)

    assert not worker.is_alive()
    assert Primes.get_cache_stats()["cache_size"] == 0


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
