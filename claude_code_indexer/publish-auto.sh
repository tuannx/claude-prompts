#!/bin/bash
# Automated publish script (no prompts)
# Use this for CI/CD or when you're sure about publishing

set -e

echo "🚀 Claude Code Indexer - Automated Publish"
echo "========================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get version
VERSION=$(grep "version = " pyproject.toml | cut -d'"' -f2)
echo -e "${YELLOW}Publishing version: $VERSION${NC}"

# 1. Check syntax
echo -e "\n${YELLOW}Checking syntax...${NC}"
python -m py_compile claude_code_indexer/*.py
echo -e "${GREEN}✅ No syntax errors${NC}"

# 2. Run essential tests
echo -e "\n${YELLOW}Running MCP tests...${NC}"
python -m pytest tests/test_mcp_tools.py -v --no-cov -x
echo -e "${GREEN}✅ MCP tests passed${NC}"

# 3. Clean and build
echo -e "\n${YELLOW}Building packages...${NC}"
rm -rf dist/ build/ *.egg-info
python -m build
echo -e "${GREEN}✅ Build complete${NC}"

# 4. Upload to PyPI
echo -e "\n${YELLOW}Uploading to PyPI...${NC}"
python -m twine upload dist/*
echo -e "\n${GREEN}🎉 Successfully published claude-code-indexer v$VERSION!${NC}"
echo -e "${GREEN}View at: https://pypi.org/project/claude-code-indexer/$VERSION/${NC}"