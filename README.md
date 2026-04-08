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

## Security

This project follows secure coding practices. See [SECURITY.md](SECURITY.md) for:
- Security fixes and improvements
- Secure random number generation guidelines
- Input validation best practices
- How to report security issues

**Recent Security Fix:** Updated random number generation to use cryptographically secure `secrets` module instead of predictable `random` module.
