# Makefile for development command shortcuts
# Provides convenient targets for common development tasks

.PHONY: all install build test benchmark format lint clean run

# Default target - runs install, format, lint, and test in sequence
all: install format lint test
	@echo "All tasks completed successfully!"

# Install dependencies using poetry
install:
	poetry install

# Alias for install target
build: install

# Run unit tests, excluding benchmarks
test:
	poetry run pytest --benchmark-skip tests/

# Run benchmarks only
benchmark:
	poetry run pytest --benchmark-only tests/

# Format code using black and isort
format:
	-poetry run black src/ tests/
	-poetry run isort src/ tests/

# Lint code using ruff
lint:
	poetry run ruff check src/ tests/

# Clean up Python cache, build artifacts, and test artifacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf dist/ build/ *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	@echo "Clean completed!"

# Run the main application
run:
	poetry run python main.py
