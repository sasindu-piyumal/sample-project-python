# Plan Name: Fix Medium-Severity Performance Inefficiencies and Add Missing Error Handling

## Tasks

### 1. Refactor all five DsList methods to idiomatic Python (Epic: Optimise DsList methods in dslist.py)

#### Description

In `src/llm_benchmark/datastructures/dslist.py`, replace the body of each of the five static methods as follows:

1. `modify_list` (L15-18): replace `range(len(v))` append loop with `return [x + 1 for x in v]`
2. `search_list` (L32-36): replace `range(len(v))` loop with `return [i for i, x in enumerate(v) if x == n]`
3. `reverse_list` (L60-63): replace manual reverse accumulator with `return v[::-1]`
4. `rotate_list` (L79-83): replace two manual append loops with `return v[n:] + v[:n]` — the existing empty-list guard and `n = n % len(v)` modulo are already in place and should be preserved
5. `merge_lists` (L97-102): replace two `range(len())` append loops with `return v1 + v2`

Verification: run the existing test suite for `test_dslist.py` — all five benchmark tests must pass with outputs identical to before.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): N/A
    - current (in progress task): Refactor all five DsList methods to idiomatic Python <-
    - upcoming (not yet): Refactor sum_matrix in double.py and sync fix_code.py template
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Refactor the five static methods in `DsList` to use idiomatic Python, replacing all verbose manual loops with concise built-in equivalents.

##### Technical Specs:
- **File:** `src/llm_benchmark/datastructures/dslist.py`
- **Scope:** Method bodies only — signatures, docstrings, and any existing guard clauses must be preserved

##### Implementation Checklist:
- [ ] `modify_list` (L15-18): replace `range(len(v))` append loop with `return [x + 1 for x in v]`
- [ ] `search_list` (L32-36): replace `range(len(v))` index loop with `return [i for i, x in enumerate(v) if x == n]`
- [ ] `reverse_list` (L60-63): replace manual reverse accumulator with `return v[::-1]`
- [ ] `rotate_list` (L79-83): replace the two manual append loops with `return v[n:] + v[:n]` — the empty-list guard and `n = n % len(v)` modulo that precede this block are already in place and **must not be removed**
- [ ] `merge_lists` (L97-102): replace the two `range(len())` append loops with `return v1 + v2`
- [ ] No changes outside the listed method bodies

##### Success Criteria:
- [ ] All five `test_benchmark_*` functions in `tests/llm_benchmark/datastructures/test_dslist.py` pass
- [ ] Output of each method is identical to the previous implementation for all inputs exercised by the test suite
- [ ] No method signature or docstring has been altered

##### Files to modify:
- `src/llm_benchmark/datastructures/dslist.py`

---


### 2. Optimise DsList methods in dslist.py (Epic: Performance & error handling cleanup)

#### Description

Replace all five manual loop implementations in `src/llm_benchmark/datastructures/dslist.py` with idiomatic Python equivalents. All changes are inside the `DsList` class and the file has an existing test suite that validates each method.


### 3. Add error handling to test files (Epic: Performance & error handling cleanup)

#### Description

Wrap bare calls in the test suite with try/except so that exceptions produce clear, descriptive pytest failures rather than raw tracebacks. Targets: five `test_benchmark_*` functions in `test_dslist.py` and two DB-query tests in `test_query.py`.


### 4. Add error handling to main.py (Epic: Performance & error handling cleanup)

#### Description

Guard the two unprotected areas in `main.py`: the logger handler setup block (L26-30) and the seven benchmark sub-function calls (L164-171). A failure in any single benchmark should be logged at ERROR level and execution should continue to the next benchmark.


### 5. Optimise control and string module functions (Epic: Performance & error handling cleanup)

#### Description

Replace inefficient implementations in `double.py`, `fix_code.py`, `strops.py`, `single.py`, and `bst.py`. Covers: sum_matrix nested loops, palindrome manual loop, sum_modulus O(n) generator, and BST height recalculation on every insert.


### 6. Performance & error handling cleanup

#### Description

Final cleanup pass replacing verbose manual loops with idiomatic Python constructs across dslist.py, double.py, fix_code.py, strops.py, single.py, and bst.py, then adding missing try/except guards to main.py and the test suite. All changes are self-contained and independently testable.


### 7. Refactor sum_matrix in double.py and sync fix_code.py template (Epic: Optimise control and string module functions)

