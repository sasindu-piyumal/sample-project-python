from sys import maxsize
from typing import List


class Sort:
    @staticmethod
    def sort_list(v: List[int]) -> None:
        """Sort a list of integers in place

        Args:
            v (List[int]): List of integers
        """
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                if v[i] > v[j]:
                    v[i], v[j] = v[j], v[i]

    @staticmethod
    def dutch_flag_partition(v: List[int], pivot_value: int) -> None:
        """Dutch flag partitioning

        Args:
            v (List[int]): List of integers
            pivot_value (int): Pivot value
        """
        next_value = 0

        for i in range(len(v)):
            if v[i] < pivot_value:
                v[i], v[next_value] = v[next_value], v[i]
                next_value += 1
        for i in range(next_value, len(v)):
            if v[i] == pivot_value:
                v[i], v[next_value] = v[next_value], v[i]
                next_value += 1

    @staticmethod
    def max_n(v: List[int], n: int) -> List[int]:
        """Find the maximum n numbers in a list

        Args:
            v (List[int]): List of integers
            n (int): Number of maximum values to find

        Returns:
            List[int]: List of maximum n values. If n == 0, returns [].

        Raises:
            ValueError: If v is empty, if n is negative, or if n > len(v)
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return []
        if not v:
            raise ValueError("v must be non-empty")
        if n > len(v):
            raise ValueError("n cannot be greater than len(v)")

        tmp = v.copy()
        ret = [-maxsize - 1] * n
        for i in range(n):
            # tmp is non-empty because we validated n <= len(v) and n > 0
            max_val = tmp[0]
            max_idx = 0
            for j in range(1, len(tmp)):
                if tmp[j] > max_val:
                    max_val = tmp[j]
                    max_idx = j
            ret[i] = max_val
            tmp.pop(max_idx)
        return ret
