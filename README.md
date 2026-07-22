# llm-benchmarking-py

## Usage

Build:

```shell
poetry install
```

Run Main:

```shell
poetry run main
```

Run Unit Tests:

```shell
poetry run pytest --benchmark-skip tests/
```

Run Benchmarking:

```shell
poetry run pytest --benchmark-only tests/
```

## Security checks

Run the same dependency and source checks used by CI through Poetry:

```shell
poetry run bandit -r src main.py -ll -ii -f json -o bandit-results.json
poetry run pip-audit --format json --output pip-audit-results.json
```

Bandit scans the application source (`src` and `main.py`), while pip-audit
checks the installed Python dependencies. The JSON reports are local generated
artifacts and are ignored by Git. CI uploads both reports as the
`security-scan-reports` workflow artifact. Security checks are currently
warning/report-only: findings do not fail pull requests or pushes to `main`.

### Remediating findings

For Bandit findings, review the reported file, line, and rule, then determine
whether the code is vulnerable in this application. Prefer a secure code
change, and document or narrowly suppress a confirmed false positive with
maintainer approval. Re-run the scan and tests after changes.

For pip-audit findings, identify the affected package and advisory, check its
supported fixed versions, and update the Poetry dependency constraint and lock
file. Verify compatibility with the test suite; if an upgrade is not yet
possible, record the rationale and mitigation and track the issue for follow-up.

Maintainers can also use GitHub-native Dependabot alerts, security advisories,
and code-scanning integrations for additional review and notification. These
are optional practices; this project does not require pre-commit hooks or
mandatory local secret scanning.
