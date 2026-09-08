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


@pytest.mark.parametrize(
    "values, n, expected",
    [
        # Mixed positive and negative with positive N
        ([5, -1, 3, -3, 0, 2], 3, [5, 3, 2]),
        ([10, -5, 20, -10, 15], 2, [20, 15]),
        ([-5, -1, -10, -3], 2, [-1, -3]),
        ([1, -1, 2, -2, 3, -3], 4, [3, 2, 1, -1]),
        # Large positive and small negative
        ([100, -50, 1, -1, 50], 3, [100, 50, 1]),
        ([-100, 100, -1, 1, -50, 50], 3, [100, 50, 1]),
    ],
)
def test_max_n_mixed_signs(values, n, expected):
    """Test max_n with mixed positive and negative values."""
    original_list = values.copy()
    
    result = Sort.max_n(values, n)
    
    # Verify result is in descending order
    assert result == expected
    assert result == sorted(result, reverse=True)
    
    # Verify source list unchanged
    assert values == original_list


@pytest.mark.parametrize(
    "values, n, expected_values",
    [
        # Duplicates of different values
        ([5, 5, 3, 3, 1, 1], 4, [5, 5, 3, 3]),
        ([2, 2, 2, 1, 1, 1], 3, [2, 2, 2]),
        ([1, 2, 1, 2, 1, 2], 4, [2, 2, 1, 1]),
        # All same value
        ([5, 5, 5, 5], 2, [5, 5]),
        ([3, 3, 3, 3, 3], 5, [3, 3, 3, 3, 3]),
        # Mix with duplicates
        ([10, 5, 10, 3, 5, 10], 3, [10, 10, 10]),
        ([7, 7, 7, 6, 6, 5], 4, [7, 7, 7, 6]),
    ],
)
def test_max_n_with_duplicates(values, n, expected_values):
    """Test max_n preserves duplicate values in result."""
    original_list = values.copy()
    
    result = Sort.max_n(values, n)
    
    # Verify result length
    assert len(result) == n
    # Verify result is in descending order
    assert result == sorted(result, reverse=True)
    # Verify duplicates preserved
    assert Counter(result) == Counter(expected_values)
    
    # Verify source list unchanged
    assert values == original_list


@pytest.mark.parametrize(
    "n",
    [0, 1, 5],
)
def test_max_n_empty_input(n):
    """Test max_n with empty input list."""
    values = []
    original_list = values.copy()
    
    result = Sort.max_n(values, n)
    
    # Empty list should return empty result
    assert result == []
    
    # Verify source list unchanged
    assert values == original_list


@pytest.mark.parametrize(
    "values, expected",
    [
        # Single element, N=0
        ([5], []),
        # Multiple elements, N=0
        ([1, 2, 3, 4, 5], []),
        # Large values, N=0
        ([100, 200, 300], []),
        # With duplicates, N=0
        ([1, 1, 1, 1], []),
    ],
)
def test_max_n_zero_n(values, expected):
    """Test max_n when N is 0."""
    original_list = values.copy()
    
    result = Sort.max_n(values, 0)
    
    assert result == expected
    assert result == []
    
    # Verify source list unchanged
    assert values == original_list


