#!/bin/bash
# Tool Installation Verification Script
# This script verifies that all security analysis tools are installed and accessible

set -e  # Exit on any error

echo "=================================================="
echo "Security Tool Installation Verification"
echo "=================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
FAILED=0

echo "Step 1: Updating lock file with all dependencies..."
echo "Command: poetry lock"
poetry lock
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ poetry lock completed successfully${NC}"
else
    echo -e "${RED}✗ poetry lock failed${NC}"
    FAILED=1
fi
echo ""

echo "Step 2: Installing all dependencies including dev tools..."
echo "Command: poetry install"
poetry install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ poetry install completed successfully${NC}"
else
    echo -e "${RED}✗ poetry install failed${NC}"
    FAILED=1
fi
echo ""

echo "Step 3: Verifying individual tools..."
echo ""

# Array of tools to verify
declare -a TOOLS=("mypy" "bandit" "pylint" "pip-audit")
TOOL_COUNT=0
SUCCESS_COUNT=0

for tool in "${TOOLS[@]}"; do
    TOOL_COUNT=$((TOOL_COUNT + 1))
    echo -n "Checking $tool... "
    
    if poetry run $tool --version > /dev/null 2>&1; then
        VERSION=$(poetry run $tool --version 2>&1)
        echo -e "${GREEN}✓ OK${NC}"
        echo "  Version: $VERSION"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED=1
    fi
done
echo ""

echo "=================================================="
echo "Verification Summary"
echo "=================================================="
echo "Tools verified: $SUCCESS_COUNT/$TOOL_COUNT"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tools installed and accessible!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tools failed verification${NC}"
    exit 1
fi
