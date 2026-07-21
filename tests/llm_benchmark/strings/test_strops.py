import pytest

from llm_benchmark.strings.strops import StrOps


@pytest.mark.parametrize(
    "value, reversed_value",
    [
        ("", ""),
        ("benchmark", "kramhcneb"),
        ("racecar", "racecar"),
    ],
)
def test_str_reverse(value: str, reversed_value: str) -> None:
    assert StrOps.str_reverse(value) == reversed_value


@pytest.mark.parametrize(
    "value, is_palindrome",
    [
        ("", True),
        ("racecar", True),
        ("benchmark", False),
    ],
)
def test_palindrome(value: str, is_palindrome: bool) -> None:
    assert StrOps.palindrome(value) == is_palindrome
