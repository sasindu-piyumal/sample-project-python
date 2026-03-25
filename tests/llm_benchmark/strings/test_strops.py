import pytest

from llm_benchmark.strings.strops import StrOps


# Tests for str_reverse()
@pytest.mark.parametrize(
    "input_string, expected",
    [
        # Empty string
        ("", ""),
        # Single character
        ("a", "a"),
        # Even-length strings
        ("ab", "ba"),
        ("abcd", "dcba"),
        ("hello", "olleh"),
        # Odd-length strings
        ("abc", "cba"),
        ("abcde", "edcba"),
        # Unicode characters
        ("café", "éfac"),
        ("こんにちは", "はんちんこ"),
        ("🎉", "🎉"),
        # Special characters and whitespace
        ("a!b@c", "c@b!a"),
        ("a b c", "c b a"),
        ("hello world", "dlrow olleh"),
        # Mixed case
        ("HeLLo", "oLLeH"),
        # Repeated characters
        ("aaa", "aaa"),
        ("abba", "abba"),
        # Numbers
        ("12345", "54321"),
        # Complex mix
        ("Test123!@#", "#@!321tseT"),
    ],
)
def test_str_reverse(input_string: str, expected: str) -> None:
    """Test str_reverse with various inputs including edge cases."""
    assert StrOps.str_reverse(input_string) == expected


# Tests for palindrome()
@pytest.mark.parametrize(
    "input_string, is_palindrome",
    [
        # Empty string (technically a palindrome)
        ("", True),
        # Single character (always a palindrome)
        ("a", True),
        # Even-length palindromes
        ("abba", True),
        ("aa", True),
        ("abccba", True),
        # Even-length non-palindromes
        ("ab", False),
        ("abcd", False),
        ("hello", False),
        # Odd-length palindromes
        ("aba", True),
        ("racecar", True),
        ("noon", True),
        ("a", True),
        # Odd-length non-palindromes
        ("abc", False),
        ("abcde", False),
        ("hello", False),
        # Unicode palindromes
        ("a", True),
        ("aba", True),
        # Unicode non-palindromes
        ("café", False),
        ("こんにちは", False),
        # Single emoji
        ("🎉", True),
        # Special characters and whitespace
        ("a!b!a", True),
        ("a!b@a", True),
        ("a b a", True),
        ("a b c", False),
        ("! ! !", True),
        # Case sensitivity (different cases are different characters)
        ("Aa", False),
        ("ABA", False),
        ("aaa", True),
        # Numbers
        ("12321", True),
        ("12345", False),
        ("11", True),
        # Mixed palindromes
        ("a1b1a", True),
        ("race car", False),  # space matters
        ("12a21", True),
        # Repeated characters
        ("aaa", True),
        ("aaaa", True),
        ("ababa", True),
        ("ababab", False),
    ],
)
def test_palindrome(input_string: str, is_palindrome: bool) -> None:
    """Test palindrome with various inputs including edge cases."""
    assert StrOps.palindrome(input_string) == is_palindrome


# ============================================================================
# Performance Benchmarks using pytest-benchmark
# ============================================================================

# Benchmark data fixtures
SMALL_STRING = "The quick brown fox" * 1  # ~20 characters
MEDIUM_STRING = "The quick brown fox jumps over the lazy dog. " * 60  # ~2,820 characters
LARGE_STRING = "The quick brown fox jumps over the lazy dog. " * 2272  # ~102,240 characters

# Palindrome fixtures
SMALL_PALINDROME = "A man a plan a canal Panama" * 1  # Non-palindrome, ~28 chars
MEDIUM_PALINDROME = "racecar" * 400  # ~2,800 chars of palindromic pattern
LARGE_PALINDROME = "racecar" * 14400  # ~100,800 chars of palindromic pattern


# str_reverse() benchmarks
def test_benchmark_str_reverse_small(benchmark):
    """Benchmark str_reverse with small input (10-50 characters)."""
    result = benchmark(StrOps.str_reverse, SMALL_STRING)
    assert len(result) == len(SMALL_STRING)


def test_benchmark_str_reverse_medium(benchmark):
    """Benchmark str_reverse with medium input (1,000-5,000 characters)."""
    result = benchmark(StrOps.str_reverse, MEDIUM_STRING)
    assert len(result) == len(MEDIUM_STRING)


def test_benchmark_str_reverse_large(benchmark):
    """Benchmark str_reverse with large input (100,000+ characters)."""
    result = benchmark(StrOps.str_reverse, LARGE_STRING)
    assert len(result) == len(LARGE_STRING)


# palindrome() benchmarks
def test_benchmark_palindrome_small(benchmark):
    """Benchmark palindrome with small input (10-50 characters)."""
    result = benchmark(StrOps.palindrome, SMALL_PALINDROME)
    assert isinstance(result, bool)


def test_benchmark_palindrome_medium(benchmark):
    """Benchmark palindrome with medium input (1,000-5,000 characters)."""
    result = benchmark(StrOps.palindrome, MEDIUM_PALINDROME)
    assert isinstance(result, bool)


def test_benchmark_palindrome_large(benchmark):
    """Benchmark palindrome with large input (100,000+ characters)."""
    result = benchmark(StrOps.palindrome, LARGE_PALINDROME)
    assert isinstance(result, bool)
