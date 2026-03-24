from typing import List


class Primes:
    """Collection of prime number algorithms including efficient and benchmark variants."""

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime using an optimized trial division.

        Uses a 6k ± 1 stepping method to check divisibility efficiently up to
        sqrt(n).

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
        if n in (2, 3):
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        # Check candidates of the form 6k ± 1 up to sqrt(n)
        i = 5
        step = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += step
            step = 6 - step  # alternate steps to cover 6k ± 1
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
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        
        # Only need to check up to sqrt(n)
        sqrt_n = int(n ** 0.5)
        for i in range(2, sqrt_n + 1):
            if is_prime[i]:
                # Mark all multiples of i starting from i^2 as composite
                for j in range(i * i, n, i):
                    is_prime[j] = False
        
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