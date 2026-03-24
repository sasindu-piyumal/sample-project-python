from collections import Counter
from typing import List


class DoubleForLoop:
    @staticmethod
    def sum_square(n: int) -> int:
        """Sum of squares of numbers from 0 to n (exclusive)

        Args:
            n (int): Number to sum up to

        Returns:
            int: Sum of squares of numbers from 0 to n (exclusive)
        """
        # Use mathematical formula for sum of squares: 0^2 + 1^2 + ... + (n-1)^2
        # Formula: (n-1) * n * (2*n - 1) // 6
        if n <= 0:
            return 0
        return (n - 1) * n * (2 * n - 1) // 6

    @staticmethod
    def sum_triangle(n: int) -> int:
        """Sum of triangle of numbers from 0 to n (exclusive)

        Args:
            n (int): Number to sum up to

        Returns:
            int: Sum of triangle of numbers from 0 to n (exclusive)
        """
        # Each row i contributes sum_{j=0..i} j = i*(i+1)//2.
        # Total = sum_{i=0..n-1} i*(i+1)//2 = (n-1)*n*(n+1)//6
        if n <= 0:
            return 0
        return (n - 1) * n * (n + 1) // 6

    @staticmethod
    def count_pairs(arr: List[int]) -> int:
        """Count pairs of numbers in an array

        A pair is defined as exactly two numbers in the array that are equal.

        Args:
            arr (List[int]): Array of integers

        Returns:
            int: Number of pairs in the array
        """
        # Count frequency of each element in O(N) time
        freq_map = Counter(arr)
        
        # Count elements that appear exactly twice
        count = sum(1 for freq in freq_map.values() if freq == 2)
        
        return count

    @staticmethod
    def count_duplicates(arr0: List[int], arr1: List[int]) -> int:
        """Count elements that match at the same index.

        Args:
            arr0 (List[int]): Array of integers
            arr1 (List[int]): Array of integers

        Returns:
            int: Count of elements that match at the same index
        """
        if not arr0 or not arr1:
            return 0
        # Compare element-by-element instead of using Counter
        return sum(1 for a, b in zip(arr0, arr1) if a == b)

    @staticmethod
    def sum_matrix(m: List[List[int]]) -> int:
        """Sum of matrix of integers

        Args:
            m (List[List[int]]): Matrix of integers

        Returns:
            int: Sum of matrix of integers
        """
        sum_ = 0
        for row in m:
            for val in row:
                sum_ += val
        return sum_