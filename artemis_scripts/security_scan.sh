#!/bin/bash

# Security scanning script — runs bandit (static analysis) and pip-audit
# (dependency vulnerability check) in sequence. Exits non-zero if either
# tool reports findings.

set -e

# Import variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/variables.sh"

echo "=== Running bandit (static security analysis) against src/ ==="
poetry run bandit -r src/

echo ""
echo "=== Running pip-audit (dependency vulnerability scan) ==="
poetry run pip-audit

echo ""
echo "=== All security checks passed ==="