#### Description

Two coordinated changes that must stay in sync:

1. `src/llm_benchmark/control/double.py` (L84-88): replace the nested accumulator loop in `DoubleForLoop.sum_matrix` with `return sum(sum(row) for row in m)`. The existing method signature and docstring should be preserved.

2. `fix_code.py` (L144-148): update the embedded string template that contains the same old nested-loop `sum_matrix` body to use the identical one-liner. This is critical — `fix_code.py` is a patch script that writes source code to `double.py`; if the template is left unchanged, re-running the script will silently revert the fix.

Verification: run the `DoubleForLoop.sum_matrix` benchmark; also manually inspect that the template string in `fix_code.py` matches the new implementation.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Refactor all five DsList methods to idiomatic Python
    - current (in progress task): Refactor sum_matrix in double.py and sync fix_code.py template <-
    - upcoming (not yet): Refactor palindrome (strops.py) and sum_modulus (single.py) to efficient implementations
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Replace the nested-loop body of `DoubleForLoop.sum_matrix` with a one-liner, **and** update the matching embedded template in `fix_code.py` so that re-running the patch script cannot revert the change.

##### Technical Specs:
- **Backend:** Two files must change together; either change alone leaves the codebase in an inconsistent state
- `fix_code.py` is a patch script — its embedded string templates are written verbatim back to source files when the script runs

##### Implementation Checklist:
- [ ] `src/llm_benchmark/control/double.py` (L84-88): replace the nested `for row / for val` accumulator loop with `return sum(sum(row) for row in m)`
- [ ] Preserve the existing method signature and docstring in `double.py`
- [ ] `fix_code.py` (L144-148): locate the embedded string template containing the old `sum_matrix` body and update it to use the identical one-liner
- [ ] Verify by inspection that the template string in `fix_code.py` and the live implementation in `double.py` are character-for-character consistent

##### Success Criteria:
- [ ] `DoubleForLoop.sum_matrix` returns correct results when executed
- [ ] Running `fix_code.py` after the changes does not revert `double.py` to the old nested-loop implementation
- [ ] Method signature and docstring in `double.py` are unchanged

##### Dependencies:
- Task (6) should be complete, as other parts of the patch script may interact with `dslist.py`

##### Files to modify:
- `src/llm_benchmark/control/double.py`
- `fix_code.py`

---


### 8. Refactor palindrome (strops.py) and sum_modulus (single.py) to efficient implementations (Epic: Optimise control and string module functions)

#### Description

Two small but distinct performance improvements in separate files:

1. `src/llm_benchmark/strings/strops.py` (L24-27): replace the manual character-by-character comparison loop in `StrOps.palindrome` with `return s == s[::-1]`. Preserve existing method signature and any guard clauses.

2. `src/llm_benchmark/control/single.py` (L40-53): replace the O(n) generator `sum(i for i in range(n) if i % m == 0)` in `SingleForLoop.sum_modulus` with the O(1) arithmetic formula:
   ```python
   count = (n - 1) // m
   return m * count * (count + 1) // 2
   ```
   Edge-case behaviour must be preserved: if `n <= 0` the result should be 0 (count will be negative, guard if needed); `m == 0` should still raise `ZeroDivisionError` as currently documented.

Verification: run existing benchmark/unit tests for both methods and confirm outputs are identical to the generator-based results.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Refactor sum_matrix in double.py and sync fix_code.py template
    - current (in progress task): Refactor palindrome (strops.py) and sum_modulus (single.py) to efficient implementations <-
    - upcoming (not yet): Implement lazy height evaluation in BST
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Two independent performance improvements in separate files: replace a manual palindrome loop with a slice comparison, and replace an O(n) modulus generator with an O(1) arithmetic formula.

##### Technical Specs:
- **Files:** `strops.py` and `single.py` — changes are fully independent of each other
- **Validation:** Both replacements must produce byte-for-byte identical outputs to the code they replace across all inputs, including edge cases

##### Implementation Checklist:
- [ ] `src/llm_benchmark/strings/strops.py` (L24-27): replace the character-by-character comparison loop in `StrOps.palindrome` with `return s == s[::-1]`
- [ ] Preserve the existing method signature and any guard clauses that appear before the loop in `palindrome`
- [ ] `src/llm_benchmark/control/single.py` (L40-53): replace the generator expression in `SingleForLoop.sum_modulus` with:
  ```python
  count = (n - 1) // m
  return m * count * (count + 1) // 2
  ```
