import array as _array
from typing import List


class Primes:
    """Collection of prime number algorithms including efficient and benchmark variants."""

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime using trial division.

        Uses an optimized O(sqrt(n)) algorithm that checks divisibility only by
        2 and odd numbers up to the square root of n.

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
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        # Check odd divisors up to sqrt(n)
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

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
        for j in range(1, n):
            for k in range(1, 10000):
                _ = k * j  # Arbitrary multiplication with no purpose

        # INEFFICIENCY #2: Linear divisibility check O(n) instead of O(sqrt(n))
        for i in range(2, n):
            # INEFFICIENCY #3: Busy-wait loop O(1000) before each check
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

        # bytearray uses 1 byte per element vs ~56-byte Python bool objects in
        # a list, giving ~8x memory reduction for large n.
        is_prime = bytearray(b'\x01' * n)
        is_prime[0] = is_prime[1] = 0

        # Only need to check up to sqrt(n)
        sqrt_n = int(n ** 0.5)
        for i in range(2, sqrt_n + 1):
            if is_prime[i]:
                # Bulk-zero all multiples of i via a single C-level slice
                # assignment (equivalent to memset), avoiding a Python for-loop
                # and its per-iteration bytecode + object allocation overhead.
                is_prime[i * i::i] = bytes(len(is_prime[i * i::i]))

        # Sum all remaining prime numbers
        return sum(i for i in range(n) if is_prime[i])

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

        # array.array('l') stores C signed longs (8 bytes/element on 64-bit),
        # avoiding the ~28-byte Python int heap object overhead per factor.
        # list() converts back to a plain list so the public API is unchanged.
        factors = _array.array('l')

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

        return list(factors)
