# llm-benchmarking-py

## Development

### Quick Start

Get started with the project in three simple steps:

1. **Install dependencies:**
   ```shell
   make install
   ```

2. **Set up pre-commit hooks (optional but recommended):**
   ```shell
   pre-commit install
   ```

3. **Run the development workflow:**
   ```shell
   make all
   ```

This will install dependencies, format your code, run linting checks, and execute tests.

### Makefile Commands

The project provides convenient `make` commands for common development tasks:

#### Setup & Maintenance

- **`make install`** - Install project dependencies using Poetry
  ```shell
  make install
  ```

- **`make clean`** - Remove generated artifacts, cache files, and build directories
  ```shell
  make clean
  ```

#### Development Workflow

- **`make format`** - Auto-format code using Black and isort
  ```shell
  make format
  ```
  Formats all Python files in `src/` and `tests/` directories.

- **`make lint`** - Check code quality using Ruff linter
  ```shell
  make lint
  ```
  Identifies code quality issues, style violations, and potential bugs.

#### Testing & Benchmarking

- **`make test`** - Run unit tests (excludes benchmarks)
  ```shell
  make test
  ```

- **`make benchmark`** - Run performance benchmarks only
  ```shell
  make benchmark
  ```

#### Running the Application

- **`make run`** - Execute the main application
  ```shell
  make run
  ```

#### Complete Workflow

- **`make all`** - Run the full development workflow
  ```shell
  make all
  ```
  Runs: `install` → `format` → `lint` → `test` (in sequence)

### Pre-commit Hooks

Pre-commit hooks automatically check code quality and formatting on every commit, ensuring consistent code standards.

#### Setup

Install pre-commit hooks:

```shell
pre-commit install
```

This configures Git to automatically run checks before each commit.

#### Running Hooks

**Automatically** - Hooks run on every `git commit`

**Manually** - Run all hooks on all files:

```shell
pre-commit run --all-files
```

#### What Hooks Check

The project includes the following pre-commit hooks:

- **Black** - Code formatting consistency
- **isort** - Import statement organization
- **Ruff** - Code quality and linting checks
- **Trailing whitespace** - Removes trailing whitespace
- **End-of-file fixer** - Ensures files end with newline
- **YAML validator** - Checks YAML file syntax
- **Large file detector** - Warns about large files (>1MB)

### Poetry Commands (Advanced Reference)

For advanced use cases, you can run Poetry commands directly:

- **Install dependencies:**
  ```shell
  poetry install
  ```

- **Run the main application:**
  ```shell
  poetry run python main.py
  ```

- **Run unit tests:**
  ```shell
  poetry run pytest --benchmark-skip tests/
  ```

- **Run benchmarks:**
  ```shell
  poetry run pytest --benchmark-only tests/
  ```

- **Format code:**
  ```shell
  poetry run black src/ tests/
  poetry run isort src/ tests/
  ```

- **Run linting:**
  ```shell
  poetry run ruff check src/ tests/
  ```

Most developers should use the `make` commands above instead, as they provide a simpler, unified interface.
