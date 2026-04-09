# Development Guide

Welcome to the llm-benchmarking-py development guide. This document provides instructions for setting up your development environment, including pre-commit hooks for code quality and security.

## Table of Contents

1. [Pre-commit Hooks](#pre-commit-hooks)
   - [Installation](#installation)
   - [Configuration](#configuration)
   - [Usage](#usage)
   - [Hook Descriptions](#hook-descriptions)
   - [Troubleshooting](#troubleshooting)
   - [Bypass Options](#bypass-options)

---

## Pre-commit Hooks

Pre-commit hooks are automated checks that run before each git commit. They help maintain code quality, consistency, and security across the repository.

### Installation

#### Step 1: Install pre-commit Package

First, ensure you have `pre-commit` installed as a development dependency:

```bash
pip install pre-commit
```

Or if you're using Poetry (recommended for this project):

```bash
poetry add --group dev pre-commit
```

#### Step 2: Activate Hooks in Your Git Repository

Once installed, initialize the pre-commit hooks:

```bash
pre-commit install
```

This command creates git hooks in your `.git/hooks/` directory that will run automatically before each commit.

#### Verification

To verify the installation was successful:

```bash
pre-commit --version
```

You should see output like: `pre-commit x.x.x`

### Configuration

The pre-commit hooks are configured in the `.pre-commit-config.yaml` file at the root of the repository. This file defines:

- Which hooks to run
- Hook repositories and versions
- Hook-specific arguments and configuration

**Important**: When `.pre-commit-config.yaml` is updated by maintainers, you may need to update your local hooks:

```bash
pre-commit autoupdate
```

This updates all hook repositories to their latest versions while respecting version constraints.

### Usage

#### Automatic Checking (On Commit)

Once hooks are installed, they run automatically before each commit:

```bash
git commit -m "Your commit message"
```

If hooks fail, the commit is blocked and you'll see:
1. Which hook failed
2. The file(s) that caused the failure
3. Error details and fixes applied (if applicable)

Many hooks automatically fix issues. After fixes are applied, stage the changes and commit again:

```bash
git add .
git commit -m "Your commit message"
```

#### Manual Checking (All Files)

To manually run all hooks against your entire codebase without committing:

```bash
pre-commit run --all-files
```

This is useful for:
- Testing hook configuration
- Getting a full report of issues before committing
- Running in CI/CD pipelines
- Bulk-checking the repository after updates

#### Manual Checking (Specific Hooks)

To run a specific hook on staged files:

```bash
pre-commit run hook-id
```

For example, to run only Black formatting:

```bash
pre-commit run black --all-files
```

#### Running Against Specific Files

To run hooks only on certain files:

```bash
pre-commit run --files file1.py file2.py
```

### Hook Descriptions

#### 1. **trailing-whitespace**
- **Purpose**: Removes trailing whitespace from lines
- **Behavior**: Automatically fixes by removing whitespace at line ends
- **Files**: All files
- **Example Fix**:
  ```python
  # Before: "def hello():    "
  # After:  "def hello():"
  ```

#### 2. **end-of-file-fixer**
- **Purpose**: Ensures files end with a single newline
- **Behavior**: Automatically adds a newline at end of file if missing
- **Files**: All files
- **Example Fix**:
  ```python
  # Before: "print('hello')"
  # After:  "print('hello')\n"
  ```

#### 3. **check-yaml**
- **Purpose**: Validates YAML file syntax
- **Behavior**: Prevents committing invalid YAML files
- **Files**: `.yaml`, `.yml` files
- **Example Error**:
  ```
  ERROR: Invalid YAML in config.yml
  mapping values are not allowed here
  ```

#### 4. **check-added-large-files**
- **Purpose**: Prevents committing large files to the repository
- **Behavior**: Blocks commits with files larger than the configured limit
- **Files**: All files
- **Default Limit**: ~500KB
- **Example Error**:
  ```
  ERROR: file.zip (2.5 MB) exceeds maximum file size (500 KB)
  ```
- **Fix**: Remove large files and use `.gitignore` or proper file storage

#### 5. **python-safety-dependencies-check**
- **Purpose**: Scans Python dependencies for known security vulnerabilities
- **Behavior**: Checks `requirements.txt` and `poetry.lock` for unsafe packages
- **Files**: Dependency files
- **Example Error**:
  ```
  Vulnerability found in package: django==2.0.0
  Use: django==2.2.0 or later
  ```
- **Fix**: Update vulnerable packages in `pyproject.toml` and run `poetry lock`

#### 6. **black**
- **Purpose**: Enforces consistent Python code formatting
- **Behavior**: Automatically reformats Python code to Black's style
- **Files**: `.py` files
- **Example Fix**:
  ```python
  # Before:
  result = some_function(arg1,arg2,  arg3)
  
  # After:
  result = some_function(arg1, arg2, arg3)
  ```
- **Configuration**: Uses Black's opinionated defaults (88-char line length)

#### 7. **isort**
- **Purpose**: Sorts and organizes Python import statements
- **Behavior**: Automatically groups and sorts imports
- **Files**: `.py` files
- **Example Fix**:
  ```python
  # Before:
  import os
  from typing import List
  import sys
  from collections import defaultdict
  
  # After:
  import os
  import sys
  from collections import defaultdict
  from typing import List
  ```
- **Configuration**: Uses Black-compatible profile for consistency

#### 8. **ruff**
- **Purpose**: Fast Python linter catching common errors and style issues
- **Behavior**: Automatically fixes fixable issues, reports others
- **Files**: `.py` files
- **Example Issues Caught**:
  - Unused imports
  - Undefined variables
  - Duplicate code
  - Missing docstrings
- **Example Fix**:
  ```python
  # Before:
  import os  # Unused
  x = 1
  print(y)  # Undefined
  
  # After:
  x = 1
  print(y)  # Still requires manual fix for undefined variable
  ```

#### 9. **yamllint**
- **Purpose**: Lints YAML files for style and common errors
- **Behavior**: Validates YAML syntax and enforces style consistency
- **Files**: `.yaml`, `.yml` files
- **Example Issues**:
  - Inconsistent indentation
  - Missing document start marker (`---`)
  - Line length violations
- **Example Error**:
  ```
  ERROR in .pre-commit-config.yaml:
  - Line 5: wrong indentation: expected 2 but found 4
  ```

#### 10. **pretty-format-toml**
- **Purpose**: Formats and validates TOML files
- **Behavior**: Automatically sorts and formats TOML configuration
- **Files**: `.toml` files
- **Example Fix**:
  ```toml
  # Before:
  [tool.poetry]
  name="project"
  version="1.0"
  
  [tool.isort]
  profile="black"
  
  # After (sorted alphabetically):
  [tool.isort]
  profile = "black"
  
  [tool.poetry]
  name = "project"
  version = "1.0"
  ```

### Troubleshooting

#### Issue: Hook Installation Failed

**Error**: `command not found: pre-commit`

**Solution**:
```bash
# Ensure pre-commit is installed
pip install pre-commit

# Or with Poetry:
poetry add --group dev pre-commit

# Then install hooks
pre-commit install
```

#### Issue: Hooks Not Running on Commit

**Error**: No hooks execute when you commit changes

**Solutions**:
1. Verify hooks are installed:
   ```bash
   ls -la .git/hooks/pre-commit
   ```

2. Reinstall hooks:
   ```bash
   pre-commit install
   pre-commit install --install-hooks
   ```

3. Check if hooks are disabled in git config:
   ```bash
   git config --get core.hooksPath
   # Should output: .git/hooks
   ```

#### Issue: Python Version Mismatch

**Error**: `python3 not found` or `python version does not match`

**Example**:
```
Hook failed with error code 1
The hook required python 3.9 but found python 3.8
```

**Solutions**:
1. Check your Python version:
   ```bash
   python --version
   python3 --version
   ```

2. Update hook configuration in `.pre-commit-config.yaml`:
   ```yaml
   - repo: https://github.com/psf/black
     hooks:
       - id: black
         language_version: python3.8  # Adjust to your version
   ```

3. Reinstall hooks:
   ```bash
   pre-commit install
   pre-commit autoupdate
   ```

#### Issue: Hook Failures Block Commits

**Example Error**:
```
black....................................................................FAILED
- hook id: black
- exit code: 1

1 file would be reformatted: src/example.py
```

**Solutions**:
1. Let the hook auto-fix the issue:
   ```bash
   # Many hooks auto-fix problems
   git add .
   git commit -m "Your message"  # Try again
   ```

2. Manually review changes:
   ```bash
   git diff  # See what changed
   ```

3. Stage the auto-fixed files:
   ```bash
   git add src/example.py
   git commit -m "Your message"
   ```

#### Issue: Slow Hook Execution

**Problem**: Hooks take a long time to run on every commit

**Solutions**:
1. Run hooks only on staged files (default behavior):
   ```bash
   # This is automatic, but you can verify
   pre-commit run
   ```

2. Skip expensive hooks during development (see Bypass Options below)

3. Reduce hook scope in `.pre-commit-config.yaml`:
   ```yaml
   - repo: https://github.com/psf/black
     hooks:
       - id: black
         exclude: ^(migrations/|data/)
   ```

#### Issue: Security Check Finds Vulnerable Dependency

**Error**:
```
Vulnerability found: requests==2.25.0
Use requests>=2.26.0
```

**Solution**:
1. Check which package is vulnerable:
   ```bash
   poetry show requests
   ```

2. Update the dependency:
   ```bash
   poetry update requests
   # Or specify version:
   poetry add requests@latest
   ```

3. Lock the changes:
   ```bash
   poetry lock
   ```

4. Retry commit:
   ```bash
   git add poetry.lock
   git commit -m "Update dependencies"
   ```

#### Issue: YAML File Validation Fails

**Error**:
```
yamllint...............................................................FAILED
- hook id: yamllint
- exit code: 1

ERROR in .pre-commit-config.yaml:
- Line 5: wrong indentation: expected 2 but found 4
```

**Solution**:
1. Review the file at the specified line:
   ```bash
   cat -n .pre-commit-config.yaml | head -10
   ```

2. Fix indentation (YAML requires 2-space indentation):
   ```yaml
   # Correct:
   repos:
     - repo: https://github.com/example
       hooks:
         - id: example
   
   # Incorrect (4 spaces):
   repos:
       - repo: https://github.com/example
   ```

3. Verify with:
   ```bash
   pre-commit run yamllint --all-files
   ```

#### Issue: Large File Accidentally Added

**Error**:
```
check-added-large-files..................................................FAILED
- hook id: check-added-large-files
- exit code: 1

File is 2.5 MB (exceeds 500 KB limit): data/large_file.zip
```

**Solution**:
1. Remove the file from git:
   ```bash
   git reset HEAD data/large_file.zip
   rm data/large_file.zip
   ```

2. Add to `.gitignore`:
   ```bash
   echo "data/large_file.zip" >> .gitignore
   ```

3. Commit:
   ```bash
   git add .gitignore
   git commit -m "Add large file to gitignore"
   ```

#### Issue: Cache/Environment Problems

**Error**: Hooks fail inconsistently or seem out of date

**Solution**:
1. Clear pre-commit cache:
   ```bash
   pre-commit clean
   ```

2. Reinstall all hooks:
   ```bash
   pre-commit install --install-hooks
   ```

3. Update to latest hook versions:
   ```bash
   pre-commit autoupdate
   ```

4. Run a full validation:
   ```bash
   pre-commit run --all-files
   ```

### Bypass Options

#### When to Bypass Hooks

- Committing work-in-progress (WIP) changes
- Reverting commits that were already validated
- Emergency fixes (use sparingly and with caution)
- Temporary debugging code (should not be bypassed)

**Important**: Only bypass when absolutely necessary. Hooks exist to maintain code quality and security.

#### How to Bypass (Safely)

**Option 1: Skip All Hooks (Not Recommended)**

```bash
git commit --no-verify -m "Emergency fix [skip hooks]"
```

**Option 2: Skip Specific Hooks (Recommended)**

Use the `SKIP` environment variable:

```bash
# Skip only the Black formatter
SKIP=black git commit -m "WIP: testing changes"

# Skip multiple hooks
SKIP=black,ruff,isort git commit -m "Temporary debugging"
```

**Option 3: Conditional Hook Skipping**

Create a pre-commit bypass for specific scenarios:

```bash
# Skip hooks for merge commits
SKIP=pre-commit git commit -m "Merge branch 'feature'"
```

#### Post-Bypass Validation

If you bypassed hooks, validate the code before merging to main:

```bash
# Full validation of all files
pre-commit run --all-files

# Or validate before pushing
pre-commit run --all-files && git push
```

---

## Related Documentation

- **Security Policy**: See [SECURITY.md](SECURITY.md) for security considerations and reporting vulnerabilities
- **Lock File Strategy**: See the upcoming "Lock File and Dependency Strategy" section in this guide
- **Git Workflow**: Ensure `.gitignore` is properly configured (see project root)

## Getting Help

If you encounter issues not covered here:

1. Check the hook's repository documentation:
   - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
   - [Black](https://github.com/psf/black)
   - [isort](https://github.com/PyCQA/isort)
   - [ruff](https://github.com/charliermarsh/ruff-pre-commit)
   - [yamllint](https://github.com/adrienverge/yamllint)

2. Run hooks in verbose mode:
   ```bash
   pre-commit run --all-files --verbose
   ```

3. Check your `.pre-commit-config.yaml` file for correctness

4. Review git hook logs:
   ```bash
   cat .git/hooks/pre-commit
   ```
