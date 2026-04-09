import pytest
from llm_benchmark.generator.gen_list import GenList


def test_random_list_max_value_exclusive() -> None:
    """Test that random_list respects exclusive upper bound.
    
    The parameter m should be exclusive, meaning all generated values
    should be strictly less than m (not including m).
    """
    m = 10
    # Generate a large number of values to have high confidence
    # that we would see m if it were being generated
    random_list = GenList.random_list(1000, m)
    
    # All values should be in range [0, m)
    for value in random_list:
        assert value >= 0, f"Value {value} is less than 0"
        assert value < m, f"Value {value} is >= m={m}, but m should be exclusive upper bound"


def test_random_list_generates_expected_range() -> None:
    """Test that random_list generates values in the expected range."""
    m = 5
    n = 100
    random_list = GenList.random_list(n, m)
    
    # Check that list has correct length
    assert len(random_list) == n
    
    # Check that all values are in valid range [0, m)
    for value in random_list:
        assert 0 <= value < m, f"Value {value} not in range [0, {m})"


def test_random_matrix_generates_expected_range() -> None:
    """Test that random_matrix generates values in the expected range."""
    n = 5
    m = 3
    random_matrix = GenList.random_matrix(n, m)
    
    # Check that matrix has correct dimensions
    assert len(random_matrix) == n
    
    # Check that each row has correct number of columns and values are in range
    for row in random_matrix:
        assert len(row) == n, f"Row has {len(row)} columns, expected {n}"
        for value in row:
            assert 0 <= value < m, f"Value {value} not in range [0, {m})"
