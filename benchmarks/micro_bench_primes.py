#!/usr/bin/env python3
"""
micro_bench_primes.py
=====================
Standalone micro-benchmark for Primes.is_prime_ineff.

This script compares the *original* O(n × 11 000) implementation against the
optimised O(√n) trial-division implementation that replaced it, so the
speedup ratio is visible without running the full pytest-benchmark suite.

Usage
-----
    python benchmarks/micro_bench_primes.py

The script uses only the standard-library ``timeit`` module — no third-party
dependencies are required.

Hardware context
----------------
The optimised implementation is tuned for general-purpose x86-64 CPUs:
  * Integer modulo (%) maps to a single IDIV instruction.  Keeping divisors
    small (≤ √n) keeps both operands in registers and avoids cache pressure.
  * Even-number short-circuit means the hot loop body is only entered for odd
    divisors, cutting the number of IDIV instructions in half.
  * math.isqrt() is computed once per call (O(1), hardware-integer precision)
    and stored in a local variable so the loop condition is a single CMP.
  * Eliminating the two previously nested busy-loops (~17 M + ~1.7 M wasted
    iterations for n = 1700) removes virtually all the runtime cost.
"""

import math
import textwrap
import timeit
from typing import Callable, Dict, List, Tuple

# ---------------------------------------------------------------------------
# Reference: original O(n × 11 000) implementation (preserved for comparison)
# ---------------------------------------------------------------------------

def _is_prime_ineff_original(n: int) -> bool:
    """Exact copy of the pre-optimisation is_prime_ineff body."""
    if n < 2:
        return False

    # Introduce unnecessary calculations
    for j in range(1, n):            # Extra loop that does nothing useful
        for k in range(1, 10000):    # Arbitrary large loop
            _ = k * j               # Pointless multiplication

    # Check divisibility by all numbers up to n
    for i in range(2, n):
        for _ in range(1000):        # Extra iterations that do nothing
            pass

        if n % i == 0:
            return False

    return True


# ---------------------------------------------------------------------------
# Optimised O(√n) implementation (mirrors primes.py)
# ---------------------------------------------------------------------------

def _is_prime_ineff_optimised(n: int) -> bool:
    """O(√n) trial-division replacement (mirrors Primes.is_prime_ineff)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = math.isqrt(n)
    i = 3
    while i <= limit:
        if n % i == 0:
            return False
        i += 2
    return True


# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

IMPLEMENTATIONS: Dict[str, Callable[[int], bool]] = {
    "original  (O(n × 11 000))": _is_prime_ineff_original,
    "optimised (O(√n))        ": _is_prime_ineff_optimised,
}

# Representative test values: (n, expected_result, label)
TEST_CASES: List[Tuple[int, bool, str]] = [
    (4,    False, "small composite (4)"),
    (17,   True,  "small prime     (17)"),
    (100,  False, "medium composite (100)"),
    (97,   True,  "medium prime     (97)"),
    (1700, False, "large composite  (1700)  ← main.py call site"),
    (1699, True,  "large prime      (1699)"),
]

# How many timeit repetitions and repeats to use per measurement.
# The original implementation is **very** slow for large n, so we use fewer
# repetitions there to avoid the benchmark itself taking minutes.
REPS_OPTIMISED = 10_000
REPS_ORIGINAL  = 1        # One call to the original at n=1700 takes ~seconds


def _measure(fn: Callable[[int], bool], n: int, reps: int, repeats: int = 5) -> float:
    """Return the *best* mean time (seconds per call) across ``repeats`` runs."""
    times = timeit.repeat(
        stmt=lambda: fn(n),
        number=reps,
        repeat=repeats,
    )
    # Best-of-N mean reduces noise from OS scheduling jitter.
    return min(times) / reps


def _fmt_time(seconds: float) -> str:
    """Human-friendly time string."""
    if seconds >= 1:
        return f"{seconds:.3f} s"
    if seconds >= 1e-3:
        return f"{seconds * 1e3:.3f} ms"
    if seconds >= 1e-6:
        return f"{seconds * 1e6:.3f} µs"
    return f"{seconds * 1e9:.3f} ns"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("  Micro-benchmark: Primes.is_prime_ineff")
    print("  Worst-ranked bottleneck — O(n × 11 000) → O(√n) trial division")
    print("=" * 70)

    # --- Correctness check --------------------------------------------------
    print("\n[1] Correctness verification")
    print("-" * 40)
    all_ok = True
    for n, expected, label in TEST_CASES:
        orig = _is_prime_ineff_original(n)
        opt  = _is_prime_ineff_optimised(n)
        status = "✓" if orig == opt == expected else "✗"
        if status == "✗":
            all_ok = False
        print(f"  {status}  n={n:5d}  expected={expected}  original={orig}  optimised={opt}  ({label})")

    if all_ok:
        print("\n  All results match. ✓")
    else:
        print("\n  MISMATCH detected — check implementation! ✗")

    # --- Timing: optimised only (all cases) ---------------------------------
    print("\n[2] Optimised O(√n) timings")
    print("-" * 40)
    opt_times: Dict[str, float] = {}
    for n, _, label in TEST_CASES:
        t = _measure(_is_prime_ineff_optimised, n, REPS_OPTIMISED)
        opt_times[label] = t
        print(f"  n={n:5d}  {_fmt_time(t):>12s} / call   ({label})")

    # --- Timing: original vs optimised for the main.py call-site (n=1700) --
    print("\n[3] Head-to-head: n=1700 (the main.py call site)")
    print("-" * 40)
    print(f"  Timing original O(n × 11 000) with {REPS_ORIGINAL} repetition(s)…")

    n_compare = 1700
    label_compare = "large composite  (1700)  ← main.py call site"

    t_orig = _measure(_is_prime_ineff_original, n_compare, REPS_ORIGINAL, repeats=1)
    t_opt  = opt_times[label_compare]

    print(f"\n  original  (O(n × 11 000)) : {_fmt_time(t_orig):>12s} / call")
    print(f"  optimised (O(√n))         : {_fmt_time(t_opt):>12s} / call")

    if t_opt > 0:
        speedup = t_orig / t_opt
        print(f"\n  Speedup: {speedup:,.0f}×")
        print(
            textwrap.fill(
                f"  At n=1700 the original implementation spent ~17 M iterations on "
                f"pointless nested multiplications and ~1.7 M no-op loop iterations "
                f"before even beginning the divisibility check.  The optimised version "
                f"performs at most ⌊√1700⌋ = {math.isqrt(n_compare)} trial divisions "
                f"(odd candidates only), achieving a {speedup:,.0f}× wall-clock speedup.",
                width=70,
                initial_indent="  ",
                subsequent_indent="  ",
            )
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
