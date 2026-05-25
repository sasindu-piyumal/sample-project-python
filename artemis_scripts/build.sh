#!/bin/bash     

# Import variables
DIR="$(cd "${BASH_SOURCE[0]%/*}" 2>/dev/null && pwd || pwd)"
source "$DIR/variables.sh"

# Populate BUILD with the build command
BUILD="poetry install"
echo "Running build command: $BUILD"
$BUILD