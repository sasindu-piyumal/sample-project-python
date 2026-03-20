import heapq
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
        """Reorder values in-place as < pivot, == pivot, then > pivot.

        Args:
            v: List of integers.
            pivot_value: Pivot value.
        """
        low = 0
        mid = 0
        high = len(v) - 1

        while mid <= high:
            if v[mid] < pivot_value:
                v[low], v[mid] = v[mid], v[low]
                low += 1
                mid += 1
            elif v[mid] > pivot_value:
                v[mid], v[high] = v[high], v[mid]
                high -= 1
            else:
                mid += 1

    @staticmethod
    def max_n(v: List[int], n: int) -> List[int]:
        """Return the n largest numbers from a list.

        Args:
            v: List of integers.
            n: Number of maximum values to find.

        Returns:
            List[int]: List of maximum n values.
        """
        return heapq.nlargest(n, v)