import pytest

from llm_benchmark.generator.gen_list import GenList


@pytest.mark.parametrize("n, m", [(1, 5), (3, 5), (5, 3), (4, 4)])
def test_random_matrix_shape(n: int, m: int) -> None:
    matrix = GenList.random_matrix(n, m)
    assert len(matrix) == n
    for row in matrix:
        assert len(row) == m


def test_benchmark_random_matrix(benchmark) -> None:
    benchmark(GenList.random_matrix, 5, 3)
