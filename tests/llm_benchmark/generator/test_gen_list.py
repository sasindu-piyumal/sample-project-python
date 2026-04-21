"""Tests for the GenList generator module."""

from llm_benchmark.generator.gen_list import GenList


def test_random_matrix_dimensions() -> None:
    """Test that random_matrix generates correct dimensions (n rows, m columns).
    
    This test verifies that a call to random_matrix(3, 5) produces:
    - 3 rows (len(matrix) == 3)
    - 5 columns per row (len(matrix[i]) == 5 for each row)
    
    Before the fix, random_matrix(n, m) incorrectly generated n rows with n columns
    instead of n rows with m columns.
    """
    n = 3
    m = 5
    matrix = GenList.random_matrix(n, m)
    
    # Check that we have n rows
    assert len(matrix) == n, f"Expected {n} rows, got {len(matrix)}"
    
    # Check that each row has m columns
    for i, row in enumerate(matrix):
        assert len(row) == m, f"Row {i}: Expected {m} columns, got {len(row)}"


def test_random_matrix_dimensions_large() -> None:
    """Test random_matrix with different dimensions (2 rows, 7 columns)."""
    n = 2
    m = 7
    matrix = GenList.random_matrix(n, m)
    
    assert len(matrix) == n
    for row in matrix:
        assert len(row) == m


def test_random_matrix_dimensions_rectangle() -> None:
    """Test random_matrix with very different dimensions (10 rows, 3 columns)."""
    n = 10
    m = 3
    matrix = GenList.random_matrix(n, m)
    
    assert len(matrix) == n
    for row in matrix:
        assert len(row) == m
