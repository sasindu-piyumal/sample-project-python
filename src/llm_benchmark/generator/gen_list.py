import secrets
from typing import List


class GenList:
    @staticmethod
    def random_list(n: int, m: int) -> List[int]:
        """Generate a list of cryptographically secure random integers

        **Security Note**: This method uses the `secrets` module for
        cryptographically secure random number generation, suitable for
        security-sensitive applications like generating tokens, test data
        for security systems, or any scenario where randomness predictability
        could be exploited.

        Args:
            n (int): Number of integers to generate (must be >= 0)
            m (int): Maximum value of integers (inclusive, must be >= 0)

        Returns:
            List[int]: List of cryptographically secure random integers

        Raises:
            ValueError: If n or m is negative

        Examples:
            >>> random_nums = GenList.random_list(5, 10)
            >>> len(random_nums)
            5
            >>> all(0 <= x <= 10 for x in random_nums)
            True
        """
        if n < 0:
            raise ValueError(f"n must be non-negative, got {n}")
        if m < 0:
            raise ValueError(f"m must be non-negative, got {m}")
        
        return [secrets.randbelow(m + 1) for _ in range(n)]

    @staticmethod
    def random_matrix(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of cryptographically secure random integers

        **Security Note**: Uses cryptographically secure random number generation
        via the `secrets` module. See `random_list` documentation for details.

        Args:
            n (int): Number of rows (must be >= 0)
            m (int): Number of columns and maximum value (must be >= 0)

        Returns:
            List[List[int]]: Matrix of cryptographically secure random integers

        Raises:
            ValueError: If n or m is negative

        Examples:
            >>> matrix = GenList.random_matrix(3, 5)
            >>> len(matrix)
            3
            >>> all(len(row) == 3 for row in matrix)
            True
        """
        if n < 0:
            raise ValueError(f"n must be non-negative, got {n}")
        if m < 0:
            raise ValueError(f"m must be non-negative, got {m}")
        
        return [GenList.random_list(n, m) for _ in range(n)]
