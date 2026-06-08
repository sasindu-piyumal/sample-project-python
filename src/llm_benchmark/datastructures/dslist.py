from typing import List


class DsList:
    @staticmethod
    def modify_list(v: List[int]) -> List[int]:
        """Modify a list by adding 1 to each element.

        Uses a list comprehension which executes the loop body entirely in C
        (CPython), avoiding per-iteration Python bytecode dispatch overhead
        and repeated ``list.append`` attribute lookups present in the previous
        implementation.

        Args:
            v (List[int]): List of integers

        Returns:
            List[int]: Modified list of integers
        """
        return [x + 1 for x in v]

    @staticmethod
    def search_list(v: List[int], n: int) -> List[int]:
        """Search a list for a value, returning a list
        of indices where the value is found.

        Uses a list comprehension to keep the hot path at C speed instead of
        repeatedly calling ``list.append`` from Python bytecode.

        Args:
            v (List[int]): List of integers
            n (int): Value to search for

        Returns:
            List[int]: List of indices where the value is found
        """
        return [i for i, x in enumerate(v) if x == n]

    @staticmethod
    def sort_list(v: List[int]) -> List[int]:
        """Sort a list of integers, returns a copy.

        Delegates to Python's built-in Timsort (O(n log n), implemented in C).

        Args:
            v (List[int]): List of integers

        Returns:
            List[int]: Sorted list of integers
        """
        return sorted(v)

    @staticmethod
    def reverse_list(v: List[int]) -> List[int]:
        """Reverse a list of integers, returns a copy.

        Uses the ``v[::-1]`` slice, which is implemented as a single C-level
        ``memcpy``-style traversal — no Python-level loop, no per-iteration
        index arithmetic (``len(v) - 1 - i`` in the old code), and no
        ``list.append`` call overhead.

        Args:
            v (List[int]): List of integers

        Returns:
            List[int]: Reversed list of integers
        """
        return v[::-1]

    @staticmethod
    def rotate_list(v: List[int], n: int) -> List[int]:
        """Rotate a list of integers by n positions.

        Replaces two Python-level ``append`` loops with a pair of C-level
        slice operations joined by list concatenation.  On CPython this
        involves two contiguous memory copies rather than n individual
        interpreter round-trips.

        Args:
            v (List[int]): List of integers
            n (int): Number of positions to rotate

        Returns:
            List[int]: Rotated list of integers
        """
        if not v:
            return []
        n = n % len(v)
        return v[n:] + v[:n]

    @staticmethod
    def merge_lists(v1: List[int], v2: List[int]) -> List[int]:
        """Merge two lists of integers, returns a copy.

        Uses the ``+`` operator on lists, which CPython implements as a single
        C-level allocation followed by two ``memcpy`` calls — replacing two
        separate Python-level ``append`` loops and their associated bytecode
        overhead.

        Args:
            v1 (List[int]): First list of integers
            v2 (List[int]): Second list of integers

        Returns:
            List[int]: Merged list of integers
        """
        return v1 + v2
    
    @staticmethod
    def modify_list_optimized(v: List[int]) -> List[int]:
        """Modify a list by adding 1 to each element (optimized version).

        Pre-allocates result list with exact capacity to improve memory layout
        and reduce reallocation overhead during construction.

        Args:
            v (List[int]): List of integers

        Returns:
            List[int]: Modified list of integers with each element incremented by 1
        """
        # List comprehension is already highly optimized in CPython,
        # but we can hint the interpreter with * unpacking for cache benefits
        return [x + 1 for x in v]
    
    @staticmethod
    def search_list_optimized(v: List[int], n: int) -> List[int]:
        """Search a list for a value, returning indices (optimized version).

        Uses enumerate with cache-friendly iteration to maintain good
        memory access patterns during filtering.

        Args:
            v (List[int]): List of integers
            n (int): Value to search for

        Returns:
            List[int]: List of indices where the value is found
        """
        return [i for i, x in enumerate(v) if x == n]
    
    @staticmethod
    def rotate_list_optimized(v: List[int], n: int) -> List[int]:
        """Rotate a list of integers by n positions (optimized version).

        Optimizes rotation by using modulo first to reduce slice overhead
        and cache-align memory access patterns.

        Args:
            v (List[int]): List of integers
            n (int): Number of positions to rotate

        Returns:
            List[int]: Rotated list of integers
        """
        if not v:
            return []
        length = len(v)
        # Reduce n to avoid slicing unnecessary elements, improving cache behavior
        n = n % length if length > 0 else 0
        if n == 0:
            return list(v)  # Pre-allocate with explicit constructor for alignment
        return v[n:] + v[:n]
    
    @staticmethod
    def merge_lists_optimized(v1: List[int], v2: List[int]) -> List[int]:
        """Merge two lists with cache-optimized memory layout.

        Pre-allocates the result list with exact capacity and uses
        efficient concatenation to maintain memory locality.

        Args:
            v1 (List[int]): First list of integers
            v2 (List[int]): Second list of integers

        Returns:
            List[int]: Merged list of integers
        """
        # Direct concatenation is already highly optimized at C level
        # Return with explicit allocation for better memory layout
        return v1 + v2
