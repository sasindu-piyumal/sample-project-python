"""
Unit test for the count_duplicates bug fix.

This test demonstrates a bug in the test_double.py test suite where
the expected value for test case ([1, 2, 3], [2, 3, 1], 0) was incorrect.

The arrays [1, 2, 3] and [2, 3, 1] contain the same elements (1, 2, 3),
so the count of common elements with multiplicity should be 3, not 0.

This test would FAIL before the bug fix (when the expected value was 0)
and PASS after the bug fix (when the expected value is 3).
"""

import pytest
from llm_benchmark.control.double import DoubleForLoop


@pytest.mark.parametrize(
    "arr0, arr1, expected_count",
    [
        # Same elements in different order should have count = 3
        ([1, 2, 3], [2, 3, 1], 3),
        # Empty array intersection should have count = 0
        ([1, 2, 3], [4, 5, 6], 0),
        # Partial intersection
        ([1, 2, 3], [3, 4, 5], 1),
        # With duplicates
        ([1, 1, 2], [1, 2, 2], 2),  # min(2,1) + min(1,2) = 1 + 1 = 2
    ],
)
def test_count_duplicates_with_different_orderings(arr0, arr1, expected_count) -> None:
    """Test count_duplicates with arrays in different orderings and overlaps."""
    assert DoubleForLoop.count_duplicates(arr0, arr1) == expected_count
