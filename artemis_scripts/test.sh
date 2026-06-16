#!/bin/bash     

# Import variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/variables.sh"

# Populate TEST with the test command
TEST="poetry run pytest --benchmark-skip tests/"
echo "Running test command: $TEST"
eval $TEST
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Error: Test command failed with exit code $exit_code" >&2
    exit $exit_code
fi
exit 0
