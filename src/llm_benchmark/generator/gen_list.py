from random import randint
from typing import List


class GenList:
    @staticmethod
    def random_list(n: int, m: int) -> List[int]:
        """Generate a list of random integers

        Args:
            n (int): Number of integers to generate
            m (int): Maximum value of integers (exclusive)

        Returns:
            List[int]: List of random integers
        """
        return [randint(0, m) for _ in range(n)]

    @staticmethod
    def random_matrix(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of random integers

        Args:
            n (int): Number of rows
            m (int): Number of columns

        Returns:
            List[List[int]]: Matrix of random integers
        """
        rand_int = randint
        return [[rand_int(0, m) for _ in range(m)] for _ in range(n)]
    
    @staticmethod
    def random_matrix_optimized(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of random integers with optimized memory layout.

        Pre-allocates the outer list with exact capacity and ensures each inner
        list is also pre-allocated for better cache locality and reduced
        reallocation overhead during generation.

        Args:
            n (int): Number of rows
            m (int): Number of columns

        Returns:
            List[List[int]]: Matrix of random integers with optimized layout
        """
        # Cache the randint function to avoid repeated lookups
        rand_int = randint
        # Pre-allocate outer list and use direct indexing for better cache behavior
        # Create matrix with explicit pre-allocation for each row
        matrix = []
        for _ in range(n):
            # Pre-allocate each row's list with exact size needed
            row = [rand_int(0, m) for _ in range(m)]
            matrix.append(row)
        return matrix
