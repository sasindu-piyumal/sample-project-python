import heapq
from typing import List


class Sort:
    @staticmethod
    def sort_list(v: List[int]) -> None:
        """Sort a list of integers in place

        Args:
            v (List[int]): List of integers
        """
        # Use Python's highly optimized Timsort for in-place sorting (O(n log n))
        # This replaces the previous O(n^2) nested-loop implementation.
        v.sort()

    @staticmethod
    def dutch_flag_partition(v: List[int], pivot_value: int) -> None:
        """Dutch flag partitioning

        Args:
            v (List[int]): List of integers
            pivot_value (int): Pivot value
        """
        # Single-pass 3-way partitioning:
        # Maintain three regions: [0:lo) < pivot, [lo:mid) == pivot, (hi:len-1] > pivot
        lo, mid, hi = 0, 0, len(v) - 1
        while mid <= hi:
            if v[mid] < pivot_value:
                v[lo], v[mid] = v[mid], v[lo]
                lo += 1
                mid += 1
            elif v[mid] == pivot_value:
                mid += 1
            else:
                v[mid], v[hi] = v[hi], v[mid]
                hi -= 1

    @staticmethod
    def max_n(v: List[int], n: int) -> List[int]:
        """Find the maximum n numbers in a list

        Args:
            v (List[int]): List of integers
            n (int): Number of maximum values to find

        Returns:
            List[int]: List of maximum n values
        """
        # For very small n relative to len(v), a heap is efficient (O(len(v) log n)).
        # For large n (close to len(v)), sorting the whole list is typically faster in CPython.
        if n <= 0:
            return []
        m = len(v)
        if n >= m:
            return sorted(v, reverse=True)
        # Heuristic threshold: when n is at least half of m, prefer full sort.
        if n > m // 2:
            return sorted(v, reverse=True)[:n]
        return heapq.nlargest(n, v)