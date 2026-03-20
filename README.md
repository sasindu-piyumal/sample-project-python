# llm-benchmarking-py

## Security

This project takes security seriously. Please see [SECURITY.md](SECURITY.md) for:
- How to report security vulnerabilities responsibly
- Security best practices for using this project
- Information about security scanning tools and known limitations

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
