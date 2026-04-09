import pytest

from llm_benchmark.generator.gen_list import GenList


@pytest.mark.parametrize("rows, columns", [(2, 4), (3, 1)])
def test_random_matrix_uses_requested_dimensions(rows: int, columns: int) -> None:
    matrix = GenList.random_matrix(rows, columns)

    assert len(matrix) == rows
    assert all(len(row) == columns for row in matrix)
