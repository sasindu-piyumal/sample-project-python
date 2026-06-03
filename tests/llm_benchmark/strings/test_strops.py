import pytest

from llm_benchmark.strings.strops import StrOps


@pytest.mark.parametrize(
    "s, expected",
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ba"),
        ("hello", "olleh"),
        ("racecar", "racecar"),
    ],
)
def test_str_reverse(s: str, expected: str) -> None:
    assert StrOps.str_reverse(s) == expected


def test_benchmark_str_reverse(benchmark) -> None:
    benchmark(StrOps.str_reverse, "hello world")


@pytest.mark.parametrize(
    "s, expected",
    [
        ("", True),
        ("a", True),
        ("aa", True),
        ("ab", False),
        ("racecar", True),
        ("hello", False),
        ("madam", True),
        ("abcba", True),
        ("abcd", False),
    ],
)
def test_palindrome(s: str, expected: bool) -> None:
    assert StrOps.palindrome(s) == expected


def test_benchmark_palindrome(benchmark) -> None:
    benchmark(StrOps.palindrome, "racecar")
