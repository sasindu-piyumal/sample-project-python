#!/usr/bin/env python3
"""Micro-benchmark for DsList: optimised vs naïve implementations.

Run directly:
    python benchmarks/micro_benchmark_dslist.py

Or via Poetry:
    poetry run python benchmarks/micro_benchmark_dslist.py

The script compares the current (optimised) implementation against the
original naïve loop-with-append pattern for five DsList methods.  It uses
only the standard library (``timeit``) so no extra dependencies are needed.

Hardware notes
--------------
* The optimised versions delegate work to CPython's C runtime, reducing
  Python bytecode dispatch to nearly zero.  On any x86-64 CPU the slice and
  list-concatenation paths benefit from hardware prefetching because they
  access memory sequentially.
* ``list.__add__`` and slicing allocate a single contiguous block up-front;
  the naïve ``append`` path may trigger multiple ``realloc`` calls as the
  list grows, hurting cache efficiency.
* Results are printed as mean ± std-dev in microseconds so they can be
  compared across different runner specs without needing pytest-benchmark.
"""

from __future__ import annotations

import statistics
import timeit
from typing import Callable, List

# ---------------------------------------------------------------------------
# Naïve (original) implementations
# ---------------------------------------------------------------------------


def _modify_list_naive(v: List[int]) -> List[int]:
    ret = []
    for i in range(len(v)):
        ret.append(v[i] + 1)
    return ret


def _search_list_naive(v: List[int], n: int) -> List[int]:
    ret = []
    for i in range(len(v)):
        if v[i] == n:
            ret.append(i)
    return ret


def _reverse_list_naive(v: List[int]) -> List[int]:
    ret = []
    for i in range(len(v)):
        ret.append(v[len(v) - 1 - i])
    return ret


def _rotate_list_naive(v: List[int], n: int) -> List[int]:
    if not v:
        return []
    n = n % len(v)
    ret = []
    for i in range(n, len(v)):
        ret.append(v[i])
    for i in range(n):
        ret.append(v[i])
    return ret


def _merge_lists_naive(v1: List[int], v2: List[int]) -> List[int]:
    ret = []
    for i in range(len(v1)):
        ret.append(v1[i])
    for i in range(len(v2)):
        ret.append(v2[i])
    return ret


# ---------------------------------------------------------------------------
# Optimised implementations (mirror of dslist.py)
# ---------------------------------------------------------------------------


def _modify_list_opt(v: List[int]) -> List[int]:
    return [x + 1 for x in v]


def _search_list_opt(v: List[int], n: int) -> List[int]:
    return [i for i, x in enumerate(v) if x == n]


def _reverse_list_opt(v: List[int]) -> List[int]:
    return v[::-1]


def _rotate_list_opt(v: List[int], n: int) -> List[int]:
    if not v:
        return []
    n = n % len(v)
    return v[n:] + v[:n]


def _merge_lists_opt(v1: List[int], v2: List[int]) -> List[int]:
    return v1 + v2


# ---------------------------------------------------------------------------
# Benchmark harness
# ---------------------------------------------------------------------------

REPEAT = 7          # independent timing runs
NUMBER = 100_000    # iterations per run


def _measure(fn: Callable, *args, repeat: int = REPEAT, number: int = NUMBER) -> tuple[float, float]:
    """Return (mean_us, stdev_us) for *fn* called with *args*."""
    times = timeit.repeat(
        lambda: fn(*args),
        repeat=repeat,
        number=number,
    )
    mean_s = statistics.mean(times) / number
    stdev_s = statistics.stdev(times) / number
    return mean_s * 1e6, stdev_s * 1e6


def _speedup(naive_mean: float, opt_mean: float) -> str:
    if opt_mean == 0:
        return "∞"
    return f"{naive_mean / opt_mean:.2f}×"


def _run_benchmark(
    name: str,
    naive_fn: Callable,
    opt_fn: Callable,
    *args,
) -> None:
    naive_mean, naive_sd = _measure(naive_fn, *args)
    opt_mean, opt_sd = _measure(opt_fn, *args)
    speedup = _speedup(naive_mean, opt_mean)

    print(f"\n{'─' * 60}")
    print(f"  {name}")
    print(f"{'─' * 60}")
    print(f"  Naïve   : {naive_mean:8.3f} µs  ± {naive_sd:.3f} µs")
    print(f"  Optimised: {opt_mean:8.3f} µs  ± {opt_sd:.3f} µs")
    print(f"  Speed-up : {speedup}")


# ---------------------------------------------------------------------------
# Input data for each benchmark size
# ---------------------------------------------------------------------------

SIZES = [10, 100, 1_000, 10_000]


def main() -> None:
    import sys
    import platform

    print("=" * 60)
    print("  DsList micro-benchmark")
    print("=" * 60)
    print(f"  Python   : {sys.version.split()[0]}")
    print(f"  Platform : {platform.machine()} / {platform.system()}")
    print(f"  Runs     : {REPEAT} × {NUMBER:,} iterations per function/size")

    for size in SIZES:
        data = list(range(size, 0, -1))   # worst-case reversed input
        half = size // 2
        data2 = list(range(half))         # second list for merge

        print(f"\n{'━' * 60}")
        print(f"  Input size: n = {size:,}")
        print(f"{'━' * 60}")

        _run_benchmark(
            "modify_list  (loop+append  vs  list comprehension)",
            _modify_list_naive,
            _modify_list_opt,
            data,
        )
        _run_benchmark(
            "search_list  (loop+append  vs  enumerate comprehension)",
            _search_list_naive,
            _search_list_opt,
            data,
            half,
        )
        _run_benchmark(
            "reverse_list (loop+append  vs  v[::-1])",
            _reverse_list_naive,
            _reverse_list_opt,
            data,
        )
        _run_benchmark(
            "rotate_list  (two loops    vs  slice concat)",
            _rotate_list_naive,
            _rotate_list_opt,
            data,
            size // 3,
        )
        _run_benchmark(
            "merge_lists  (two loops    vs  v1 + v2)",
            _merge_lists_naive,
            _merge_lists_opt,
            data,
            data2,
        )

    print(f"\n{'=' * 60}")
    print("  Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
