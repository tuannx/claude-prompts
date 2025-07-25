#!/bin/bash
# Publish script for claude-code-indexer using .pypirc

set -e

echo "🚀 Publishing claude-code-indexer to PyPI"
echo "========================================="

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "❌ dist/ directory not found. Building package..."
    python -m build
fi

# Check if .pypirc exists
if [ ! -f ~/.pypirc ]; then
    echo "❌ ~/.pypirc not found"
    echo "Please create ~/.pypirc with your PyPI credentials"
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

# Upload using .pypirc
echo "📤 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Upload complete!"
echo ""
echo "🎉 Package published successfully!"
echo "Install with: pip install claude-code-indexer"