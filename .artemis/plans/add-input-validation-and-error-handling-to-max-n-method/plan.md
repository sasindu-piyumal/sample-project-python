# Plan Name: Add Input Validation and Error Handling to max_n Method

## Tasks

### 1. Add `ValueError` guards to `max_n` (Epic: Add input validation and tests for `max_n` in sort.py)

#### Description

In `src/llm_benchmark/algorithms/sort.py`, add the following guards at the top of the `max_n` method body, in this order:
1. `if v is None: raise ValueError('v must not be None')`
2. `if len(v) == 0: raise ValueError('v must not be empty')`
3. `if n <= 0: raise ValueError('n must be a positive integer')`
4. `if n > len(v): raise ValueError('n must not exceed the length of v')`

The existing `return heapq.nlargest(n, v)` line remains unchanged below the guards.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): N/A
    - current (in progress task): Add `ValueError` guards to `max_n` <-
    - upcoming (not yet): Update `max_n` docstring with constraints and Raises section
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Add four `ValueError` guards to the `max_n` method in `src/llm_benchmark/algorithms/sort.py`. These guards must be inserted at the top of the method body, before the existing `return` statement, in the exact order listed below.

##### Technical Specs:
- **Backend:** Modify `max_n` in `src/llm_benchmark/algorithms/sort.py` only
- **Validation:** Four guards, in order:
  1. `if v is None` → `raise ValueError('v must not be None')`
  2. `if len(v) == 0` → `raise ValueError('v must not be empty')`
  3. `if n <= 0` → `raise ValueError('n must be a positive integer')`
  4. `if n > len(v)` → `raise ValueError('n must not exceed the length of v')`

##### Implementation Checklist:
- [ ] Insert all four guards at the top of the `max_n` method body
- [ ] Preserve the exact error message strings — they are matched by tests
- [ ] Preserve guard ordering as specified (None → empty → n≤0 → n>len)
- [ ] Leave `return heapq.nlargest(n, v)` unchanged and in place below the guards
- [ ] Make no changes to any other method in the file

##### Success Criteria:
- [ ] Calling `max_n(None, 1)` raises `ValueError` with message `'v must not be None'`
- [ ] Calling `max_n([], 1)` raises `ValueError` with message `'v must not be empty'`
- [ ] Calling `max_n([1,2], 0)` raises `ValueError` with message `'n must be a positive integer'`
- [ ] Calling `max_n([1,2], -1)` raises `ValueError` with message `'n must be a positive integer'`
- [ ] Calling `max_n([1,2,3], 5)` raises `ValueError` with message `'n must not exceed the length of v'`
- [ ] Valid calls (e.g. `max_n([3,1,4], 2)`) still return correct results via `heapq.nlargest`

##### Files to modify:
- `src/llm_benchmark/algorithms/sort.py`

---


### 2. Add input validation and tests for `max_n` in sort.py

#### Description

The `max_n` method in `src/llm_benchmark/algorithms/sort.py` currently has no input validation. `heapq.nlargest` silently handles bad inputs in unexpected ways. This task adds explicit `ValueError` guards, updates the docstring, and introduces a new pytest test file covering all validation and happy paths.


### 3. Update `max_n` docstring with constraints and Raises section (Epic: Add input validation and tests for `max_n` in sort.py)

#### Description

In `src/llm_benchmark/algorithms/sort.py`, update the `max_n` docstring to:
- Clarify in the `Args` section that `v` must be a non-None, non-empty list and `n` must satisfy `0 < n <= len(v)`.
- Add a `Raises` section documenting all four `ValueError` cases:
  - `v is None`
  - `v` is empty
  - `n <= 0`
  - `n > len(v)`

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Add `ValueError` guards to `max_n`
    - current (in progress task): Update `max_n` docstring with constraints and Raises section <-
    - upcoming (not yet): Add parametrized error-path tests for `max_n`
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Update the docstring of the `max_n` method in `src/llm_benchmark/algorithms/sort.py` to reflect the input constraints and document the four `ValueError` cases that are now raised.

##### Technical Specs:
- **Scope:** Docstring only — no logic changes
- **Args section:** Clarify that `v` must be a non-`None`, non-empty list of integers, and that `n` must satisfy `0 < n <= len(v)`
- **Raises section:** Add a new `Raises:` block documenting all four `ValueError` cases:
  - `v is None`
  - `v` is empty
  - `n <= 0`
  - `n > len(v)`

##### Implementation Checklist:
- [ ] Update the `v` argument description to state it must be non-`None` and non-empty
- [ ] Update the `n` argument description to state the constraint `0 < n <= len(v)`
- [ ] Add a `Raises:` section in Google-style docstring format
- [ ] Document all four `ValueError` cases under `Raises:`, each with a brief condition description
- [ ] Make no changes to method logic or signature

##### Success Criteria:
- [ ] The `Args` section accurately describes the constraints on both `v` and `n`
- [ ] A `Raises` section exists and lists all four `ValueError` conditions
- [ ] The docstring style is consistent with the rest of the file
- [ ] No logic or behaviour is altered

##### Files to modify:
- `src/llm_benchmark/algorithms/sort.py`

---


### 4. Add parametrized error-path tests for `max_n` (Epic: Add input validation and tests for `max_n` in sort.py)

#### Description

