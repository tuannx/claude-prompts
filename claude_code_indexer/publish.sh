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

# Show what will be uploaded
echo "📦 Files to upload:"
ls -la dist/

# Confirm
read -p "Upload to PyPI? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Upload cancelled"
    exit 1
fi

# Upload
echo "📤 Uploading to PyPI..."
python -m twine upload \
    --username __token__ \
    --password "$PYPI_TOKEN" \
    dist/*

echo "✅ Upload complete!"
echo ""
echo "🎉 Package published successfully!"
echo "Install with: pip install claude-code-indexer"