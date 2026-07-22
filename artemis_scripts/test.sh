#!/bin/bash     

# Import variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/variables.sh"

echo "Running test command: poetry run pytest --benchmark-skip tests/"
poetry run pytest --benchmark-skip tests/
