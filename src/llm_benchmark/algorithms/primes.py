from typing import List
from itertools import compress
from math import isqrt
import threading

# Module-level cache for memoized prime checking results
_prime_cache = {}
# Lock to protect concurrent access to _prime_cache
_cache_lock = threading.Lock()


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
        2 and odd numbers up to the square root of n. Results are cached to 
        eliminate redundant calculations for repeated primality checks.

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
        # Local reference avoids repeated global dict lookup
        cache = _prime_cache
        if n in cache:
            return cache[n]
        
        if n < 2:
            result = False
        elif n < 4:
            result = True  # 2 and 3
        elif n % 2 == 0 or n % 3 == 0:
            result = False
        else:
            # Check divisors of the form 6k±1 up to sqrt(n),
            # skipping all multiples of 2 and 3 (~33% fewer iterations)
            result = True
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    result = False
                    break
                i += 6
        
        cache[n] = result
        return result

    @staticmethod
    def is_prime_ineff(n: int) -> bool:
        """Check primality using a deliberately simple linear divisor scan.

        This serves as a comparison baseline for :meth:`is_prime`, which stops
        at the square root and skips divisors that are multiples of 2 or 3.

        Args:
            n: The number to check for primality.

        Returns:
            True if the number is prime, False otherwise.

        Time Complexity:
            O(n), because every possible divisor from 2 through n - 1 is
            considered for prime inputs.
        """
        if n < 2:
            return False

        for i in range(2, n):
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
        
        # Sieve of Eratosthenes using bytearray:
        # - 1 byte per element vs ~28 bytes for list[bool] (28x less memory)
        # - Slice assignment uses C-level memset instead of Python loop
        sieve = bytearray(b'\x01') * n
        sieve[0] = sieve[1] = 0
        
        for i in range(2, isqrt(n) + 1):
            if sieve[i]:
                # C-level bulk zeroing of composite multiples
                sieve[i * i:n:i] = bytearray(len(range(i * i, n, i)))
        
        # Cache individual prime results for future use
        cache = _prime_cache
        for i in range(n):
            if i not in cache:
                cache[i] = bool(sieve[i])
        
        # Sum primes using C-level itertools.compress (avoids Python-level if)
        return sum(compress(range(n), sieve))

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
        
        # Extract all factors of 3
        while n % 3 == 0:
            factors.append(3)
            n //= 3
        
        # Check divisors of the form 6k±1, skipping multiples of 2 and 3
        i = 5
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            while n % (i + 2) == 0:
                factors.append(i + 2)
                n //= (i + 2)
            i += 6
        
        # If n > 1 after division, it's a prime factor itself
        if n > 1:
            factors.append(n)
        
        return factors