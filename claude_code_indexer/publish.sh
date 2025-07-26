#!/bin/bash
# Script to publish to PyPI

echo "📦 Building Claude Code Indexer for PyPI..."

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build
python -m build

# Check the build
echo "📋 Build contents:"
ls -la dist/

# Upload to TestPyPI first (optional)
echo "🧪 Upload to TestPyPI? (y/n)"
read -r response
if [[ "$response" == "y" ]]; then
    python -m twine upload --repository testpypi dist/*
    echo "Test with: pip install -i https://test.pypi.org/simple/ claude-code-indexer"
fi

# Upload to PyPI
echo "🚀 Upload to PyPI? (y/n)"
read -r response
if [[ "$response" == "y" ]]; then
    python -m twine upload dist/*
    echo "✅ Published! Install with: pip install claude-code-indexer"
fi