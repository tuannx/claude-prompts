#!/bin/bash
# One-line installer for Claude Code Indexer
# Usage: curl -sSL https://raw.githubusercontent.com/tuannx/claude-prompts/main/claude_code_indexer/install.sh | bash

set -e

echo "🚀 Installing Claude Code Indexer..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version+ required. You have $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install
echo "📦 Installing package..."
python3 -m pip install --user git+https://github.com/tuannx/claude-prompts.git#subdirectory=claude_code_indexer

# Add to PATH if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "🔧 Adding ~/.local/bin to PATH..."
    
    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        echo "✅ Added to ~/.zshrc. Run: source ~/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        echo "✅ Added to ~/.bashrc. Run: source ~/.bashrc"
    fi
fi

# Create alias
echo "🔗 Creating 'cci' alias..."
alias_cmd="alias cci='python3 -m claude_code_indexer.cli'"

if [ -n "$ZSH_VERSION" ]; then
    echo "$alias_cmd" >> ~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
    echo "$alias_cmd" >> ~/.bashrc
fi

echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  cci --help"
echo "  cci index ."
echo "  cci doctor"
echo ""
echo "If 'cci' command not found, run:"
echo "  python3 -m claude_code_indexer.cli --help"