- [ ] Confirm edge-case parity for `sum_modulus`:
  - `m == 0` must still raise `ZeroDivisionError` (the floor-division `(n - 1) // m` will do this naturally — do not suppress it)
  - `n <= 0` must return `0`; verify whether the formula produces a negative `count` in this case and add an explicit guard (`if count < 0: return 0`) if needed

##### Success Criteria:
- [ ] All existing benchmark and unit tests for `StrOps.palindrome` pass with unchanged output
- [ ] All existing benchmark and unit tests for `SingleForLoop.sum_modulus` pass with unchanged output
- [ ] `sum_modulus(n=0, m=3)` and `sum_modulus(n=-5, m=3)` both return `0`
- [ ] `sum_modulus(n=10, m=0)` raises `ZeroDivisionError`
- [ ] Method signatures and docstrings are unchanged in both files

##### Files to modify:
- `src/llm_benchmark/strings/strops.py`
- `src/llm_benchmark/control/single.py`

---


### 9. Implement lazy height evaluation in BST (Epic: Optimise control and string module functions)

#### Description

In `src/llm_benchmark/datastructures/bst.py`, replace the eager per-insert height recalculation with a dirty-flag pattern:

1. `BST.__init__`: add `self._height_dirty = False` and initialise `self._height = -1` (representing an empty tree). This avoids any traversal on construction.

2. `BST._insert_value` (L58): remove the `self._height = self._calculate_height(self._root)` call and replace it with `self._height_dirty = True`.

3. `BST.height` property: before returning `self._height`, check `if self._height_dirty:` — if so, call `self._height = self._calculate_height(self._root)` and reset `self._height_dirty = False`. Then return `self._height`.

This reduces the cost of N sequential inserts from O(N²) to O(N) total, with a single O(N) traversal paid only on the first `height` access after inserts.

Verification: insert a sequence of values and assert `bst.height` returns the correct value; assert no traversal occurs if `height` is not called after an insert.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Refactor palindrome (strops.py) and sum_modulus (single.py) to efficient implementations
    - current (in progress task): Implement lazy height evaluation in BST <-
    - upcoming (not yet): Wrap logger handler setup in try/except
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Replace the eager per-insert height recalculation in `BST` with a dirty-flag pattern so that `N` sequential inserts cost O(N) total rather than O(N²).

##### Technical Specs:
- **File:** `src/llm_benchmark/datastructures/bst.py`
- **Pattern:** Lazy evaluation via a boolean dirty flag — the expensive `_calculate_height` traversal is deferred until the `height` property is actually read
- **Invariant:** A fresh, empty tree must never trigger a traversal; `_height` is initialised to `-1` (sentinel for empty tree) and `_height_dirty` to `False`

##### Implementation Checklist:
- [ ] `BST.__init__`: add `self._height = -1` and `self._height_dirty = False` — no call to `_calculate_height` at construction time
- [ ] `BST._insert_value` (L58): remove the line `self._height = self._calculate_height(self._root)` and replace it with `self._height_dirty = True`
- [ ] `BST.height` property: add a guard at the top of the getter —
  ```python
  if self._height_dirty:
      self._height = self._calculate_height(self._root)
      self._height_dirty = False
  return self._height
  ```
- [ ] No other methods or logic in `bst.py` should be modified
- [ ] Confirm `_calculate_height` itself is unchanged — it is only the call-site that moves

##### Success Criteria:
- [ ] Inserting a known sequence of values and then reading `bst.height` returns the correct height
- [ ] Reading `bst.height` twice after a single batch of inserts only triggers one traversal (the dirty flag is cleared after the first read)
- [ ] Constructing a `BST` without calling `height` does not invoke `_calculate_height` at any point
- [ ] All pre-existing tests against the `BST` class continue to pass

##### Files to modify:
- `src/llm_benchmark/datastructures/bst.py`


### 10. Wrap logger handler setup in try/except (Epic: Add error handling to main.py)

#### Description

In `main.py` (L26-30), wrap the logger configuration block — `logger.handlers.clear()` and all subsequent handler additions — in a `try/except Exception as e:` block. On failure, print or log a fallback warning (using a bare `print()` or `logging.lastResort` if the handler setup has already partially failed) and continue, since a logging misconfiguration should not abort the entire benchmark run.

