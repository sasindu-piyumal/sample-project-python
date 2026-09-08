from collections import Counter
from typing import List, Tuple

import pytest

from llm_benchmark.algorithms.sort import Sort


def test_sort_list_sorts_in_place() -> None:
    values = [5, -1, 3, 3, 0, -7]
    original = values

    result = Sort.sort_list(values)

    assert result is None
    assert values is original
    assert values == [-7, -1, 0, 3, 3, 5]


def test_benchmark_sort_list_reversed_input(benchmark) -> None:
    values = list(range(1_000, 0, -1))

    def sort_copy() -> None:
        Sort.sort_list(values.copy())

    benchmark(sort_copy)


def _find_partition_boundaries(arr: List[int], pivot: int) -> Tuple[int, int]:
    """Find the boundaries of the partition regions.
    
    Returns:
        Tuple of (first_equal_index, first_greater_index)
        - Elements [0, first_equal_index) are < pivot
        - Elements [first_equal_index, first_greater_index) are == pivot
        - Elements [first_greater_index, len(arr)) are > pivot
    """
    first_equal = 0
    while first_equal < len(arr) and arr[first_equal] < pivot:
        first_equal += 1
    
    first_greater = first_equal
    while first_greater < len(arr) and arr[first_greater] == pivot:
        first_greater += 1
    
    return first_equal, first_greater


@pytest.mark.parametrize(
    "values, pivot",
    [
        # Mixed values with pivot in the middle
        ([3, 1, 4, 1, 5, 9, 2, 6], 5),
        ([2, 7, 1, 8, 2, 8, 1, 8], 8),
        ([5, 2, 8, 1, 9, 3, 7, 4], 5),
        # Negative and positive values
        ([-5, 3, -2, 7, 0, -1, 4], 0),
        ([-10, -5, 0, 5, 10], 0),
        # Values spread across range
        ([10, 20, 30, 40, 50], 25),
        ([1, 100, 2, 99, 3, 98], 50),
    ],
)
def test_dutch_flag_partition_mixed_values(values, pivot):
    """Test partitioning with mixed values."""
    original_list = values
    original_multiset = Counter(values)
    
    result = Sort.dutch_flag_partition(values, pivot)
    
    # Verify return value is None
    assert result is None
    # Verify in-place mutation
    assert values is original_list
    # Verify multiset preserved
    assert Counter(values) == original_multiset
    
    # Verify partition regions
    first_equal, first_greater = _find_partition_boundaries(values, pivot)
    
    # Check all elements < pivot are in left region
    for i in range(first_equal):
        assert values[i] < pivot
    
    # Check all elements == pivot are in middle region
    for i in range(first_equal, first_greater):
        assert values[i] == pivot
    
    # Check all elements > pivot are in right region
    for i in range(first_greater, len(values)):
        assert values[i] > pivot


@pytest.mark.parametrize(
    "values, pivot",
    [
        # All duplicates of pivot
        ([5, 5, 5, 5], 5),
        ([1, 1, 1], 1),
        # Multiple duplicates mixed
        ([1, 2, 1, 2, 1, 2], 1),
        ([3, 3, 5, 5, 3, 5], 3),
        ([4, 2, 4, 2, 4, 2], 4),
        # Many duplicates with single unique values
        ([7, 7, 7, 7, 7, 9, 3], 7),
        ([1, 1, 1, 2, 1, 1, 1], 1),
    ],
)
def test_dutch_flag_partition_duplicates(values, pivot):
    """Test partitioning with duplicate values."""
    original_list = values
    original_multiset = Counter(values)
    
    result = Sort.dutch_flag_partition(values, pivot)
    
    assert result is None
    assert values is original_list
    assert Counter(values) == original_multiset
    
    first_equal, first_greater = _find_partition_boundaries(values, pivot)
    
    for i in range(first_equal):
        assert values[i] < pivot
    for i in range(first_equal, first_greater):
        assert values[i] == pivot
    for i in range(first_greater, len(values)):
        assert values[i] > pivot


