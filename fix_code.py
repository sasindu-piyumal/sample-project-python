import os

# Content for src/llm_benchmark/control/single.py
single_py_content = """from typing import List


class SingleForLoop:
    @staticmethod
    def sum_range(n: int) -> int:
        \"\"\"Sum of numbers from 0 to n (exclusive).

        Args:
            n (int): Number to sum up to, exclusive.

        Returns:
            int: Sum of integers from 0 to n (exclusive).

        Raises:
            ValueError: If n is negative.
        \"\"\"
        if n < 0:
            raise ValueError("n must be non-negative")
        return n * (n - 1) // 2

    @staticmethod
    def max_list(v: List[int]) -> int:
        \"\"\"Maximum value in a vector.

        Args:
            v (List[int]): Vector of integers

        Returns:
            int: Maximum value in the vector

        Raises:
            ValueError: If the input vector is empty.
        \"\"\"
        if not v:
            raise ValueError("max_list() arg is an empty sequence")
        return max(v)

    @staticmethod
    def sum_modulus(n: int, m: int) -> int:
        \"\"\"Sum of multiples of m less than n (based on test expectations).

        Args:
            n (int): Upper bound (exclusive)
            m (int): Multiplier

        Returns:
            int: Sum of numbers < n that are divisible by m.

        Raises:
            ZeroDivisionError: If m == 0
        \"\"\"
        # FIX: The tests expect sum of multiples (0, m, 2m...), not sum of remainders
        return sum(i for i in range(n) if i % m == 0)
"""

# Content for src/llm_benchmark/control/double.py
double_py_content = """from collections import Counter
from typing import List


class DoubleForLoop:
    @staticmethod
    def sum_square(n: int) -> int:
        \"\"\"Sum of squares of numbers from 0 to n (exclusive)

        Args:
            n (int): Number to sum up to

        Returns:
            int: Sum of squares of numbers from 0 to n (exclusive)
        \"\"\"
        # Use mathematical formula for sum of squares: 0^2 + 1^2 + ... + (n-1)^2
        # Formula: (n-1) * n * (2*n - 1) // 6
        if n <= 0:
            return 0
        return (n - 1) * n * (2 * n - 1) // 6

    @staticmethod
    def sum_triangle(n: int) -> int:
        \"\"\"Sum of triangle of numbers from 0 to n (exclusive)

        Args:
            n (int): Number to sum up to

        Returns:
            int: Sum of triangle of numbers from 0 to n (exclusive)
        \"\"\"
        # Each row i contributes sum_{j=0..i} j = i*(i+1)//2.
        # Total = sum_{i=0..n-1} i*(i+1)//2 = (n-1)*n*(n+1)//6
        if n <= 0:
            return 0
        return (n - 1) * n * (n + 1) // 6

    @staticmethod
    def count_pairs(arr: List[int]) -> int:
        \"\"\"Count pairs of numbers in an array

        A pair is defined as exactly two numbers in the array that are equal.

        Args:
            arr (List[int]): Array of integers

        Returns:
            int: Number of pairs in the array
        \"\"\"
        # Count frequency of each element in O(N) time
        freq_map = Counter(arr)
        
        # Count elements that appear exactly twice
        count = sum(1 for freq in freq_map.values() if freq == 2)
        
        return count

    @staticmethod
    def count_duplicates(arr0: List[int], arr1: List[int]) -> int:
        \"\"\"Count elements that match at the same index.

        Args:
            arr0 (List[int]): Array of integers
            arr1 (List[int]): Array of integers

        Returns:
            int: Count of elements that match at the same index
        \"\"\"
        if not arr0 or not arr1:
            return 0
        # FIX: Compare element-by-element using zip
        return sum(1 for a, b in zip(arr0, arr1) if a == b)

    @staticmethod
    def sum_matrix(m: List[List[int]]) -> int:
        \"\"\"Sum of matrix of integers

        Args:
            m (List[List[int]]): Matrix of integers

        Returns:
            int: Sum of matrix of integers
        \"\"\"
        sum_ = 0
        for row in m:
            for val in row:
                sum_ += val
        return sum_
"""

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Fixed {path}")

if __name__ == "__main__":
    write_file("src/llm_benchmark/control/single.py", single_py_content)
    write_file("src/llm_benchmark/control/double.py", double_py_content)
    print("Code patched successfully.")
