#!/bin/bash     

# Import variables
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DIR/variables.sh"

# Populate BENCHMARK with the benchmark command
BENCHMARK="python -m poetry run pytest tests/ --benchmark-only --benchmark-json=artemis_raw.json && python artemis_scripts/parse_benchmark.py"
echo "Running benchmark command: $BENCHMARK"
exec $BENCHMARK