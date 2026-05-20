#!/bin/bash     

# Import variables
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DIR/variables.sh"

# Populate BENCHMARK with the benchmark command
BENCHMARK="poetry run pytest --benchmark-only tests/"
echo "Running benchmark command: $BENCHMARK"
exec $BENCHMARK