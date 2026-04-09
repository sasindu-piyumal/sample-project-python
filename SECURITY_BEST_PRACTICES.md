# Security Best Practices for llm-benchmarking-py

This document provides security guidelines and best practices for developers working on the llm-benchmarking-py project. It establishes consistent patterns for input validation, error handling, logging, and database access throughout the codebase.

**Audience:** Developers and code reviewers  
**Last Updated:** 2024  
**Related Documents:** [SECURITY.md](./SECURITY.md)

---

## Table of Contents

1. [Core Security Principles](#core-security-principles)
2. [Input Validation](#input-validation)
3. [Error Handling](#error-handling)
4. [Logging Security](#logging-security)
5. [Database Access](#database-access)
6. [Type Checking](#type-checking)
7. [Environment & Configuration](#environment--configuration)
8. [Code Review Checklist](#code-review-checklist)

---

## Core Security Principles

Security in this project is built on four key principles:

1. **Defense in Depth:** Validate at entry points, handle errors gracefully, and never trust input
2. **Fail Safely:** Errors should not expose sensitive information or leave the system in an unsafe state
3. **Type Safety:** Use type hints and mypy to catch errors early
4. **Audit Trail:** Log security-relevant events while protecting sensitive data

All code should reflect these principles through:
- Input validation before processing
- Explicit error handling with appropriate logging
- Type hints on all function signatures
- Parameterized queries for database access
- Sensitive data protection in logs

---

## Input Validation

### Principle: Never Trust Input

All external input must be validated before use, including:
- Function parameters from external sources
- User input
- Configuration values
- Query parameters

### Type Checking: The First Line of Defense

Use Python type hints on all function parameters and return types:

```python
# ✅ CORRECT: Type hints on all parameters
def max_list(v: List[int]) -> int:
    """Find maximum value in a list."""
    if not v:
        raise ValueError("max_list() arg is an empty sequence")
    return max(v)

# ❌ INCORRECT: Missing type hints
def max_list(v):
    """Find maximum value in a list."""
    return max(v)  # What if v is None? What if it's not a list?
```

*From: `src/llm_benchmark/control/single.py`*

### Bounds Checking: Validate Numeric Ranges

Always validate that numeric inputs are within acceptable ranges:

```python
# ✅ CORRECT: Bounds checking with informative error message
@staticmethod
def sum_range(n: int) -> int:
    """Sum of numbers from 0 to n inclusive.
    
    Args:
        n (int): Number to sum up to, inclusive.
    
    Returns:
        int: Sum of integers from 0 to n inclusive.
    
    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return n * (n + 1) // 2

# ❌ INCORRECT: No bounds checking
@staticmethod
def sum_range(n: int) -> int:
    """Sum of numbers from 0 to n inclusive."""
    return n * (n + 1) // 2  # What if n is negative? Integer overflow?
```

*From: `src/llm_benchmark/control/single.py`*

### Empty/Null Checking: Handle Edge Cases

Always check for empty or None values:

```python
# ✅ CORRECT: Explicit check for empty list
@staticmethod
def max_list(v: List[int]) -> int:
    """Maximum value in a vector."""
    if not v:
        raise ValueError("max_list() arg is an empty sequence")
    return max(v)

# ❌ INCORRECT: No empty check
@staticmethod
def max_list(v: List[int]) -> int:
    """Maximum value in a vector."""
    return max(v)  # Crashes with cryptic error if v is empty
```

*From: `src/llm_benchmark/control/single.py`*

### Divisor/Denominator Validation

Always validate divisors before use:

```python
# ✅ CORRECT: Let Python raise ZeroDivisionError naturally
@staticmethod
def sum_modulus(n: int, m: int) -> int:
    """Sum of modulus i % m for i in the inclusive range 0..n.
    
    Args:
        n (int): Number to sum up to (inclusive)
        m (int): Modulus (non-zero)
    
    Raises:
        ZeroDivisionError: If m == 0
    """
    return sum(i % m for i in range(n + 1))

# ❌ INCORRECT: Silent failure or undefined behavior
@staticmethod
def sum_modulus(n: int, m: int) -> int:
    """Sum of modulus i % m for i in the inclusive range 0..n."""
    if m == 0:
        return 0  # Silent failure - wrong result!
    return sum(i % m for i in range(n + 1))
```

*From: `src/llm_benchmark/control/single.py`*

### String Validation

For string inputs, validate format, length, and content:

```python
# ✅ CORRECT: Type hint specifies string, validation at entry point
@staticmethod
def query_album(name: str) -> bool:
    """Check if an album exists.
    
    Args:
        name (str): Name of the album
    
    Returns:
        bool: True if the album exists, False otherwise
    """
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        # Always use parameterized queries for string input (see Database Access section)
        cur.execute(
            "SELECT 1 FROM Album WHERE Title = ? LIMIT 1",
            (name,),
        )
        return cur.fetchone() is not None

# ❌ INCORRECT: No validation, vulnerable to SQL injection
@staticmethod
def query_album(name: str) -> bool:
    """Check if an album exists."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        # DANGER: String concatenation allows SQL injection!
        cur.execute(f"SELECT 1 FROM Album WHERE Title = '{name}' LIMIT 1")
        return cur.fetchone() is not None
```

*From: `src/llm_benchmark/sql/query.py`*

### Collection Size Validation

Check collection sizes to prevent resource exhaustion:

```python
# ✅ CORRECT: Matrix size is validated implicitly by reasonable inputs
@staticmethod
def random_matrix(n: int, m: int) -> List[List[int]]:
    """Generate a matrix of random integers.
    
    Args:
        n (int): Number of rows
        m (int): Number of columns
    
    Returns:
        List[List[int]]: Matrix of random integers
    """
    # In production, add explicit bounds:
    # if n > MAX_MATRIX_ROWS or m > MAX_MATRIX_COLS:
    #     raise ValueError(f"Matrix size exceeds limits: {n}x{m}")
    return [GenList.random_list(n, m) for _ in range(n)]

# ⚠️  BEST PRACTICE: Add size limits for production systems
MAX_MATRIX_ROWS = 10000
MAX_MATRIX_COLS = 10000

@staticmethod
def random_matrix_safe(n: int, m: int) -> List[List[int]]:
    """Generate a matrix with size validation."""
    if n <= 0 or m <= 0:
        raise ValueError("Matrix dimensions must be positive")
    if n > MAX_MATRIX_ROWS or m > MAX_MATRIX_COLS:
        raise ValueError(
            f"Matrix size {n}x{m} exceeds maximum {MAX_MATRIX_ROWS}x{MAX_MATRIX_COLS}"
        )
    return [GenList.random_list(n, m) for _ in range(n)]
```

*From: `src/llm_benchmark/generator/gen_list.py`*

### Prime Number Bounds

Always validate prime number inputs:

```python
# ✅ CORRECT: Bounds checking on prime operations
@staticmethod
def is_prime(n: int) -> bool:
    """Check if a number is prime using trial division.
    
    Args:
        n: The number to check for primality.
    
    Returns:
        True if the number is prime, False otherwise.
    """
    if n < 2:
        return False  # By definition, numbers < 2 are not prime
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

# ❌ INCORRECT: No bounds checking
@staticmethod
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    for i in range(2, n):
        if n % i == 0:
            return False
    return True  # What if n is -5? Returns True (wrong!)
```

*From: `src/llm_benchmark/algorithms/primes.py`*

---

## Error Handling

### Principle: Fail Fast, Fail Safely

Handle errors explicitly. Don't suppress exceptions unless you understand why.

### Raising Exceptions: When and How

Use exceptions for error conditions, not control flow:

```python
# ✅ CORRECT: Exceptions for error conditions
@staticmethod
def sum_range(n: int) -> int:
    """Sum of numbers from 0 to n inclusive.
    
    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return n * (n + 1) // 2

# ❌ INCORRECT: Exceptions for control flow
@staticmethod
def sum_range(n: int) -> int:
    """Sum of numbers from 0 to n inclusive."""
    try:
        return n * (n + 1) // 2
    except:  # Don't catch exceptions you didn't raise!
        return 0

# ❌ INCORRECT: Silently returning wrong value
@staticmethod
def sum_range(n: int) -> int:
    """Sum of numbers from 0 to n inclusive."""
    if n < 0:
        return 0  # Caller doesn't know about the error!
    return n * (n + 1) // 2
```

*From: `src/llm_benchmark/control/single.py`*

### Exception Messages: Informative, Not Leaky

Exception messages should be informative but never expose sensitive information:

```python
# ✅ CORRECT: Clear, specific, no sensitive data exposed
try:
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Album WHERE Title = ?", (album_name,))
        return cur.fetchall()
except sqlite3.DatabaseError as e:
    logger.error("Failed to query albums: database error")  # Don't log the exception details
    raise ValueError("Unable to retrieve album data") from None  # Hide the original error

# ❌ INCORRECT: Exposes full error details
try:
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Album WHERE Title = '{album_name}'")  # SQL injection!
        return cur.fetchall()
except sqlite3.DatabaseError as e:
    raise ValueError(f"Database error: {e}") from e  # Exposes the error to the caller
```

### Handling Multiple Error Types

Catch specific exceptions, not generic ones:

```python
# ✅ CORRECT: Specific exception handling
def process_album_list(album_names: List[str]) -> List[bool]:
    """Check multiple albums."""
    results = []
    for name in album_names:
        try:
            exists = SqlQuery.query_album(name)
            results.append(exists)
        except ValueError as e:
            logger.warning(f"Invalid album name: {name}")
            results.append(False)
        except sqlite3.DatabaseError as e:
            logger.error("Database connection failed")
            raise
    return results

# ❌ INCORRECT: Bare except silences all errors
def process_album_list(album_names: List[str]) -> List[bool]:
    """Check multiple albums."""
    results = []
    for name in album_names:
        try:
            exists = SqlQuery.query_album(name)
            results.append(exists)
        except:  # Catches everything - bad practice!
            results.append(False)
    return results
```

### Exit Codes and Error Returns

For main program entry points, use appropriate exit codes:

```python
# ✅ CORRECT: Use exit codes to signal error conditions
def main():
    """Main entry point."""
    try:
        single()
        double()
        sql()
        primes()
        sort()
        dslist()
        strops()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error in main: {type(e).__name__}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())

# ❌ INCORRECT: Silent failure
def main():
    try:
        single()
        double()
        sql()
    except:
        pass  # Silently fails - caller doesn't know what happened
```

*From: `src/llm_benchmark/main.py`*

---

## Logging Security

### Principle: Log Enough to Debug, Not Enough to Compromise Security

Logging is essential for debugging and security monitoring, but logs can be a security risk if they contain sensitive data.

### What CAN Be Logged Safely

```python
import logging

logger = logging.getLogger(__name__)

# ✅ CORRECT: Safe to log
logger.info("Starting algorithm execution")
logger.info(f"Processed {count} items")
logger.info("Database query completed successfully")
logger.debug(f"Algorithm took {elapsed_time}ms")
logger.warning("Input validation failed for album name")
logger.error("Failed to connect to database")
```

### What CANNOT Be Logged

```python
import logging

logger = logging.getLogger(__name__)

# ❌ INCORRECT: Don't log sensitive data
def query_user(username: str, password: str):
    logger.info(f"Authenticating user: {username}")  # OK
    logger.debug(f"Password: {password}")  # NEVER LOG PASSWORDS!
    logger.info(f"User {username} connected from {ip_address}")  # OK if IP is logged separately
    logger.error(f"Query failed: {sql_error_message}")  # May contain sensitive info

# ❌ INCORRECT: Don't log full database errors
try:
    result = execute_query(sql_statement)
except DatabaseError as e:
    logger.error(f"Query failed: {e}")  # May expose schema, column names, etc.
```

### Logging Configuration Best Practice

The project uses centralized logging configuration in main.py:

```python
# ✅ CORRECT: Centralized logging configuration (from main.py)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Initialize root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Configure FileHandler
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "main.log"))
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Configure StreamHandler (console output)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

logger.info("Logging infrastructure initialized")
```

### Module-Level Logging Pattern

Use module-level loggers in each module:

```python
# ✅ CORRECT: Module-level logger pattern
import logging

logger = logging.getLogger(__name__)

class SqlQuery:
    @staticmethod
    def query_album(name: str) -> bool:
        """Check if an album exists."""
        try:
            with sqlite3.connect("data/chinook.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT 1 FROM Album WHERE Title = ? LIMIT 1",
                    (name,),
                )
                result = cur.fetchone() is not None
                if result:
                    logger.debug(f"Album found in database")
                return result
        except sqlite3.DatabaseError as e:
            logger.error("Database connection failed")
            raise
```

### Log Levels Guide

Use appropriate log levels:

- **DEBUG:** Detailed information for diagnosing problems (algorithm iterations, loop counts)
- **INFO:** General informational messages (program start/stop, major operations)
- **WARNING:** Warning messages (unusual but non-critical conditions)
- **ERROR:** Error messages (failures that prevent an operation, but not fatal)
- **CRITICAL:** Critical messages (failures that prevent the program from running)

```python
import logging

logger = logging.getLogger(__name__)

def process_list(items: List[int]) -> int:
    """Process a list and return the sum."""
    logger.debug(f"Processing {len(items)} items")  # DEBUG
    
    if not items:
        logger.warning("Empty list provided to process_list")  # WARNING
        return 0
    
    try:
        result = sum(items)
        logger.info("List processing completed successfully")  # INFO
        return result
    except OverflowError as e:
        logger.error("Integer overflow during sum calculation")  # ERROR
        raise
    except Exception as e:
        logger.critical(f"Unexpected error: {type(e).__name__}")  # CRITICAL
        raise
```

---

## Database Access

### Principle: Always Use Parameterized Queries

SQL injection is one of the most critical security vulnerabilities. Use parameterized queries exclusively.

### Parameterized Queries: The Right Way

```python
import sqlite3

# ✅ CORRECT: Parameterized query with placeholders
@staticmethod
def query_album(name: str) -> bool:
    """Check if an album exists.
    
    Args:
        name (str): Name of the album
    
    Returns:
        bool: True if the album exists, False otherwise
    """
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        # Use ? placeholders and pass parameters as a tuple
        cur.execute(
            "SELECT 1 FROM Album WHERE Title = ? LIMIT 1",
            (name,),  # Parameters passed separately
        )
        return cur.fetchone() is not None

# ❌ INCORRECT: String concatenation (SQL Injection vulnerability!)
@staticmethod
def query_album(name: str) -> bool:
    """Check if an album exists."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        # DANGER: Allows SQL injection if name contains quotes or SQL commands
        cur.execute(f"SELECT 1 FROM Album WHERE Title = '{name}' LIMIT 1")
        return cur.fetchone() is not None

# Attack example:
# album_name = "x' OR '1'='1"
# String concatenation: SELECT 1 FROM Album WHERE Title = 'x' OR '1'='1' LIMIT 1
# This returns all albums! Parameterized query would search for the literal string.
```

*From: `src/llm_benchmark/sql/query.py`*

### Parameterized Multi-Parameter Queries

```python
# ✅ CORRECT: Multiple parameters
@staticmethod
def join_albums() -> list:
    """Join the Album, Artist, and Track tables."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        cur.execute(
            """\
            SELECT 
                t.Name AS TrackName,
                a.Title AS AlbumName,
                ar.Name AS ArtistName
            FROM 
                Track t
            JOIN Album a ON a.AlbumId = t.AlbumId
            JOIN Artist ar ON ar.ArtistId = a.ArtistId
            """
        )
        return cur.fetchall()

# ✅ CORRECT: With WHERE clause parameters
@staticmethod
def query_by_artist_and_year(artist_name: str, year: int) -> list:
    """Query tracks by artist and year."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        cur.execute(
            """\
            SELECT t.Name
            FROM Track t
            JOIN Album a ON a.AlbumId = t.AlbumId
            JOIN Artist ar ON ar.ArtistId = a.ArtistId
            WHERE ar.Name = ? AND strftime('%Y', a.ReleaseDate) = ?
            """,
            (artist_name, str(year)),  # Both parameters here
        )
        return cur.fetchall()

# ❌ INCORRECT: Only partially parameterized
@staticmethod
def query_by_artist_and_year(artist_name: str, year: int) -> list:
    """Query tracks by artist and year."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        cur.execute(
            f"""\
            SELECT t.Name
            FROM Track t
            JOIN Album a ON a.AlbumId = t.AlbumId
            JOIN Artist ar ON ar.ArtistId = a.ArtistId
            WHERE ar.Name = ? AND strftime('%Y', a.ReleaseDate) = '{year}'
            """,
            (artist_name,),  # Only artist parameterized, year is not!
        )
        return cur.fetchall()
```

### Database Connection Management

Always use context managers for database connections:

```python
# ✅ CORRECT: Context manager ensures connection is closed
@staticmethod
def top_invoices() -> list:
    """Get the top 10 invoices by total."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        cur.execute(
            """\
            SELECT 
                i.InvoiceId, 
                c.FirstName || ' ' || c.LastName AS CustomerName, 
                i.Total
            FROM 
                Invoice i
            JOIN Customer c ON c.CustomerId = i.CustomerId
            ORDER BY i.Total DESC
            LIMIT 10
            """
        )
        return cur.fetchall()
    # Connection automatically closed here, even if exception occurs

# ❌ INCORRECT: Manual connection management
@staticmethod
def top_invoices() -> list:
    """Get the top 10 invoices by total."""
    conn = sqlite3.connect("data/chinook.db")
    cur = conn.cursor()
    
    cur.execute("SELECT ...")
    result = cur.fetchall()
    
    conn.close()  # What if an exception occurs above?
    return result
```

*From: `src/llm_benchmark/sql/query.py`*

### Result Set Handling

Always limit results to prevent resource exhaustion:

```python
# ✅ CORRECT: LIMIT clause in query
@staticmethod
def top_invoices() -> list:
    """Get the top 10 invoices by total."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        cur.execute(
            """\
            SELECT 
                i.InvoiceId, 
                c.FirstName || ' ' || c.LastName AS CustomerName, 
                i.Total
            FROM 
                Invoice i
            JOIN Customer c ON c.CustomerId = i.CustomerId
            ORDER BY i.Total DESC
            LIMIT 10
            """
        )
        return cur.fetchall()

# ❌ INCORRECT: Unbounded query
@staticmethod
def all_invoices() -> list:
    """Get all invoices."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM Invoice")  # No LIMIT!
        return cur.fetchall()  # Could be millions of rows
```

---

## Type Checking

### Principle: Use Type Hints Everywhere

Type hints are not just documentation; they enable static analysis tools to catch errors before runtime.

### Function Signatures

Always include type hints on:
- All parameters
- Return types
- Imported types from `typing` module

```python
from typing import List

# ✅ CORRECT: Complete type hints
@staticmethod
def modify_list(v: List[int]) -> List[int]:
    """Modify a list by adding 1 to each element.
    
    Args:
        v (List[int]): List of integers
    
    Returns:
        List[int]: Modified list of integers
    """
    ret = []
    for i in range(len(v)):
        ret.append(v[i] + 1)
    return ret

# ❌ INCORRECT: Missing type hints
@staticmethod
def modify_list(v):
    """Modify a list by adding 1 to each element."""
    ret = []
    for i in range(len(v)):
        ret.append(v[i] + 1)
    return ret
```

*From: `src/llm_benchmark/datastructures/dslist.py`*

### Complex Types

Use the `typing` module for complex types:

```python
from typing import List, Dict, Optional, Tuple

# ✅ CORRECT: Using typing module for clarity
@staticmethod
def count_duplicates(arr0: List[int], arr1: List[int]) -> int:
    """Count duplicates between two arrays.
    
    Args:
        arr0 (List[int]): Array of integers
        arr1 (List[int]): Array of integers
    
    Returns:
        int: Total count of elements that appear in both arrays
    """
    if not arr0 or not arr1:
        return 0
    c0 = Counter(arr0)
    c1 = Counter(arr1)
    return sum(min(c0[k], c1[k]) for k in c0.keys() & c1.keys())

# ❌ INCORRECT: Unclear types
@staticmethod
def count_duplicates(arr0, arr1):
    """Count duplicates between two arrays."""
    if not arr0 or not arr1:
        return 0
    c0 = Counter(arr0)
    c1 = Counter(arr1)
    return sum(min(c0[k], c1[k]) for k in c0.keys() & c1.keys())
```

*From: `src/llm_benchmark/control/double.py`*

### Mypy Configuration

The project includes mypy configuration for type checking:

```bash
# Run mypy to check types
mypy src/

# Run mypy with strict settings
mypy --strict src/
```

Configure mypy in `pyproject.toml` for consistent enforcement:

```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true
```

### Optional Types

Use `Optional` for values that might be None:

```python
from typing import Optional

# ✅ CORRECT: Optional for nullable types
@staticmethod
def find_album(name: str) -> Optional[Dict[str, str]]:
    """Find an album by name.
    
    Args:
        name (str): Album name to search for
    
    Returns:
        Optional[Dict[str, str]]: Album data if found, None otherwise
    """
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT AlbumId, Title FROM Album WHERE Title = ?",
            (name,),
        )
        row = cur.fetchone()
        if row:
            return {"id": row[0], "title": row[1]}
        return None

# ❌ INCORRECT: No indication that None is possible
@staticmethod
def find_album(name: str) -> Dict[str, str]:
    """Find an album by name."""
    with sqlite3.connect("data/chinook.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT AlbumId, Title FROM Album WHERE Title = ?",
            (name,),
        )
        row = cur.fetchone()
        if row:
            return {"id": row[0], "title": row[1]}
        return None  # Type checker won't catch this mismatch!
```

---

## Environment & Configuration

### Principle: Never Hardcode Secrets or Configuration

Configuration should be environment-specific and external to the code.

### Environment Variables

Use environment variables for configuration that changes between environments:

```python
import os
from pathlib import Path

# ✅ CORRECT: Configuration from environment
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/chinook.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
MAX_QUERY_RESULTS = int(os.getenv("MAX_QUERY_RESULTS", "1000"))

# ✅ CORRECT: Secrets from environment (never hardcoded)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
if DATABASE_PASSWORD is None:
    raise ValueError("DATABASE_PASSWORD environment variable not set")

# ❌ INCORRECT: Hardcoded configuration
DATABASE_PATH = "data/chinook.db"
DEBUG = True
DATABASE_PASSWORD = "super_secret_password_123"  # NEVER DO THIS!
```

### Configuration Files

For complex configurations, use external config files (not in git):

```python
import json
from pathlib import Path

# ✅ CORRECT: Loading from external config file
def load_config(config_path: str = ".env.json") -> dict:
    """Load configuration from external file.
    
    Args:
        config_path (str): Path to configuration file
    
    Returns:
        dict: Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path) as f:
        config = json.load(f)
    
    # Validate required keys
    required_keys = ["database_path", "log_level"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    return config
```

### Logging Configuration from Environment

```python
import logging
import os

# ✅ CORRECT: Logging configuration from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Initialize root logger
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Configure FileHandler
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "main.log"))
file_handler.setLevel(LOG_LEVEL)
file_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Configure StreamHandler (console output)
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

logger.info(f"Logging infrastructure initialized with level {LOG_LEVEL}")
```

*From: `src/llm_benchmark/main.py`*

---

## Code Review Checklist

Use this checklist when reviewing code for security:

### Input Validation
- [ ] All function parameters have type hints
- [ ] Numeric inputs are validated for appropriate ranges
- [ ] Empty/None values are explicitly checked
- [ ] String inputs are never used in string concatenation with SQL or shell commands
- [ ] Collection sizes are bounded where appropriate

### Error Handling
- [ ] Errors raise appropriate, specific exceptions
- [ ] Exception messages don't expose sensitive information
- [ ] All resources (files, connections) are properly cleaned up (use context managers)
- [ ] No bare `except:` clauses

### Logging
- [ ] Sensitive data (passwords, keys, tokens) is never logged
- [ ] Error messages provide useful information without exposing internals
- [ ] Appropriate log levels are used (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- [ ] Logging is configured centrally

### Database Access
- [ ] All SQL queries use parameterized queries with placeholders
- [ ] No string concatenation in SQL queries
- [ ] Database connections use context managers (`with` statement)
- [ ] Query results are limited appropriately

### Type Checking
- [ ] All function parameters have type hints
- [ ] All return types are specified
- [ ] Complex types use `typing` module (`List`, `Dict`, `Optional`, etc.)
- [ ] Code passes `mypy --strict` checks

### Environment & Configuration
- [ ] Secrets are never hardcoded
- [ ] Configuration is environment-specific
- [ ] Sensitive settings come from environment variables
- [ ] Configuration files are in `.gitignore`

---

## Quick Reference: Common Patterns

### Safe Function Template

```python
from typing import List
import logging

logger = logging.getLogger(__name__)

class SafeAlgorithm:
    @staticmethod
    def safe_function(items: List[int], limit: int) -> int:
        """Process items with proper validation and error handling.
        
        Args:
            items (List[int]): List of integers to process
            limit (int): Maximum allowed value
        
        Returns:
            int: Processing result
        
        Raises:
            ValueError: If inputs are invalid
        """
        # 1. Validate inputs
        if not items:
            raise ValueError("items cannot be empty")
        if limit <= 0:
            raise ValueError("limit must be positive")
        if limit > 10000:
            raise ValueError(f"limit {limit} exceeds maximum of 10000")
        
        # 2. Log entry
        logger.debug(f"Processing {len(items)} items with limit {limit}")
        
        # 3. Process safely
        try:
            result = sum(x for x in items if x <= limit)
            logger.info("Processing completed successfully")
            return result
        except OverflowError:
            logger.error("Integer overflow during processing")
            raise ValueError("Result exceeds integer limits") from None
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}")
            raise
```

### Safe Query Template

```python
import sqlite3
from typing import List

class SafeQuery:
    @staticmethod
    def safe_query(db_path: str, album_name: str) -> List[tuple]:
        """Execute a parameterized query safely.
        
        Args:
            db_path (str): Path to database file
            album_name (str): Album name to search for
        
        Returns:
            List[tuple]: Query results
        
        Raises:
            ValueError: If inputs are invalid
            sqlite3.DatabaseError: If query fails
        """
        # 1. Validate inputs
        if not album_name:
            raise ValueError("album_name cannot be empty")
        if not Path(db_path).exists():
            raise ValueError(f"Database not found: {db_path}")
        
        # 2. Execute parameterized query
        try:
            with sqlite3.connect(db_path) as conn:
                cur = conn.cursor()
                
                # Use ? placeholders - parameters passed separately
                cur.execute(
                    "SELECT * FROM Album WHERE Title = ? LIMIT 100",
                    (album_name,),  # Parameters as tuple
                )
                return cur.fetchall()
        except sqlite3.DatabaseError as e:
            logger.error("Database query failed")
            raise ValueError("Unable to retrieve data") from None
```

---

## Additional Resources

- **Related Document:** [SECURITY.md](./SECURITY.md) - Vulnerability reporting process
- **Type Checking:** [mypy Documentation](https://mypy.readthedocs.io/)
- **SQL Injection:** [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- **Logging:** [Python logging Documentation](https://docs.python.org/3/library/logging.html)
- **Type Hints:** [PEP 484](https://www.python.org/dev/peps/pep-0484/)

