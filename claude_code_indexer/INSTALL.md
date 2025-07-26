# Installation Guide for Claude Code Indexer

## 🚀 Quick Install (Recommended)

### Option 1: Install from PyPI (When Published)
```bash
pip install claude-code-indexer
```

### Option 2: Install from GitHub
```bash
pip install git+https://github.com/tuannx/claude-prompts.git#subdirectory=claude_code_indexer
```

### Option 3: Install from Source
```bash
# Clone the repository
git clone https://github.com/tuannx/claude-prompts.git
cd claude-prompts/claude_code_indexer

# Install
pip install .
```

## 🛡️ Safe Installation Script

Save this as `install_cci.py` and run it:

```python
#!/usr/bin/env python3
"""
Safe installer for Claude Code Indexer
Works on Windows, Mac, and Linux
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. You have {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_pip():
    """Ensure pip is installed"""
    try:
        import pip
        print("✅ pip is installed")
        return True
    except ImportError:
        print("❌ pip not found")
        print("Installing pip...")
        try:
            import ensurepip
            ensurepip.bootstrap()
            return True
        except:
            print("Failed to install pip. Please install manually.")
            return False


def install_package():
    """Install Claude Code Indexer"""
    print("\n📦 Installing Claude Code Indexer...")
    
    # Try different installation methods
    methods = [
        # Method 1: From PyPI (when published)
        ([sys.executable, "-m", "pip", "install", "claude-code-indexer"], "PyPI"),
        
        # Method 2: From GitHub
        ([sys.executable, "-m", "pip", "install", 
          "git+https://github.com/tuannx/claude-prompts.git#subdirectory=claude_code_indexer"], 
         "GitHub"),
    ]
    
    for cmd, source in methods:
        print(f"\nTrying to install from {source}...")
        try:
            subprocess.check_call(cmd)
            print(f"✅ Successfully installed from {source}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install from {source}")
            continue
    
    return False


def verify_installation():
    """Verify the installation works"""
    print("\n🔍 Verifying installation...")
    
    try:
        # Try importing
        import claude_code_indexer
        print("✅ Package imported successfully")
        
        # Try running CLI
        result = subprocess.run(
            [sys.executable, "-m", "claude_code_indexer.cli", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ CLI working: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  CLI not responding properly")
            return False
            
    except ImportError:
        print("❌ Package import failed")
        return False


def create_shortcuts():
    """Create convenient shortcuts"""
    print("\n🔗 Creating shortcuts...")
    
    # For Unix-like systems
    if os.name != 'nt':
        shell_rc = Path.home() / '.bashrc'
        if Path.home() / '.zshrc' in Path.home().iterdir():
            shell_rc = Path.home() / '.zshrc'
        
        alias_line = "alias cci='python -m claude_code_indexer.cli'"
        
        try:
            with open(shell_rc, 'a') as f:
                f.write(f"\n# Claude Code Indexer\n{alias_line}\n")
            print(f"✅ Added alias to {shell_rc}")
            print("   Run 'source ~/.bashrc' or restart terminal")
        except:
            print(f"ℹ️  Add this to your shell config: {alias_line}")
    
    # For Windows
    else:
        print("ℹ️  On Windows, 'cci' command should work automatically")
        print("   If not, use: python -m claude_code_indexer.cli")


def main():
    """Main installation process"""
    print("🚀 Claude Code Indexer Installer")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_pip():
        return
    
    # Install
    if not install_package():
        print("\n❌ Installation failed")
        print("\nManual installation:")
        print("1. Download from: https://github.com/tuannx/claude-prompts")
        print("2. cd claude-prompts/claude_code_indexer")
        print("3. pip install .")
        return
    
    # Verify
    if verify_installation():
        create_shortcuts()
        print("\n✅ Installation complete!")
        print("\nUsage:")
        print("  cci --help")
        print("  cci index .")
        print("  cci doctor")
    else:
        print("\n⚠️  Installation completed but verification failed")
        print("Try running: python -m claude_code_indexer.cli --help")


if __name__ == "__main__":
    main()
```

## 🖥️ Platform-Specific Instructions

### Windows
```powershell
# Run PowerShell as Administrator
python -m pip install claude-code-indexer

# Or use the installer
python install_cci.py
```

### macOS
```bash
# Using Homebrew Python
brew install python@3.11
python3 -m pip install claude-code-indexer

# Or use the installer
python3 install_cci.py
```

### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip
pip3 install claude-code-indexer

# Or use the installer
python3 install_cci.py
```

## 🐳 Docker Installation (Zero Dependencies)

```dockerfile
FROM python:3.11-slim

RUN pip install claude-code-indexer

WORKDIR /code

ENTRYPOINT ["cci"]
```

Usage:
```bash
# Build
docker build -t cci .

# Run
docker run -v $(pwd):/code cci index .
```

## 🔧 Troubleshooting

### Command not found
```bash
# Use full module path
python -m claude_code_indexer.cli --help

# Or add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Import errors
```bash
# Reinstall with dependencies
pip install --upgrade --force-reinstall claude-code-indexer

# Or use virtual environment
python -m venv cci_env
source cci_env/bin/activate  # Linux/Mac
cci_env\Scripts\activate     # Windows
pip install claude-code-indexer
```

### Permission errors
```bash
# Install for user only
pip install --user claude-code-indexer

# Or use pipx (recommended)
pipx install claude-code-indexer
```

## ✅ Verify Installation

```bash
# Check version
cci --version

# Run diagnostics
cci doctor

# Test indexing
cci index --help
```

## 🆘 Support

- Issues: https://github.com/tuannx/claude-prompts/issues
- Documentation: https://github.com/tuannx/claude-prompts/tree/main/claude_code_indexer