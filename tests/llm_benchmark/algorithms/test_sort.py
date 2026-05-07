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
