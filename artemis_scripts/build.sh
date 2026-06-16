#!/bin/bash     

# Import variables
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/variables.sh"

# Populate BUILD with the build command
BUILD="poetry install"
echo "Running build command: $BUILD"
eval $BUILD
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Error: Build command failed with exit code $exit_code" >&2
    exit $exit_code
fi
exit 0
