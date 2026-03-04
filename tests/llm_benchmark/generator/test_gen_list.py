from typing import List

import pytest

from llm_benchmark.generator.gen_list import GenList


class TestRandomList:
    """Tests for the random_list generation method"""

    def test_random_list_length(self) -> None:
        """Test that random_list generates correct number of elements"""
        result = GenList.random_list(10, 100)
        assert len(result) == 10

    def test_random_list_empty(self) -> None:
        """Test that random_list with n=0 returns empty list"""
        result = GenList.random_list(0, 100)
        assert result == []

    def test_random_list_single_element(self) -> None:
        """Test that random_list with n=1 returns list with one element"""
        result = GenList.random_list(1, 100)
        assert len(result) == 1
        assert isinstance(result[0], int)

    def test_random_list_bounds(self) -> None:
        """Test that all values are within bounds [0, m)"""
        m = 50
        result = GenList.random_list(100, m)
        for val in result:
            assert 0 <= val <= m, f"Value {val} outside bounds [0, {m}]"

    def test_random_list_all_values_within_bound(self) -> None:
        """Test that all generated values are within the specified bound"""
        for m in [10, 50, 100]:
            result = GenList.random_list(50, m)
            for val in result:
                assert val >= 0
                assert val <= m

    def test_random_list_returns_list_of_ints(self) -> None:
        """Test that random_list returns list of integers"""
        result = GenList.random_list(10, 100)
        assert isinstance(result, list)
        assert all(isinstance(val, int) for val in result)

    @pytest.mark.parametrize("n", [1, 5, 10, 50])
    def test_random_list_various_sizes(self, n: int) -> None:
        """Test random_list with various sizes"""
        result = GenList.random_list(n, 100)
        assert len(result) == n

    @pytest.mark.parametrize("m", [5, 10, 50, 100])
    def test_random_list_various_bounds(self, m: int) -> None:
        """Test random_list with various max bounds"""
        result = GenList.random_list(20, m)
        assert all(0 <= val <= m for val in result)


class TestRandomMatrix:
    """Tests for the random_matrix generation method"""

    def test_random_matrix_dimensions(self) -> None:
        """Test that random_matrix generates correct dimensions"""
        result = GenList.random_matrix(5, 100)
        assert len(result) == 5
        assert all(len(row) == 5 for row in result)

    def test_random_matrix_empty(self) -> None:
        """Test that random_matrix with n=0 returns empty list"""
        result = GenList.random_matrix(0, 100)
        assert result == []

    def test_random_matrix_single_element(self) -> None:
        """Test that random_matrix with n=1 returns 1x1 matrix"""
        result = GenList.random_matrix(1, 100)
        assert len(result) == 1
        assert len(result[0]) == 1
        assert isinstance(result[0][0], int)

    def test_random_matrix_bounds(self) -> None:
        """Test that all values in matrix are within bounds"""
        m = 50
        result = GenList.random_matrix(10, m)
        for row in result:
            for val in row:
                assert 0 <= val <= m

    def test_random_matrix_returns_list_of_lists(self) -> None:
        """Test that random_matrix returns list of lists of integers"""
        result = GenList.random_matrix(5, 100)
        assert isinstance(result, list)
        assert all(isinstance(row, list) for row in result)
        assert all(isinstance(val, int) for row in result for val in row)

    @pytest.mark.parametrize("n", [1, 2, 5, 10])
    def test_random_matrix_various_sizes(self, n: int) -> None:
        """Test random_matrix with various sizes"""
        result = GenList.random_matrix(n, 100)
        assert len(result) == n
        assert all(len(row) == n for row in result)

    @pytest.mark.parametrize("m", [5, 10, 50])
    def test_random_matrix_various_bounds(self, m: int) -> None:
        """Test random_matrix with various max bounds"""
        result = GenList.random_matrix(5, m)
        assert all(0 <= val <= m for row in result for val in row)

    def test_random_matrix_square(self) -> None:
        """Test that random_matrix generates square matrix"""
        for n in [1, 3, 5, 7]:
            result = GenList.random_matrix(n, 100)
            assert len(result) == n
            assert all(len(row) == n for row in result)


def test_benchmark_random_list(benchmark) -> None:
    """Benchmark random_list generation"""
    benchmark(GenList.random_list, 100, 1000)


def test_benchmark_random_matrix(benchmark) -> None:
    """Benchmark random_matrix generation"""
    benchmark(GenList.random_matrix, 10, 100)
