import math
from typing import List


class Primes:
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime.

        Uses trial division up to √n, handling 2 and odd numbers separately
        so the hot loop only tests odd candidates — roughly half as many
        divisions as a naïve 2-to-n scan.

        Complexity: O(√n)   (was O(n))

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
        # Only test odd divisors from 3 up to √n.
        # math.isqrt is available from Python 3.8 and avoids floating-point
        # rounding issues that can affect int(math.sqrt(n)).
        limit = math.isqrt(n)
        i = 3
        while i <= limit:
            if n % i == 0:
                return False
            i += 2
        return True

    @staticmethod
    def is_prime_ineff(n: int) -> bool:
        """Check if a number is prime.

        Formerly an intentionally slow implementation that executed
        O(n × 10 000 + n × 1 000) wasted operations before even starting
        the divisibility loop.  Replaced with the same O(√n) trial-division
        algorithm used by :meth:`is_prime` so the two methods share a single
        efficient code-path and callers need not be changed.

        Optimisations applied
        ─────────────────────
        * Early-exit for n < 2 and for even n > 2.
        * Trial divisors are restricted to odd numbers starting at 3,
          halving the number of modulo operations.
        * The loop ceiling is math.isqrt(n) (integer square root, O(1),
          no floating-point error) instead of n, cutting the work from
          O(n) to O(√n).
        * math.isqrt is computed once outside the loop to avoid repeated
          calls inside the hot path.

        Hardware note: on x86-64 the integer modulo (%) maps to a single
        IDIV instruction; keeping operands small (≤ √n) maximises the
        chance that both dividend and divisor fit in CPU registers and
        avoids expensive memory traffic for large n.

        Complexity: O(√n)   (was O(n × 11 000))

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
        limit = math.isqrt(n)
        i = 3
        while i <= limit:
            if n % i == 0:
                return False
            i += 2
        return True

    @staticmethod
    def sum_primes(n: int) -> int:
        """Sum of primes from 0 to n (exclusive)

        Args:
            n (int): Number to sum up to

        Returns:
            int: Sum of primes from 0 to n
        """
        sum_ = 0
        for i in range(n):
            if Primes.is_prime(i):
                sum_ += i
        return sum_

    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Prime factors of a number.

        Divides out 2 first, then tests only odd candidates up to √n,
        reducing the work from O(n) per call to O(√n).

        Args:
            n (int): Number to factorize

        Returns:
            List[int]: List of prime factors
        """
        ret = []
        # Divide out all factors of 2 first.
        while n > 1 and n % 2 == 0:
            ret.append(2)
            n //= 2
        # Now n is odd; only odd divisors can remain.
        i = 3
        while i * i <= n:
            while n % i == 0:
                ret.append(i)
                n //= i
            i += 2
        if n > 1:
            ret.append(n)
        return ret
