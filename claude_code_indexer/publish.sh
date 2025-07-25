#!/bin/bash
# Main publish script with essential tests
# For quick publish without tests, use publish-quick.sh

set -e

echo "🚀 Claude Code Indexer - Pre-publish Checklist"
echo "============================================="

# Colors
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

# 1. Check syntax errors
echo -e "\n${YELLOW}Step 1: Checking for syntax errors...${NC}"
python -m py_compile claude_code_indexer/*.py
check_step $? "No syntax errors found"

# 2. Run MCP tests (most critical)
echo -e "\n${YELLOW}Step 2: Running MCP tests...${NC}"
python -m pytest tests/test_mcp_tools.py -v --no-cov -x
check_step $? "MCP tests passed"

# 3. Run basic CLI tests
echo -e "\n${YELLOW}Step 3: Running basic CLI tests...${NC}"
python -m pytest tests/test_cli.py::TestCLI::test_cli_version tests/test_cli.py::TestCLI::test_cli_help -v
check_step $? "Basic CLI tests passed"

# 4. Check version number
echo -e "\n${YELLOW}Step 4: Version check...${NC}"
CURRENT_VERSION=$(grep "version = " pyproject.toml | cut -d'"' -f2)
echo "Current version: $CURRENT_VERSION"
read -p "Is this the correct version? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Please update version in pyproject.toml first${NC}"
    exit 1
fi

# 5. Clean build artifacts
echo -e "\n${YELLOW}Step 5: Cleaning old build artifacts...${NC}"
rm -rf dist/ build/ *.egg-info
check_step $? "Build artifacts cleaned"

# 6. Build packages
echo -e "\n${YELLOW}Step 6: Building packages...${NC}"
python -m build
check_step $? "Packages built successfully"

# 7. Final confirmation
echo -e "\n${YELLOW}Ready to publish version $CURRENT_VERSION to PyPI${NC}"
echo "This will make the release public and cannot be undone."
read -p "Are you sure you want to continue? (yes/no) " -r
if [[ ! $REPLY == "yes" ]]; then
    echo -e "${RED}Publishing cancelled${NC}"
    exit 1
fi

# 8. Upload to PyPI
echo -e "\n${YELLOW}Publishing to PyPI...${NC}"
python -m twine upload dist/*
check_step $? "Successfully published to PyPI"

echo -e "\n${GREEN}🎉 Successfully published claude-code-indexer v$CURRENT_VERSION!${NC}"
echo -e "${GREEN}Users can now update with: pip install --upgrade claude-code-indexer${NC}"