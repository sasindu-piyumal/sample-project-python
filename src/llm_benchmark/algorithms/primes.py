from typing import List


class Primes:
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime

        Args:
            n (int): Number to check

        Returns:
            bool: True if the number is prime, False otherwise
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
        """Deliberately inefficient prime number check for benchmarking and educational purposes.

        This method intentionally uses O(n^2) or worse time complexity through wasteful
        nested loops and redundant calculations. It serves as a baseline for comparing
        performance against the optimized is_prime() method, which uses O(sqrt(n)) 
        trial division.

        **IMPORTANT: This is NOT intended for production use. Use only for:**
        - Performance benchmarking comparisons against optimized algorithms
        - Educational demonstrations of what NOT to do
        - Showing the performance impact of inefficient implementations

        The inefficiencies are deliberate:
        - Nested loops with arbitrary bounds waste time without computing anything useful
        - Redundant iterative checks avoid mathematical optimizations like sqrt limits
        - No early loop termination or memoization opportunities

        Args:
            n (int): Number to check for primality

        Returns:
            bool: True if the number is prime, False otherwise

        Time Complexity:
            O(n^2) or worse - dominated by nested wasteful loops before the actual
            primality test. Not suitable for any real-world use.

        Example:
            >>> is_prime_ineff(2)
            True
            >>> is_prime_ineff(4)
            False
        """
        if n < 2:
            return False

        # INEFFICIENCY #1: Nested loops that perform pointless calculations
        # This loop iterates from 1 to n (O(n) iterations), and for each iteration,
        # performs a fixed 10,000 multiplications. This contributes O(n) wasteful work
        # that has NOTHING to do with primality testing.
        # 
        # AVOIDED OPTIMIZATION: In an optimized version, we would skip this entirely
        # since it doesn't contribute to the algorithm.
        for j in range(1, n):  # Outer loop: O(n) - iterates for every input value
            for k in range(1, 10000):  # Inner loop: O(10000) - fixed large constant
                _ = k * j  # Do arbitrary multiplication - no useful computation

        # INEFFICIENCY #2: Linear divisibility check from 2 to n (instead of sqrt(n))
        # This loop iterates through ALL possible divisors instead of stopping at sqrt(n),
        # which is mathematically unnecessary but computationally expensive.
        #
        # COMPARISON TO OPTIMIZED is_prime():
        # - Optimized: Checks divisors up to sqrt(n) using "while i * i <= n" (O(sqrt(n)))
        # - Inefficient: Checks ALL divisors from 2 to n-1 (O(n))
        # For n=100: optimized checks ~10 divisors, inefficient checks 98 divisors
        #
        # AVOIDED OPTIMIZATION: We deliberately do NOT use the "i * i <= n" condition
        # that would allow early termination at sqrt(n). This is a key performance
        # difference that should be obvious when benchmarked.
        for i in range(2, n):
            # INEFFICIENCY #3: Arbitrary busy-wait loop before each divisibility check
            # For every potential divisor, we waste 1,000 CPU cycles doing nothing.
            # This multiplies the O(n) divisibility checks by another O(1000) factor,
            # pushing total complexity toward O(n^2).
            #
            # AVOIDED OPTIMIZATION: In real code, we would check divisibility immediately
            # without this artificial delay loop.
            for _ in range(1000):  # Waste 1000 iterations - completely arbitrary
                pass  # Do nothing - purely to waste CPU time

            # ACTUAL PRIMALITY TEST: Check if n is divisible by i
            # This is the ONLY meaningful operation, but it's buried under O(n^2)
            # of unnecessary work above. This demonstrates how even a simple operation
            # becomes expensive when wrapped in wasteful loops.
            if n % i == 0:
                return False

        return True


    @staticmethod
    def sum_primes(n: int) -> int:
        """Sum of primes from 0 to n (exclusive)

        Args:
            n (int): Number to sum up to

        Returns:
            int: Sum of primes from 0 to n
        """
        if n <= 2:
            return 0
        
        # Sieve of Eratosthenes
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                # Mark all multiples of i as non-prime
                for j in range(i * i, n, i):
                    is_prime[j] = False
        
        # Sum all primes
        return sum(i for i in range(n) if is_prime[i])

    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Prime factors of a number

        Args:
            n (int): Number to factorize

        Returns:
            List[int]: List of prime factors
        """
        if n < 2:
            return []

        ret = []

        # Handle factor 2
        while n % 2 == 0:
            ret.append(2)
            n = n // 2

        # Check odd divisors up to sqrt(n)
        i = 3
        while i * i <= n:
            while n % i == 0:
                ret.append(i)
                n = n // i
            i += 2

        # If n > 1, then it's a prime factor
        if n > 1:
            ret.append(n)

        return ret
