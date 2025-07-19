#!/bin/bash
# One-click AutoIt Support Installer for claude-code-indexer
# Linux/macOS Shell Script

echo "=================================================="
echo " AutoIt Support Installer for claude-code-indexer"
echo "=================================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found! Please install Python 3.8+ first."
    exit 1
fi

echo "[INFO] Python found - proceeding with installation..."
echo

# Run the simple installer
python3 simple-autoit-installer.py

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Installation failed!"
    echo "Please check the error messages above."
    exit 1
fi

echo
echo "=================================================="
echo " Installation completed successfully!"
echo "=================================================="
echo
echo "You can now use AutoIt support with:"
echo "  claude-code-indexer index /path/to/autoit/project"
echo "  claude-code-indexer query --important"
echo
echo "Supported file types: .au3, .aut, .a3x"
echo