#!/bin/bash     

# Import variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/variables.sh"

# Populate BENCHMARK with the benchmark command
BENCHMARK="poetry run pytest --benchmark-only tests/"
echo "Running benchmark command: $BENCHMARK"
eval $BENCHMARK
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Error: Benchmark command failed with exit code $exit_code" >&2
    exit $exit_code
fi
exit 0
