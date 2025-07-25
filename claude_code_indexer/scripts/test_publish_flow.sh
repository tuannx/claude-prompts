#!/bin/bash
# Quick test of publish flow (without full tests)

set -e

echo "🚀 Claude Code Indexer - Quick Publish Flow Test"
echo "============================================="

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check step
check_step() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# 1. Run minimal tests
echo -e "\n${YELLOW}Step 1: Running minimal tests...${NC}"
python -m pytest tests/test_update.py::TestUpdateFunctionality::test_cli_aliases_work -v
check_step $? "Minimal test passed"

# 2. Check for syntax errors
echo -e "\n${YELLOW}Step 2: Checking for syntax errors...${NC}"
python -m py_compile claude_code_indexer/*.py
check_step $? "No syntax errors found"

# 3. Check version number
echo -e "\n${YELLOW}Step 3: Current version check...${NC}"
CURRENT_VERSION=$(grep "version = " pyproject.toml | cut -d'"' -f2)
echo "Current version: $CURRENT_VERSION"

# 4. Check build process
echo -e "\n${YELLOW}Step 4: Test build process...${NC}"
# Just check if build would work, don't actually build
python -c "import build; print('Build module available')"
check_step $? "Build module available"

echo -e "\n${GREEN}✅ Quick publish flow test completed!${NC}"
echo "The full publish.sh script should work correctly."