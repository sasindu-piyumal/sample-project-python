# Planning conversation

> Captured on 2026-04-16T12:20:15.085Z

## You

Missing input validation for edge cases

Description: The max_n method does not validate that n is positive or that n does not exceed the list length. If n is negative, zero, or larger than the list size, heapq.nlargest will either return unexpected results or fail gracefully without informative error messages. Additionally, if v is None or an empty list, no error handling or validation exists to provide meaningful feedback to the caller about invalid inputs.

File: src/llm_benchmark/algorithms/sort.py:39-49


Generate a plan for these issues

## You

Missing input validation for edge cases

Description: The max_n method does not validate that n is positive or that n does not exceed the list length. If n is negative, zero, or larger than the list size, heapq.nlargest will either return unexpected results or fail gracefully without informative error messages. Additionally, if v is None or an empty list, no error handling or validation exists to provide meaningful feedback to the caller about invalid inputs.

File: src/llm_benchmark/algorithms/sort.py:39-49


Generate a plan for these issues

## Artemis

I've made an assessment of your request.

## Artemis

Let me explore the context of the relevant file before I ask you anything.

> 📄 Read `src/llm_benchmark/algorithms/sort.py`

> 📄 Read `tests/llm_benchmark/algorithms/test_primes.py`

## Artemis

No existing tests cover `sort.py` — I can see the test suite uses `pytest` with parametrize, which sets a clear pattern for new tests. The other two methods in the file lack validation too. I have a clear picture now — one key question before finalising requirements.

## Artemis

Good picture of the project. There are **no existing tests** for `sort.py` (only `test_primes.py` exists), and neither `sort_list` nor `dutch_flag_partition` have any input validation either.

One key question before I lock in requirements:

### Question from Artemis

When `max_n` receives invalid input, what should the method do — and should the other two methods (`sort_list`, `dutch_flag_partition`) also get similar validation added?

**Raise a `ValueError`** — the method throws a descriptive exception for each bad input (e.g. `n must be positive`, `v must not be None`). This is the most conventional Python approach and gives callers actionable error messages.

**Return a safe default** — e.g. return `[]` for `None`/empty `v`, or clamp `n` to `len(v)`. Softer, but callers may not realise something went wrong.

**Scope: `max_n` only** vs **all three methods** — the issue calls out `max_n` specifically, but `sort_list` and `dutch_flag_partition` have the same gap. Expanding scope adds consistency but increases work.

- Raise ValueError, max_n only
- Raise ValueError, all three methods
- Return safe default, max_n only
- Return safe default, all three methods

## You

Please stop questioning me and proceed with the Plan.

## Artemis

Understood. I'll proceed with sensible defaults.

## Artemis

The plan adds input validation to the `max_n` method in `sort.py` and backs it with a new test file. Four ordered `ValueError` guards will be inserted before the `heapq.nlargest` call — covering `None` input, empty list, non-positive `n`, and `n` exceeding the list length — along with a docstring update documenting the new constraints. A new `test_sort.py` will then be created with parametrized pytest tests for all five invalid input cases and three valid happy-path cases. This is a small, self-contained change with no external dependencies.

### Question from Artemis

Would you like to proceed with this plan?

- Yes, proceed
- No, let me adjust

## You

Yes, proceed

> ✅ Plan created successfully
