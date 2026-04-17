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
        v.sort()

    @staticmethod
    def dutch_flag_partition(v: List[int], pivot_value: int) -> None:
        """Dutch flag partitioning

        Args:
            v (List[int]): List of integers
            pivot_value (int): Pivot value
        """
        smaller = 0
        equal = 0
        larger = len(v)

        while equal < larger:
            if v[equal] < pivot_value:
                v[smaller], v[equal] = v[equal], v[smaller]
                smaller += 1
                equal += 1
            elif v[equal] == pivot_value:
                equal += 1
            else:
                larger -= 1
                v[equal], v[larger] = v[larger], v[equal]

    @staticmethod
    def max_n(v: List[int], n: int) -> List[int]:
        """Find the maximum n numbers in a list

        Args:
            v (List[int]): List of integers
            n (int): Number of maximum values to find

        Returns:
            List[int]: List of maximum n values
        """
        return heapq.nlargest(n, v)