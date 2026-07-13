import pytest

from llm_benchmark.algorithms.sort import Sort


@pytest.mark.parametrize(
    "v, n, expected",
    [([5, 3, 2, 1, 4], 0, []), ([5, 3, 2, 1, 4], 3, [5, 4, 3])],
)
def test_max_n_normal_cases(v, n, expected):
    assert Sort.max_n(v, n) == expected


def test_max_n_empty_v_raises():
    with pytest.raises(ValueError, match="v must be non-empty"):
        Sort.max_n([], 1)


def test_max_n_n_greater_than_len_raises():
    v = [1, 2, 3]
    with pytest.raises(ValueError, match="greater than len\(v\)"):
        Sort.max_n(v, 4)


@pytest.mark.parametrize("n", [-1])
def test_max_n_negative_n_raises(n):
    with pytest.raises(ValueError, match="non-negative"):
        Sort.max_n([1, 2, 3], n)