Verification: simulate a bad handler configuration and confirm that `main()` continues executing rather than raising.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Implement lazy height evaluation in BST
    - current (in progress task): Wrap logger handler setup in try/except <-
    - upcoming (not yet): Wrap each benchmark sub-function call in an individual try/except
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Guard the logger handler setup in `main.py` against configuration failures. Currently, if anything in the handler setup block raises (e.g. a bad file path, permissions error, or misconfigured formatter), the entire benchmark run aborts before a single benchmark has executed.

##### Technical Specs:
- **Backend:** Wrap the logger configuration block in `main.py` (L26-30) — beginning at `logger.handlers.clear()` and covering all subsequent handler additions — in a `try/except Exception as e:` block
- **Fallback:** On failure, emit a warning via `print()` or `logging.lastResort` (do not assume the logger itself is usable at this point) and allow execution to continue

##### Implementation Checklist:
- [ ] Identify the full extent of the handler setup block (from `logger.handlers.clear()` through the last handler addition)
- [ ] Wrap the entire block in a single `try/except Exception as e:`
- [ ] On except, emit a human-readable fallback warning identifying that logger setup failed (include `e` in the message)
- [ ] Confirm no `raise` or `sys.exit()` is present in the except branch — execution must continue

##### Success Criteria:
- [ ] Simulating a bad handler (e.g. patching a handler constructor to raise) causes the except branch to fire and `main()` continues past the setup block without re-raising
- [ ] The fallback warning is visible in output when the except branch is taken
- [ ] Normal execution (no fault injected) is unaffected

##### Files to modify:
- `main.py`

---


### 11. Wrap each benchmark sub-function call in an individual try/except (Epic: Add error handling to main.py)

#### Description

In `main.py` `main()` function (L164-171), each of the 7 sub-function calls (`single`, `double`, `sql`, `primes`, `sort`, `dslist`, `strops`) must be wrapped in its own `try/except Exception as e:` block. On exception, log at ERROR level using the existing logger: `logger.error(f'<function_name> benchmark failed: {e}')` and continue to the next call.

Do NOT wrap all 7 in a single try/except — each must be individually guarded so that a failure in one does not prevent the remaining benchmarks from running.

Verification: mock one sub-function to raise and confirm the rest still execute and the error is logged at ERROR level.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Wrap logger handler setup in try/except
    - current (in progress task): Wrap each benchmark sub-function call in an individual try/except <-
    - upcoming (not yet): Add try/except to benchmark tests in test_dslist.py
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Each of the 7 benchmark sub-function calls in `main()` (L164-171) must be individually guarded so that a failure in any one benchmark does not prevent the remaining benchmarks from running.

##### Technical Specs:
- **Backend:** Wrap each call — `single`, `double`, `sql`, `primes`, `sort`, `dslist`, `strops` — in its **own** `try/except Exception as e:` block. Do not use a single block covering multiple calls
- **Logging:** On exception, call `logger.error(f'<function_name> benchmark failed: {e}')` using the function's actual name as the prefix, then continue to the next call

##### Implementation Checklist:
- [ ] Wrap each of the 7 calls in a separate, independent `try/except Exception as e:` block
- [ ] Each except branch logs at `ERROR` level with a message identifying the specific benchmark that failed
- [ ] No `raise` or early return in any except branch
- [ ] Existing call signatures and argument passing are left unchanged

##### Success Criteria:
- [ ] Mocking any single sub-function to raise confirms: the error is logged at `ERROR` level with the correct function name, and all remaining sub-functions still execute
- [ ] When no benchmark raises, behaviour is identical to before this change
- [ ] No two benchmark calls share a single try/except block

##### Files to modify:
- `main.py`

---


### 12. Add try/except to benchmark tests in test_dslist.py (Epic: Add error handling to test files)

#### Description

In `tests/llm_benchmark/datastructures/test_dslist.py`, wrap the `benchmark(...)` call in each of these five test functions with `try/except Exception as e: pytest.fail(str(e))`:

- `test_benchmark_modify_list` (L22)
- `test_benchmark_search_list` (L38)
- `test_benchmark_sort_list` (L53)
- `test_benchmark_reverse_list` (L69)
- `test_benchmark_rotate_list` (L86)

The pattern must not silently swallow exceptions — `pytest.fail(str(e))` surfaces the original error message as a clean test failure rather than a raw traceback. Import `pytest` if not already present.

