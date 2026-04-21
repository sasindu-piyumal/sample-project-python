#!/bin/bash

# Import variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/variables.sh"

# Run bandit static analysis
BANDIT="poetry run bandit -c pyproject.toml -r src/"
echo "Running security command: $BANDIT"
eval $BANDIT
BANDIT_EXIT=$?

# Run pip-audit vulnerability scan
PIP_AUDIT="poetry run pip-audit"
echo "Running security command: $PIP_AUDIT"
eval $PIP_AUDIT
PIP_AUDIT_EXIT=$?

# Fail if either tool reported a finding
if [ $BANDIT_EXIT -ne 0 ] || [ $PIP_AUDIT_EXIT -ne 0 ]; then
    exit 1
fi
