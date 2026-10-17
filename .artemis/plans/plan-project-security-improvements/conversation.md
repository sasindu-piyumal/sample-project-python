# Planning conversation

> Captured on 2026-04-16T05:32:49.487Z

## You

Help me decide the next steps to improve the security of this project.

## You

Help me decide the next steps to improve the security of this project.

## Artemis

I've made an assessment of your request.

## Artemis

Let me take a look at the project structure first.

> 📄 Read `pyproject.toml`

> 📄 Read `.github/workflows/ci.yml`

> 📄 Read `README.md`

> 📄 Read `main.py`

> 📄 Read `src/llm_benchmark/sql/query.py`

## Artemis

I've found several useful things — Bandit is already installed and running in CI, but there are a few gaps that are typical starting points for improving security posture.

## Artemis

Here's what I've found so far — your project already has **Bandit** running in CI, which is a good foundation. That said, I've identified **four concrete gaps**:

| Gap | Detail |
|---|---|
| 🔗 **Dependency scanning** | No tool checking for known CVEs in your Poetry dependencies |
| 📌 **CI action pinning** | `actions/checkout@v2` and `actions/setup-python@v2` use floating tags — a supply chain risk |
| 🔍 **SAST strictness** | Bandit only fails on HIGH severity + HIGH confidence; medium issues go undetected |
| 🔑 **Secrets scanning** | No check to prevent accidental credential commits |

Given this is a benchmarking library (not a user-facing app), some of these matter more than others.

Which of these feels most urgent to you?

- **Dependencies** — know when a package you're using has a known exploit
- **CI hardening** — action pinning + secrets scanning to protect the pipeline itself
- **Stricter SAST** — catch more code-level issues before they merge

Or all of the above — it's a manageable scope.

## You

Dependencies

## Artemis

Good choice — there are two main tools for this. I'd recommend **`pip-audit`** — it's free, actively maintained by Google, and works natively with Poetry via `pip-audit --requirement <(poetry export)`. **`safety`** used to be popular but now requires a paid licence to access its full vulnerability database.

That said, a quick question on how strictly it should gate your CI:

Should the build **fail on any detected vulnerability**, or only on **HIGH/CRITICAL severity** ones (mirroring how you've set up Bandit)?

- **Any severity** — zero tolerance, even low-impact advisories block merges. Noisy but thorough.
- **HIGH/CRITICAL only** — consistent with your existing Bandit policy; lower-severity CVEs are surfaced but won't block the pipeline.

## You

Any severity

## Artemis

Got it. The scope is clear — let me check one technical detail about how Poetry exports dependencies before wrapping up.

## Artemis

The plan adds `pip-audit` to catch known CVEs in your Poetry dependencies — a small, two-step change. First, `pip-audit` gets added as a dev dependency and `poetry.lock` is updated. Then a single step is added to your existing GitHub Actions workflow that runs `poetry run pip-audit` after `poetry install`. No configuration is needed for severity gating — pip-audit fails the build on any finding by default, matching your zero-tolerance requirement.

### Question from Artemis

Would you like to proceed with this plan?

- Yes, proceed
- No, let me adjust

## You

Yes, proceed

> ✅ Plan created successfully