Create `tests/llm_benchmark/algorithms/test_sort.py` and add a parametrized test function covering all invalid input combinations using `pytest.raises(ValueError)`. Required cases:
- `v=None` → raises `ValueError('v must not be None')`
- `v=[]` → raises `ValueError('v must not be empty')`
- `n=0` → raises `ValueError('n must be a positive integer')`
- `n=-1` → raises `ValueError('n must be a positive integer')`
- `v=[1,2,3], n=5` → raises `ValueError('n must not exceed the length of v')`

Use `pytest.mark.parametrize` with `(v, n, expected_message)` tuples and assert the exception message matches. Follow the style of `tests/llm_benchmark/algorithms/test_primes.py`.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Update `max_n` docstring with constraints and Raises section
    - current (in progress task): Add parametrized error-path tests for `max_n` <-
    - upcoming (not yet): Add parametrized happy-path tests for `max_n`
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Create `tests/llm_benchmark/algorithms/test_sort.py` and add a parametrized test function that verifies all invalid inputs to `max_n` raise the correct `ValueError` with the correct message.

##### Technical Specs:
- **Test framework:** `pytest`
- **Pattern:** Follow the style used in `tests/llm_benchmark/algorithms/test_primes.py` — use `pytest.mark.parametrize` and `pytest.raises`
- **Parametrize tuple shape:** `(v, n, expected_message)`
- **Required cases:**

| `v` | `n` | Expected message |
|---|---|---|
| `None` | `1` | `'v must not be None'` |
| `[]` | `1` | `'v must not be empty'` |
| `[1, 2, 3]` | `0` | `'n must be a positive integer'` |
| `[1, 2, 3]` | `-1` | `'n must be a positive integer'` |
| `[1, 2, 3]` | `5` | `'n must not exceed the length of v'` |

##### Implementation Checklist:
- [ ] Create `tests/llm_benchmark/algorithms/test_sort.py` (file does not yet exist)
- [ ] Add necessary imports (`pytest` and the `Sort` class or `max_n` function)
- [ ] Define a parametrized test function covering all five error cases above
- [ ] Use `pytest.raises(ValueError)` and assert the exception message matches `expected_message` exactly
- [ ] Do not add happy-path tests in this task — those belong in a separate function (ticket 7)

##### Success Criteria:
- [ ] All five parametrized error cases are present
- [ ] Each test asserts both the exception type (`ValueError`) and the exact message string
- [ ] Running `pytest tests/llm_benchmark/algorithms/test_sort.py` passes all error-path cases
- [ ] File structure and import style is consistent with `test_primes.py`

##### Dependencies:
- Ticket #4 (guards must exist for these tests to pass)

##### Files to modify:
- `tests/llm_benchmark/algorithms/test_sort.py` *(create new)*

---


### 5. Add parametrized happy-path tests for `max_n` (Epic: Add input validation and tests for `max_n` in sort.py)

#### Description

In `tests/llm_benchmark/algorithms/test_sort.py`, add a parametrized test function for valid calls using plain `assert`. Required cases:
- `v=[3,1,4,1,5,9], n=3` → `[9, 5, 4]`
- `v=[3,1,4,1,5,9], n=1` → `[9]`
- `v=[3,1,4], n=3` (`n=len(v)`) → `[4, 3, 1]`

Use `pytest.mark.parametrize` with `(v, n, expected)` tuples. This test must live in the same file as the error-path tests.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Add parametrized error-path tests for `max_n`
    - current (in progress task): Add parametrized happy-path tests for `max_n` <-
    - upcoming (not yet): N/A
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Add a parametrized happy-path test function to the existing `tests/llm_benchmark/algorithms/test_sort.py`, covering valid calls to `max_n` and asserting correct return values.

##### Technical Specs:
- **Test framework:** `pytest`
- **Pattern:** `pytest.mark.parametrize` with plain `assert` for value checks (no `pytest.raises`)
- **Parametrize tuple shape:** `(v, n, expected)`
- **Required cases:**

| `v` | `n` | Expected result |
|---|---|---|
| `[3, 1, 4, 1, 5, 9]` | `3` | `[9, 5, 4]` |
| `[3, 1, 4, 1, 5, 9]` | `1` | `[9]` |
| `[3, 1, 4]` | `3` | `[4, 3, 1]` |

##### Implementation Checklist:
- [ ] Add the happy-path test function to the existing `test_sort.py` (do not create a new file)
- [ ] Use `pytest.mark.parametrize` with `(v, n, expected)` tuples
- [ ] Assert the return value equals `expected` using a plain `assert` statement
- [ ] The third case (`n=len(v)`) explicitly validates the boundary condition is accepted
- [ ] Do not modify or duplicate the error-path test function from ticket #6

##### Success Criteria:
- [ ] All three parametrized happy-path cases are present
- [ ] Each case asserts the exact expected list is returned (order matters — `heapq.nlargest` returns descending order)
- [ ] Running `pytest tests/llm_benchmark/algorithms/test_sort.py` passes all happy-path cases alongside the error-path cases
- [ ] No use of `pytest.raises` in this test function

##### Dependencies:
- Ticket #6 (file must already exist)
- Ticket #4 (guards must not interfere with valid inputs)

##### Files to modify:
- `tests/llm_benchmark/algorithms/test_sort.py`

