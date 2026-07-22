import pytest

from llm_benchmark.generator import gen_list
from llm_benchmark.generator.gen_list import GenList


def test_random_list_uses_exclusive_upper_bound(monkeypatch) -> None:
    stops = []

    def fake_randrange(stop: int) -> int:
        stops.append(stop)
        return stop - 1

    monkeypatch.setattr(gen_list, "randrange", fake_randrange)

    assert GenList.random_list(3, 5) == [4, 4, 4]
    assert stops == [5, 5, 5]


@pytest.mark.parametrize("bound", [0, -1])
def test_random_list_rejects_invalid_upper_bound(bound: int) -> None:
    with pytest.raises(ValueError, match="m must be greater than 0"):
        GenList.random_list(1, bound)


def test_random_matrix_uses_requested_rows_columns_and_value_bound(monkeypatch) -> None:
    stops = []

    def fake_randrange(stop: int) -> int:
        stops.append(stop)
        return stop - 1

    monkeypatch.setattr(gen_list, "randrange", fake_randrange)

    assert GenList.random_matrix(2, 3) == [[2, 2, 2], [2, 2, 2]]
    assert stops == [3, 3, 3, 3, 3, 3]