@pytest.mark.parametrize(
    "values, pivot",
    [
        # Pivot smaller than all values
        ([5, 6, 7, 8, 9], 1),
        ([10, 20, 30], 0),
        # Pivot larger than all values
        ([1, 2, 3, 4], 10),
        ([0, 1, 2], 100),
        # Pivot between values but not present
        ([1, 3, 5, 7, 9], 4),
        ([10, 20, 30, 40], 25),
        ([-10, -5, 5, 10], 0),
    ],
)
def test_dutch_flag_partition_absent_pivot(values, pivot):
    """Test partitioning when pivot is not in the list."""
    original_list = values
    original_multiset = Counter(values)
    
    result = Sort.dutch_flag_partition(values, pivot)
    
    assert result is None
    assert values is original_list
    assert Counter(values) == original_multiset
    
    first_equal, first_greater = _find_partition_boundaries(values, pivot)
    
    # When pivot is absent, equal region should be empty
    assert first_equal == first_greater
    
    for i in range(first_equal):
        assert values[i] < pivot
    for i in range(first_greater, len(values)):
        assert values[i] > pivot


@pytest.mark.parametrize(
    "values, pivot",
    [
        # All values equal to pivot
        ([5, 5, 5, 5, 5], 5),
        ([0, 0, 0], 0),
        ([1], 1),
        ([-3, -3, -3, -3], -3),
        # Large array of equal values
        ([42] * 10, 42),
    ],
)
def test_dutch_flag_partition_all_equal(values, pivot):
    """Test partitioning when all values equal the pivot."""
    original_list = values
    original_multiset = Counter(values)
    
    result = Sort.dutch_flag_partition(values, pivot)
    
    assert result is None
    assert values is original_list
    assert Counter(values) == original_multiset
    
    first_equal, first_greater = _find_partition_boundaries(values, pivot)
    
    # Left region should be empty
    assert first_equal == 0
    # Right region should be empty
    assert first_greater == len(values)
    
    # All elements should be in middle region
    for elem in values:
        assert elem == pivot


@pytest.mark.parametrize(
    "values, pivot",
    [
        # Empty list
        ([], 5),
        ([], 0),
        ([], -1),
        # Single element equal to pivot
        ([5], 5),
        ([0], 0),
        # Single element less than pivot
        ([3], 5),
        ([0], 10),
        # Single element greater than pivot
        ([7], 5),
        ([100], 1),
        # Two elements
        ([1, 2], 1),
        ([1, 2], 2),
        ([2, 1], 1),
        ([1, 1], 1),
    ],
)
def test_dutch_flag_partition_empty_and_singleton(values, pivot):
    """Test partitioning with empty or singleton lists."""
    original_list = values
    original_multiset = Counter(values)
    
    result = Sort.dutch_flag_partition(values, pivot)
    
    assert result is None
    assert values is original_list
    assert Counter(values) == original_multiset
    
    if len(values) > 0:
        first_equal, first_greater = _find_partition_boundaries(values, pivot)
        
        for i in range(first_equal):
            assert values[i] < pivot
        for i in range(first_equal, first_greater):
            assert values[i] == pivot
        for i in range(first_greater, len(values)):
            assert values[i] > pivot


class TestDutchFlagPartitionInPlace:
    """Tests verifying in-place mutation and return behavior."""

    def test_returns_none(self):
        """Dutch flag partition returns None."""
        values = [3, 1, 4, 1, 5]
        result = Sort.dutch_flag_partition(values, 3)
        assert result is None

    def test_mutates_same_list_object(self):
        """Dutch flag partition mutates the same list object."""
        values = [5, 2, 8, 1, 9]
        original_id = id(values)
        Sort.dutch_flag_partition(values, 5)
        assert id(values) == original_id

    def test_mutates_same_list_empty(self):
        """Dutch flag partition mutates same object even for empty list."""
        values = []
        original_id = id(values)
        Sort.dutch_flag_partition(values, 5)
        assert id(values) == original_id

    def test_original_reference_is_valid(self):
        """Original reference to list remains valid after partition."""
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        original_ref = values
        Sort.dutch_flag_partition(values, 5)
        # Can access via original reference
        assert len(original_ref) == 8


