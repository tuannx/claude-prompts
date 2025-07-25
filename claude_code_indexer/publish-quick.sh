#!/bin/bash
# Quick publish script - minimal checks for urgent releases
# For full testing, use publish.sh

set -e

echo "🚀 Claude Code Indexer - Quick Publish"
echo "===================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Check syntax
echo -e "\n${YELLOW}Checking Python syntax...${NC}"
python -m py_compile claude_code_indexer/*.py
echo -e "${GREEN}✅ No syntax errors${NC}"

# 2. Check version
VERSION=$(grep "version = " pyproject.toml | cut -d'"' -f2)
echo -e "\n${YELLOW}Version: $VERSION${NC}"
read -p "Continue with this version? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# 3. Clean and build
echo -e "\n${YELLOW}Building...${NC}"
rm -rf dist/ build/
python -m build
echo -e "${GREEN}✅ Build complete${NC}"

# 4. Final confirmation
echo -e "\n${RED}⚠️  WARNING: This skips most tests!${NC}"
echo "For full testing, use ./publish.sh"
read -p "Publish to PyPI? (yes/no) " -r
if [[ ! $REPLY == "yes" ]]; then
    exit 1
fi

# 5. Upload
echo -e "\n${YELLOW}Publishing...${NC}"
python -m twine upload dist/*
echo -e "\n${GREEN}✅ Published successfully!${NC}"