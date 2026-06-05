from typing import List
from functools import lru_cache

# Module-level cache for memoized prime checking results
_prime_cache = {}

# Create an LRU cache wrapper for bounded memory usage
@lru_cache(maxsize=10000)
def _lru_is_prime_cached(n: int) -> bool:
    """LRU-cached prime check to limit memory usage."""
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
    return True


class Primes:
    """Collection of prime number algorithms including efficient and benchmark variants."""

    @staticmethod
    def clear_cache() -> None:
        """Clear the prime number cache. Useful for testing and memory management.
        
        This should be called if you need to reset the memoization cache,
        such as between test runs or when memory optimization is needed.
        """
        global _prime_cache
        _prime_cache.clear()

    @staticmethod
    def get_cache_stats() -> dict:
        """Get statistics about the prime number cache.
        
        Returns:
            dict: Dictionary with cache_size (number of cached entries) and 
                  cache_memory_estimate (approximate bytes used).
        """
        cache_size = len(_prime_cache)
        # Rough estimate: Python int ~28 bytes + bool ~28 bytes + dict overhead per entry
        cache_memory_estimate = cache_size * (28 + 28 + 50)
        return {
            "cache_size": cache_size,
            "cache_memory_estimate": cache_memory_estimate
        }

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime using trial division with caching.

        Uses an optimized O(sqrt(n)) algorithm that checks divisibility only by
        2 and odd numbers up to the square root of n. Results are cached with
        an LRU strategy to limit memory usage while maintaining performance.

        Args:
            n: The number to check for primality.

        Returns:
            True if the number is prime, False otherwise.

        Examples:
            >>> Primes.is_prime(2)
            True
            >>> Primes.is_prime(17)
            True
            >>> Primes.is_prime(4)
            False
        """
        # Use LRU cache with bounded size (maxsize=10000)
        return _lru_is_prime_cached(n)

    @staticmethod
    def is_prime_ineff(n: int) -> bool:
        """Deliberately inefficient prime check for benchmarking and education.

        **WARNING: NOT FOR PRODUCTION USE**

        This method intentionally uses O(n^2) time complexity through wasteful
        nested loops and redundant calculations. It serves as a baseline for
        performance comparisons against the optimized is_prime() method.

        **Use cases:**
        - Performance benchmarking vs optimized algorithms
        - Educational demonstrations of anti-patterns
        - Showing the impact of inefficient implementations

        **Deliberate inefficiencies:**
        1. Nested loops performing O(n * 10000) pointless multiplications
        2. Linear divisibility check O(n) instead of O(sqrt(n))
        3. Busy-wait loop adding O(1000) overhead per divisibility check

        Args:
            n: The number to check for primality.

        Returns:
            True if the number is prime, False otherwise.

        Time Complexity:
            O(n^2) - Dominated by nested wasteful loops. The actual primality
            test is buried under layers of unnecessary computation.

        Examples:
            >>> Primes.is_prime_ineff(2)
            True
            >>> Primes.is_prime_ineff(4)
            False
        """
        if n < 2:
            return False

        # INEFFICIENCY #1: Nested loops with pointless calculations O(n * 10000)
        # Wastes CPU cycles on multiplications unrelated to primality testing.
        # AVOIDED: Skipping this entirely (as done in is_prime).
        for j in range(1, n):
            for k in range(1, 10000):
                _ = k * j  # Arbitrary multiplication with no purpose

        # INEFFICIENCY #2: Linear divisibility check O(n) instead of O(sqrt(n))
        # Checks ALL divisors from 2 to n-1 instead of stopping at sqrt(n).
        # 
        # Comparison to is_prime():
        # - Optimized: "i * i <= n" stops at sqrt(n) → O(sqrt(n))
        # - Inefficient: "range(2, n)" checks all → O(n)
        # 
        # For n=100: optimized checks ~10 divisors, this checks 98 divisors.
        # AVOIDED: Using "i * i <= n" termination condition.
        for i in range(2, n):
            # INEFFICIENCY #3: Busy-wait loop O(1000) before each check
            # Wastes 1000 iterations doing nothing, multiplying the O(n)
            # divisibility checks by O(1000), pushing toward O(n^2).
            # AVOIDED: Immediate divisibility checking without delays.
            for _ in range(1000):
                pass  # Pure time waste

            # The ONLY useful operation: actual primality test
            if n % i == 0:
                return False

        return True


    @staticmethod
    def sum_primes(n: int) -> int:
        """Calculate the sum of all prime numbers less than n.

        Uses the Sieve of Eratosthenes algorithm for efficient prime generation
        with O(n log log n) time complexity and O(n) space complexity.
        Caches individual prime results to improve performance for overlapping ranges.

        Args:
            n: The upper bound (exclusive) for prime summation.

        Returns:
            The sum of all prime numbers in the range [0, n).

        Examples:
            >>> Primes.sum_primes(10)
            17  # 2 + 3 + 5 + 7
            >>> Primes.sum_primes(2)
            0
        """
        if n <= 2:
            return 0
        
        # Sieve of Eratosthenes: mark composite numbers
        is_prime_arr = [True] * n
        is_prime_arr[0] = is_prime_arr[1] = False
        
        # Only need to check up to sqrt(n)
        sqrt_n = int(n ** 0.5)
        for i in range(2, sqrt_n + 1):
            if is_prime_arr[i]:
                # Mark all multiples of i starting from i^2 as composite
                for j in range(i * i, n, i):
                    is_prime_arr[j] = False
        
        # Cache individual prime results for future use
        for i in range(n):
            if i not in _prime_cache:
                _prime_cache[i] = is_prime_arr[i]
        
        # Sum all remaining prime numbers
        return sum(i for i in range(n) if is_prime_arr[i])

    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Compute the prime factorization of a number.

        Returns all prime factors (with repetition) in ascending order.
        Uses trial division with O(sqrt(n)) time complexity.

        Args:
            n: The number to factorize (must be positive).

        Returns:
            A list of prime factors in ascending order. Returns an empty list
            for n <= 1.

        Examples:
            >>> Primes.prime_factors(12)
            [2, 2, 3]
            >>> Primes.prime_factors(17)
            [17]
            >>> Primes.prime_factors(1)
            []
        """
        if n <= 1:
            return []
        
        factors = []
        
        # Extract all factors of 2
        while n % 2 == 0:
            factors.append(2)
            n //= 2
        
        # Check odd divisors starting from 3 up to sqrt(n)
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 2
        
        # If n > 1 after division, it's a prime factor itself
        if n > 1:
            factors.append(n)
        
        return factors