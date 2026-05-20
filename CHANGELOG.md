# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

#### src/llm_benchmark/algorithms/primes.py

**Memoization Cache for Prime Checking**
- Added a module-level `_prime_cache` dictionary (type: `Dict[int, bool]`) to cache results of prime computations
- Modified the `is_prime()` method to check the cache before performing calculations
- Results are now cached for future lookups, improving performance on repeated prime checks of the same numbers
- Added an early `break` statement in the primality test loop to exit as soon as a divisor is found
- Updated imports to include `Dict` from typing

**Benefits:**
- Significantly reduces computation time for repeated prime checks (especially important when `sum_primes()` is called, which checks many numbers)
- Implements memoization pattern for algorithmic optimization
- Maintains backward compatibility - results remain identical, only performance improves

#### src/llm_benchmark/control/double.py

**Algorithm Optimization for count_pairs()**
- Replaced O(n²) nested loop implementation with O(n) frequency-based counting using `Counter` from collections
- The original approach iterated through the array twice, comparing each element with every other element
- New approach:
  1. Counts frequency of each unique value in one pass
  2. Iterates through frequencies to find values that appear exactly 2 times
  3. Returns the direct count (no division needed)
- Added import for `Counter` from collections module
- Updated comments to explain the optimization

**Benefits:**
- Dramatic performance improvement: O(n²) → O(n) time complexity
- More readable and maintainable code
- Correct handling of pairs: each value appearing exactly 2 times counts as 1 pair
- Maintains semantic correctness while improving efficiency

### Summary

This changeset focuses on algorithmic optimizations:
1. **Primes module**: Introduces caching to optimize repeated computations
2. **DoubleForLoop module**: Refactors count_pairs from quadratic to linear time complexity

Both changes maintain functional correctness while significantly improving performance, particularly beneficial for benchmarking scenarios where algorithms are tested repeatedly.