Verification: mock `benchmark` to raise an exception in one test and confirm pytest reports a FAILED result with the exception message (not an ERROR/traceback).

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Wrap each benchmark sub-function call in an individual try/except
    - current (in progress task): Add try/except to benchmark tests in test_dslist.py <-
    - upcoming (not yet): Add try/except to DB query tests in test_query.py
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Wrap the `benchmark(...)` call in each of the five `test_benchmark_*` functions in `test_dslist.py` with a `try/except` that converts exceptions into clean pytest failures rather than raw tracebacks.

##### Technical Specs:
- **Testing:** Apply the pattern `try: benchmark(...) except Exception as e: pytest.fail(str(e))` consistently across all five functions
- **Import:** Ensure `pytest` is imported at the top of the file if it is not already

##### Implementation Checklist:
- [ ] Apply the try/except pattern to `test_benchmark_modify_list` (L22)
- [ ] Apply the try/except pattern to `test_benchmark_search_list` (L38)
- [ ] Apply the try/except pattern to `test_benchmark_sort_list` (L53)
- [ ] Apply the try/except pattern to `test_benchmark_reverse_list` (L69)
- [ ] Apply the try/except pattern to `test_benchmark_rotate_list` (L86)
- [ ] `pytest.fail(str(e))` is used — not `raise`, not a bare `pass`, not a custom message that omits `str(e)`
- [ ] Add `import pytest` if absent

##### Success Criteria:
- [ ] Patching `benchmark` to raise an arbitrary exception in any one of these tests causes pytest to report that test as **FAILED** (not **ERROR**) with the exception's message visible in the failure output
- [ ] Tests that do not raise continue to pass normally
- [ ] No exception is silently swallowed — `str(e)` is always forwarded to `pytest.fail`

##### Files to modify:
- `tests/llm_benchmark/datastructures/test_dslist.py`

---


### 13. Add try/except to DB query tests in test_query.py (Epic: Add error handling to test files)

#### Description

In `tests/llm_benchmark/sql/test_query.py`, wrap the database call and assertion in each of these two test functions with `try/except Exception as e: pytest.fail(f'<test_name> failed: {e}')`:

- `test_join_albums` (L21-26): wrap `SqlQuery.join_albums()[0]` and the surrounding assertions
- `test_top_invoices` (L33-37): wrap `SqlQuery.top_invoices()` and the surrounding assertions

The descriptive message in `pytest.fail()` should identify which query failed, making CI triage easier. Import `pytest` if not already present.

Verification: point the DB connection at a missing/bad database path and confirm both tests report FAILED with descriptive messages rather than raw exceptions.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Add try/except to benchmark tests in test_dslist.py
    - current (in progress task): Add try/except to DB query tests in test_query.py <-
    - upcoming (not yet): N/A
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Wrap the database calls and their surrounding assertions in `test_join_albums` and `test_top_invoices` in `test_query.py` with `try/except` blocks that produce descriptive, identifiable failures in CI rather than raw exception tracebacks.

##### Technical Specs:
- **Testing:** Each test's DB call and assertions are wrapped together in a single `try/except Exception as e:` block calling `pytest.fail()` with a message that names the failing query
- **Failure message format:** `pytest.fail(f'<test_name> failed: {e}')` — e.g. `'test_join_albums failed: {e}'`
- **Import:** Ensure `pytest` is imported if not already present

##### Implementation Checklist:
- [ ] In `test_join_albums` (L21-26): wrap `SqlQuery.join_albums()[0]` and all assertions in `try/except Exception as e: pytest.fail(f'test_join_albums failed: {e}')`
- [ ] In `test_top_invoices` (L33-37): wrap `SqlQuery.top_invoices()` and all assertions in `try/except Exception as e: pytest.fail(f'test_top_invoices failed: {e}')`
- [ ] The except branch covers both the DB call and the assertions — a failed assertion that raises should also be caught and re-surfaced via `pytest.fail`
- [ ] Add `import pytest` if absent

##### Success Criteria:
- [ ] Configuring the DB connection to point at an invalid or missing path causes both tests to report **FAILED** with a message that names the test and includes the underlying error — not an unhandled **ERROR** traceback
- [ ] The failure message in each test clearly identifies which query was being executed, aiding CI triage
- [ ] Tests pass normally when the DB connection is valid

##### Files to modify:
- `tests/llm_benchmark/sql/test_query.py`

