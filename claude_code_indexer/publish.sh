#!/bin/bash
# Publish script for claude-code-indexer

set -e

echo "🚀 Publishing claude-code-indexer to PyPI"
echo "========================================="

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "❌ dist/ directory not found. Building package..."
    python -m build
fi

# Check for API token
if [ -z "$PYPI_TOKEN" ]; then
    echo "❌ PYPI_TOKEN environment variable not set"
    echo "Please set: export PYPI_TOKEN=pypi-YOUR-TOKEN-HERE"
    exit 1
fi

# Get the latest version from pyproject.toml
VERSION=$(grep "^version" pyproject.toml | cut -d'"' -f2)
echo "📌 Current version: $VERSION"

# Show what will be uploaded
echo "📦 Files in dist/:"
ls -la dist/

# Check if old versions exist
OLD_FILES=$(ls dist/ | grep -v "$VERSION" | wc -l)
if [ "$OLD_FILES" -gt 0 ]; then
    echo ""
    echo "⚠️  Found old version files in dist/"
    read -p "Clean old versions? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🧹 Cleaning old versions..."
        find dist/ -type f ! -name "*${VERSION}*" -delete
        echo "✅ Old versions removed"
    fi
fi

echo ""
echo "📦 Files to upload:"
ls -la dist/claude_code_indexer-${VERSION}*

# Confirm
read -p "Upload to PyPI? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Upload cancelled"
    exit 1
fi

# Upload only the current version
echo "📤 Uploading version $VERSION to PyPI..."
python -m twine upload \
    --username __token__ \
    --password "$PYPI_TOKEN" \
    dist/claude_code_indexer-${VERSION}*

echo "✅ Upload complete!"
echo ""
echo "🎉 Package published successfully!"
echo "Install with: pip install claude-code-indexer"