class TestDutchFlagPartitionMultisetPreservation:
    """Tests verifying multiset (element counts) is preserved."""

    def test_multiset_preserved_mixed(self):
        """Multiset preserved with mixed values."""
        values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        original_counts = Counter(values)
        Sort.dutch_flag_partition(values, 5)
        assert Counter(values) == original_counts

    def test_multiset_preserved_all_duplicates(self):
        """Multiset preserved when all values are duplicates."""
        values = [2, 2, 2, 2, 2]
        original_counts = Counter(values)
        Sort.dutch_flag_partition(values, 2)
        assert Counter(values) == original_counts

    def test_multiset_preserved_sparse(self):
        """Multiset preserved with widely spaced values."""
        values = [1, 100, 2, 99, 3, 98, 4, 97, 5]
        original_counts = Counter(values)
        Sort.dutch_flag_partition(values, 50)
        assert Counter(values) == original_counts

    def test_multiset_preserved_negative(self):
        """Multiset preserved with negative values."""
        values = [-10, -5, -5, 0, 5, 5, 10]
        original_counts = Counter(values)
        Sort.dutch_flag_partition(values, 0)
        assert Counter(values) == original_counts


class TestDutchFlagPartitionPartitionValidation:
    """Tests verifying correct partition region formation."""

    def test_partition_regions_no_mixing(self):
        """Elements in each region satisfy their constraints."""
        values = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0]
        pivot = 5
        Sort.dutch_flag_partition(values, pivot)
        
        first_equal, first_greater = _find_partition_boundaries(values, pivot)
        
        # No element < pivot should be in equal region
        for i in range(first_equal, first_greater):
            assert values[i] == pivot
        
        # No element > pivot should be in less-than region
        for i in range(first_equal):
            assert values[i] < pivot

    def test_partition_contiguous_less(self):
        """All less-than elements are contiguous."""
        values = [10, 3, 8, 2, 9, 1, 7, 4, 6, 5]
        pivot = 6
        Sort.dutch_flag_partition(values, pivot)
        
        first_equal, _ = _find_partition_boundaries(values, pivot)
        
        # All less-than elements should be before first_equal
        less_count = sum(1 for v in values if v < pivot)
        assert first_equal == less_count

    def test_partition_contiguous_equal(self):
        """All equal elements are contiguous."""
        values = [3, 5, 3, 5, 3, 5, 3, 5, 1, 7]
        pivot = 5
        Sort.dutch_flag_partition(values, pivot)
        
        first_equal, first_greater = _find_partition_boundaries(values, pivot)
        
        # All equal elements should be between boundaries
        equal_count = sum(1 for v in values if v == pivot)
        assert first_greater - first_equal == equal_count

    def test_partition_contiguous_greater(self):
        """All greater-than elements are contiguous."""
        values = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0]
        pivot = 4
        Sort.dutch_flag_partition(values, pivot)
        
        _, first_greater = _find_partition_boundaries(values, pivot)
        
        # All greater-than elements should be from first_greater onward
        greater_count = sum(1 for v in values if v > pivot)
        assert len(values) - first_greater == greater_count

    def test_partition_no_element_misplacement(self):
        """No element is in wrong region."""
        values = [7, 2, 8, 1, 9, 3, 6, 4, 5, 0]
        pivot = 5
        Sort.dutch_flag_partition(values, pivot)
        
        first_equal, first_greater = _find_partition_boundaries(values, pivot)
        
        # Check every element is in correct region
        for i in range(len(values)):
            if i < first_equal:
                assert values[i] < pivot
            elif i < first_greater:
                assert values[i] == pivot
            else:
                assert values[i] > pivot
