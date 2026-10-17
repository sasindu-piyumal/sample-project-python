# Plan Name: Plan Project Security Improvements

## Tasks

### 1. Add pip-audit as a dev dependency (Epic: Add pip-audit dependency vulnerability scanning to CI)

#### Description

In `pyproject.toml`, add `pip-audit` under `[tool.poetry.group.dev.dependencies]`.

Then run `poetry lock` and `poetry install` to update `poetry.lock` and install the new dependency into the virtual environment.

Verify by running `poetry run pip-audit --version` and confirming it exits cleanly.

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): N/A
    - current (in progress task): Add pip-audit as a dev dependency <-
    - upcoming (not yet): Add pip-audit step to CI workflow
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Add `pip-audit` as a dev dependency to the project's Poetry configuration.

##### Technical Specs:
- **Package manager**: Poetry (`pyproject.toml` / `poetry.lock`)
- `pip-audit` must be declared under `[tool.poetry.group.dev.dependencies]` in `pyproject.toml`
- `poetry.lock` must be regenerated to reflect the new dependency

##### Implementation Checklist:
- [ ] Add `pip-audit` (no version constraint required, or use `"*"` / a reasonable lower bound) under `[tool.poetry.group.dev.dependencies]` in `pyproject.toml`
- [ ] Run `poetry lock` to regenerate `poetry.lock`
- [ ] Run `poetry install` to install the new dependency into the virtual environment
- [ ] Confirm `poetry run pip-audit --version` exits with code `0` and prints a version string

##### Success Criteria:
- [ ] `pyproject.toml` contains a `pip-audit` entry in the dev dependency group
- [ ] `poetry.lock` is updated and consistent with `pyproject.toml` (i.e. `poetry check` passes)
- [ ] `poetry run pip-audit --version` runs successfully in the local environment

##### Files to modify:
- `pyproject.toml`
- `poetry.lock`

---


### 2. Add pip-audit dependency vulnerability scanning to CI

#### Description

Integrate pip-audit into the llm_benchmark project to scan Poetry-managed Python dependencies for known CVEs on every push/PR. The build must fail on any detected vulnerability regardless of severity. pip-audit exits non-zero by default on any finding, so no extra severity flags are required.


### 3. Add pip-audit step to CI workflow (Epic: Add pip-audit dependency vulnerability scanning to CI)

#### Description

In `.github/workflows/ci.yml`, add a new step immediately after the existing 'Install dependencies' step:

```yaml
- name: Scan dependencies for vulnerabilities
  run: poetry run pip-audit
```

`poetry run pip-audit` audits all packages in the active Poetry virtual environment and exits non-zero on any finding — no additional flags are needed to gate on severity.

Verify by pushing a branch and confirming the new step appears in the GitHub Actions run log and the job fails if any vulnerability is found (or passes cleanly if none exist).

#### Prompt

<general>
These instructions are for a task that is part of a larger plan:
    <plan>
    - previous (completed): Add pip-audit as a dev dependency
    - current (in progress task): Add pip-audit step to CI workflow <-
    - upcoming (not yet): N/A
    </plan>
Within reason, stick to only the deliverables outlined in these instructions,
don't do extra work, and instead assume anything not mentioned is out of scope.
</general>

Add a vulnerability scanning step to the existing GitHub Actions CI workflow, using the `pip-audit` dev dependency introduced in the previous task.

##### Technical Specs:
- **CI file**: `.github/workflows/ci.yml`
- The new step must be placed immediately after the existing `Install dependencies` step
- The step runs `poetry run pip-audit`, which audits all packages in the active Poetry virtual environment
- No additional flags are needed — `pip-audit` exits non-zero on any finding, satisfying the requirement to fail the build on any detected vulnerability

##### Implementation Checklist:
- [ ] Insert the following step into `.github/workflows/ci.yml` directly after `Install dependencies`:
  ```yaml
  - name: Scan dependencies for vulnerabilities
    run: poetry run pip-audit
  ```
- [ ] Ensure step ordering is correct — it must not precede dependency installation
- [ ] Confirm no existing steps are removed or reordered unintentionally

##### Success Criteria:
- [ ] The new step is visible in the GitHub Actions run log on push/PR to `main`
- [ ] The job fails if `pip-audit` detects any vulnerability in the installed packages
- [ ] The job passes cleanly when no vulnerabilities are present
- [ ] Step order in the workflow is: checkout → setup Python → install Poetry → install deps → **scan dependencies** → run Bandit

##### Dependencies:
- Task (2) must be merged first — `pip-audit` must be present in `poetry.lock` before CI can invoke it

##### Files to modify:
- `.github/workflows/ci.yml`