@pytest.mark.parametrize(
    "values, expected_sorted",
    [
        # N equals length
        ([5, 1, 3, 2, 4], [5, 4, 3, 2, 1]),
        ([1], [1]),
        ([3, 3, 3], [3, 3, 3]),
        ([10, -5, 0, 5, -10], [10, 5, 0, -5, -10]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
    ],
)
def test_max_n_n_equals_length(values, expected_sorted):
    """Test max_n when N equals the list length."""
    original_list = values.copy()
    
    result = Sort.max_n(values, len(values))
    
    # Result should be entire list sorted descending
    assert result == expected_sorted
    assert result == sorted(result, reverse=True)
    
    # Verify source list unchanged
    assert values == original_list


@pytest.mark.parametrize(
    "values, n",
    [
        # N greater than length
        ([1, 2, 3], 5),
        ([5], 10),
        ([1, 2], 100),
        ([10, 20, 30, 40, 50], 10),
        ([-5, 0, 5], 7),
    ],
)
def test_max_n_n_greater_than_length(values, n):
    """Test max_n when N is greater than list length."""
    original_list = values.copy()
    
    result = Sort.max_n(values, n)
    
    # Result should be entire list sorted descending
    expected_sorted = sorted(values, reverse=True)
    assert result == expected_sorted
    assert len(result) == len(values)
    
    # Verify in descending order
    assert result == sorted(result, reverse=True)
    
    # Verify source list unchanged
    assert values == original_list


class TestMaxNDescendingOrder:
    """Tests verifying returned values are in descending order."""

    def test_descending_order_mixed_values(self):
        """Result is in descending order with mixed values."""
        values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = Sort.max_n(values, 5)
        
        # Check descending order
        for i in range(len(result) - 1):
            assert result[i] >= result[i + 1]

    def test_descending_order_single_element(self):
        """Single element is trivially in descending order."""
        values = [42]
        result = Sort.max_n(values, 1)
        
        assert result == [42]

    def test_descending_order_duplicates(self):
        """Duplicates preserve descending order (non-increasing)."""
        values = [5, 5, 5, 1, 1, 1]
        result = Sort.max_n(values, 4)
        
        assert result == [5, 5, 5, 1]
        for i in range(len(result) - 1):
            assert result[i] >= result[i + 1]

    def test_descending_order_large_n(self):
        """Descending order maintained with large N values."""
        values = list(range(1, 11))
        result = Sort.max_n(values, 10)
        
        assert result == list(range(10, 0, -1))
        for i in range(len(result) - 1):
            assert result[i] > result[i + 1]

    def test_descending_order_with_negatives(self):
        """Descending order with negative values."""
        values = [-5, 10, -3, 8, 0, -1, 5]
        result = Sort.max_n(values, 4)
        
        assert result[0] == 10
        assert result[1] == 8
        assert result[2] == 5
        assert result[3] == 0
        for i in range(len(result) - 1):
            assert result[i] >= result[i + 1]

    def test_result_is_sorted_descending(self):
        """Result equals sorted(result, reverse=True)."""
        values = [7, 2, 9, 1, 5, 3, 8]
        result = Sort.max_n(values, 5)
        
        assert result == sorted(result, reverse=True)


class TestMaxNSourceListUnchanged:
    """Tests verifying the source list remains unchanged."""

    def test_source_unchanged_normal_case(self):
        """Source list unchanged after max_n call."""
        values = [5, 2, 8, 1, 9, 3, 7]
        original = values.copy()
        
        Sort.max_n(values, 3)
        
        assert values == original

    def test_source_unchanged_with_duplicates(self):
        """Source list unchanged even with duplicates."""
        values = [1, 1, 2, 2, 3, 3]
        original = values.copy()
        
        Sort.max_n(values, 4)
        
        assert values == original

    def test_source_unchanged_empty_list(self):
        """Source list (empty) unchanged."""
        values = []
        original = values.copy()
        
        Sort.max_n(values, 5)
        
        assert values == original

    def test_source_unchanged_single_element(self):
        """Source list with single element unchanged."""
        values = [42]
        original = values.copy()
        
        Sort.max_n(values, 1)
        
        assert values == original

    def test_source_unchanged_n_greater_than_length(self):
        """Source list unchanged when N > length."""
        values = [1, 2, 3]
        original = values.copy()
        
        Sort.max_n(values, 10)
        
        assert values == original

    def test_source_unchanged_negative_values(self):
        """Source list with negatives unchanged."""
        values = [-10, -5, 0, 5, 10]
        original = values.copy()
        
        Sort.max_n(values, 3)
        
        assert values == original

    def test_source_unchanged_multiple_calls(self):
        """Source list unchanged across multiple max_n calls."""
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        original = values.copy()
        
        Sort.max_n(values, 2)
        assert values == original
        
        Sort.max_n(values, 4)
        assert values == original
        
        Sort.max_n(values, 8)
        assert values == original

    def test_source_unchanged_order_preserved(self):
        """Source list maintains original order."""
        values = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0]
        original_order = values.copy()
        
        Sort.max_n(values, 5)
        
        # Order should be preserved
        assert values == original_order


class TestMaxNBoundaryAndEdgeCases:
    """Tests for boundary and edge cases."""

    def test_max_n_single_element_n_one(self):
        """Single element, N=1."""
        values = [42]
        result = Sort.max_n(values, 1)
        
        assert result == [42]

    def test_max_n_two_elements_n_one(self):
        """Two elements, N=1."""
        values = [1, 2]
        result = Sort.max_n(values, 1)
        
        assert result == [2]

    def test_max_n_two_elements_n_two(self):
        """Two elements, N=2."""
        values = [1, 2]
        result = Sort.max_n(values, 2)
        
        assert result == [2, 1]

    def test_max_n_large_array_small_n(self):
        """Large array with small N."""
        values = list(range(1, 101))
        result = Sort.max_n(values, 3)
        
        assert result == [100, 99, 98]

    def test_max_n_all_equal_values(self):
        """All elements equal, various N values."""
        values = [5, 5, 5, 5, 5]
        
        result_1 = Sort.max_n(values, 1)
        assert result_1 == [5]
        
        result_3 = Sort.max_n(values, 3)
        assert result_3 == [5, 5, 5]
        
        result_all = Sort.max_n(values, 5)
        assert result_all == [5, 5, 5, 5, 5]

    def test_max_n_zero_in_list(self):
        """List contains zero."""
        values = [-5, 0, 5, -1, 1]
        result = Sort.max_n(values, 3)
        
        assert result == [5, 1, 0]

    def test_max_n_large_range_values(self):
        """Very large range of values."""
        values = [1000000, -1000000, 0, 500000, -500000]
        result = Sort.max_n(values, 3)
        
        assert result == [1000000, 500000, 0]

    def test_max_n_alternating_signs(self):
        """Alternating positive and negative values."""
        values = [1, -1, 2, -2, 3, -3, 4, -4]
        result = Sort.max_n(values, 4)
        
        assert result == [4, 3, 2, 1]

    def test_max_n_preserves_duplicate_counts(self):
        """Returned list has correct duplicate counts."""
        values = [5, 5, 5, 3, 3, 1]
        result = Sort.max_n(values, 5)
        
        assert Counter(result) == Counter([5, 5, 5, 3, 3])

    def test_max_n_result_values_subset_of_input(self):
        """All result values come from input."""
        values = [10, 20, 30, 40, 50]
        result = Sort.max_n(values, 3)
        
        for val in result:
            assert val in values
