from typing import List


class SingleForLoop:
    @staticmethod
    def sum_range(n: int) -> int:
        """Sum of integers from 0 to n-1 (exclusive of n).

        Args:
            n (int): Upper bound (exclusive).

        Returns:
            int: Sum of integers from 0 to n-1.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        return n * (n - 1) // 2

    @staticmethod
    def max_list(v: List[int]) -> int:
        """Maximum value in a vector.

        Args:
            v (List[int]): Vector of integers

        Returns:
            int: Maximum value in the vector

        Raises:
            ValueError: If the input vector is empty.
        """
        if not v:
            raise ValueError("max_list() arg is an empty sequence")
        return max(v)

    @staticmethod
    def sum_modulus(n: int, m: int) -> int:
        """Sum of all multiples of m that are less than n.

        Args:
            n (int): Number to sum up to (inclusive)
            m (int): Modulus (non-zero)

        Returns:
            int: Sum of i % m for i in [0, n]

        Raises:
            ZeroDivisionError: If m == 0
        """
        return sum(range(0, n, m))