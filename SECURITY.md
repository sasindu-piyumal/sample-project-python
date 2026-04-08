# Security Documentation

## Overview

This document describes security considerations, vulnerabilities that have been addressed, and secure coding practices implemented in the llm-benchmark-py project.

---

## Security Fixes

### 🔒 Fixed: Insecure Random Number Generation (HIGH)

**Status:** ✅ FIXED  
**Date:** 2024  
**Affected Module:** `src/llm_benchmark/generator/gen_list.py`

#### Vulnerability Description

The `GenList` class previously used Python's `random` module for generating random numbers. The `random` module implements the Mersenne Twister algorithm (MT19937), which is **NOT cryptographically secure** and is **predictable**.

**Security Risks:**
- **State Reconstruction:** After observing 624 consecutive 32-bit outputs, an attacker can completely reconstruct the internal state of the random number generator
- **Future Prediction:** Once the state is known, all future "random" values can be predicted
- **Replay Attacks:** With a known or guessed seed, the entire sequence can be reproduced
- **Not Suitable for Security:** Should never be used for tokens, passwords, session IDs, or any security-sensitive randomness

#### The Fix

**Changed from:**
```python
from random import randint

def random_list(n: int, m: int) -> List[int]:
    return [randint(0, m) for _ in range(n)]
```

**Changed to:**
```python
import secrets

def random_list(n: int, m: int) -> List[int]:
    if n < 0 or m < 0:
        raise ValueError("Parameters must be non-negative")
    return [secrets.randbelow(m + 1) for _ in range(n)]
```

#### Why This Matters

The `secrets` module:
- ✅ Uses cryptographically strong random number generation
- ✅ Sources entropy from OS-level secure sources (`/dev/urandom` on Unix, `CryptGenRandom()` on Windows)
- ✅ Is unpredictable even with knowledge of previous outputs
- ✅ Is suitable for security-sensitive applications
- ✅ Meets OWASP recommendations for secure random number generation

#### Additional Security Hardening

Beyond replacing the random number generator, we also added:

1. **Input Validation:**
   - Reject negative values for `n` and `m` parameters
   - Prevent potential integer overflow or unexpected behavior
   - Clear error messages for invalid inputs

2. **Updated Documentation:**
   - Security notes in docstrings
   - Clear examples of proper usage
   - Warnings about previous vulnerability

3. **Comprehensive Testing:**
   - Test demonstrating the old vulnerability (predictability)
   - Test verifying the new implementation is unpredictable
   - Test confirming state reconstruction attacks are blocked
   - Input validation tests

#### Testing the Fix

Run the security test suite:

```bash
# Run security-specific tests
poetry run pytest tests/llm_benchmark/generator/test_gen_list_security.py -v

# Run all tests
poetry run pytest tests/
```

The test file `tests/llm_benchmark/generator/test_gen_list_security.py` includes:
- **Exploit demonstration:** Shows how the old code was predictable
- **Fix verification:** Proves the new code is cryptographically secure
- **Attack prevention:** Confirms state reconstruction attacks are blocked

---

## Security Best Practices

### Random Number Generation

**❌ NEVER use for security:**
```python
import random
random.randint(0, 100)  # Predictable!
random.choice([...])     # Predictable!
random.shuffle([...])    # Predictable!
```

**✅ ALWAYS use for security:**
```python
import secrets
secrets.randbelow(100)           # Cryptographically secure
secrets.choice([...])            # Cryptographically secure
secrets.token_hex(16)            # Cryptographically secure
secrets.token_urlsafe(16)        # Cryptographically secure
```

### When to Use Which Module

| Use Case | Module | Reason |
|----------|--------|--------|
| **Security tokens** | `secrets` | Unpredictable, cryptographically secure |
| **Passwords/keys** | `secrets` | Unpredictable, cryptographically secure |
| **Session IDs** | `secrets` | Unpredictable, cryptographically secure |
| **Lottery/gaming** | `secrets` | Fair, cannot be manipulated |
| **Test data** | `secrets` (now) | Best practice, prevents future issues |
| **Statistical simulations** | `random` | Acceptable (reproducible, not security) |
| **Monte Carlo methods** | `random` | Acceptable (performance, not security) |

---

## Secure Coding Guidelines

### Input Validation

All user-facing functions should validate inputs:

```python
def process_data(count: int, max_value: int):
    """Process data with validated inputs."""
    if count < 0:
        raise ValueError(f"count must be non-negative, got {count}")
    if max_value < 0:
        raise ValueError(f"max_value must be non-negative, got {max_value}")
    
    # Safe to proceed with validated inputs
    ...
```

### SQL Queries

Always use parameterized queries (we already do this):

```python
# ✅ SECURE - Parameterized query
cursor.execute("SELECT * FROM Album WHERE Title = ?", (name,))

# ❌ INSECURE - String interpolation (SQL injection risk)
cursor.execute(f"SELECT * FROM Album WHERE Title = '{name}'")
```

### File Operations

When working with file paths, validate and sanitize:

```python
# ✅ SECURE - Validate path
import os
from pathlib import Path

def safe_file_read(filename: str) -> str:
    base_dir = Path("/safe/directory")
    file_path = (base_dir / filename).resolve()
    
    # Ensure path is within base directory (prevent path traversal)
    if not file_path.is_relative_to(base_dir):
        raise ValueError("Path traversal attempt detected")
    
    return file_path.read_text()
```

---

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public GitHub issue
2. Contact the maintainers privately
3. Provide details about the vulnerability
4. Allow time for a fix before public disclosure

---

## Security Testing

### Running Security Tests

```bash
# Run all tests including security tests
poetry run pytest tests/ -v

# Run only security tests
poetry run pytest tests/llm_benchmark/generator/test_gen_list_security.py -v
```

### Security Test Coverage

- ✅ Random number generation security
- ✅ Input validation
- ✅ SQL injection prevention (via parameterized queries)
- ✅ State reconstruction attack prevention

---

## References

- [Python secrets module documentation](https://docs.python.org/3/library/secrets.html)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Mersenne Twister Predictability](https://en.wikipedia.org/wiki/Mersenne_Twister#Disadvantages)
- [Python random module warning](https://docs.python.org/3/library/random.html) (see Warning box)

---

## Changelog

| Date | Version | Change | Severity |
|------|---------|--------|----------|
| 2024 | 0.1.1 | Fixed insecure RNG in GenList | HIGH |
| 2024 | 0.1.1 | Added input validation to GenList | MEDIUM |
| 2024 | 0.1.1 | Added security test suite | - |
| 2024 | 0.1.0 | Initial release | - |
