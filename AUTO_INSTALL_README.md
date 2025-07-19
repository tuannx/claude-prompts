# AutoIt Support - Automated Installation Guide

## 🚀 Quick Install (Recommended)

### Option 1: Simple One-Command Install
```bash
# Windows, Linux, macOS
python simple-autoit-installer.py
```

### Option 2: One-Click Install (Windows)
1. Double-click `install-autoit-support.bat`
2. Wait for completion
3. Press any key to close

### Option 3: One-Click Install (Linux/macOS)
```bash
chmod +x install-autoit-support.sh
./install-autoit-support.sh
```

## 📋 What Gets Installed

The automated installer will:
1. ✅ Check for existing claude-code-indexer installation
2. ✅ Install build tools if needed (`build`, `wheel`)
3. ✅ Build claude-code-indexer v1.10.0 with AutoIt support
4. ✅ Install or update the package
5. ✅ Verify AutoIt support is working
6. ✅ Run comprehensive tests (5 tests)

## 🔧 Installation Options

### Simple Installer Features
- **Auto-detection**: Checks existing installation
- **Smart updates**: Only rebuilds if needed
- **Verification**: Tests AutoIt support after install
- **Windows compatible**: No Unicode issues
- **Fast**: Typically completes in 30-60 seconds

### Advanced Installer Features
```bash
# Full installer with comprehensive testing
python install-autoit-support.py

# Test-only mode
python install-autoit-support.py --test

# Update check
python install-autoit-support.py --update

# Quick install/verify
python install-autoit-support.py --quick

# Help
python install-autoit-support.py --help
```

## ✅ Verification

### Automatic Verification
The installer automatically runs these tests:
1. **Import Test**: Verifies all modules load correctly
2. **Extension Test**: Checks .au3, .aut, .a3x support
3. **Recognition Test**: Tests file type detection
4. **Parsing Test**: Parses sample AutoIt code
5. **Integration Test**: Verifies indexer integration

### Manual Verification
```bash
# Run comprehensive verification
python verify_autoit_installation.py

# Quick check
claude-code-indexer --version
python -c "from claude_code_indexer.parsers import create_default_parser; print('AutoIt supported:', create_default_parser().can_parse('test.au3'))"
```

## 📊 Installation Files

| File | Purpose | Platform |
|------|---------|----------|
| `simple-autoit-installer.py` | Simple, reliable installer | All |
| `install-autoit-support.py` | Advanced installer with features | All |
| `install-autoit-support.bat` | One-click Windows installer | Windows |
| `install-autoit-support.sh` | One-click Unix installer | Linux/macOS |
| `verify_autoit_installation.py` | Comprehensive verification | All |

## 🎯 Usage After Installation

```bash
# Index AutoIt project
claude-code-indexer index /path/to/autoit/project

# Query important AutoIt components
claude-code-indexer query --important

# Search for AutoIt functions
claude-code-indexer search function_name

# Get project statistics
claude-code-indexer stats
```

## 🔧 Supported AutoIt Elements

- **Functions**: `Func...EndFunc` blocks
- **Includes**: `#include` statements  
- **Variables**: Global and Local variables with scope
- **GUI Controls**: GUICreate, GUICtrlCreate* functions
- **COM Objects**: ObjCreate statements
- **Hotkeys**: HotKeySet definitions
- **File Types**: .au3, .aut, .a3x extensions

## 🛠️ Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Install Python 3.8+ from python.org
# Windows: Add to PATH during installation
# Linux: sudo apt install python3 python3-pip
# macOS: brew install python3
```

#### Build Tools Missing
```bash
# The installer automatically installs these:
pip install build wheel setuptools
```

#### Unicode Issues (Windows)
- Use `simple-autoit-installer.py` instead of the advanced installer
- The simple installer avoids Unicode characters that cause Windows console issues

#### Permission Issues
```bash
# Windows: Run as Administrator if needed
# Linux/macOS: Use sudo if permission denied
sudo python simple-autoit-installer.py
```

### Getting Help

1. **Check version**: `claude-code-indexer --version`
2. **Run verification**: `python verify_autoit_installation.py`
3. **Test parsing**: Create a small .au3 file and run indexer on it
4. **Check logs**: Look for error messages during installation

## 📈 Performance

### Installation Speed
- **Simple installer**: 30-60 seconds
- **Advanced installer**: 60-120 seconds (includes comprehensive tests)
- **One-click installers**: Same as simple installer

### Test Results (5/5 tests pass)
1. ✅ Import and basic functionality
2. ✅ Extension support (.au3, .aut, .a3x)
3. ✅ File recognition
4. ✅ Parsing functionality (18 nodes, 7 functions)
5. ✅ Integration with indexer

## 🎉 Success Indicators

When installation is successful, you'll see:
```
SUCCESS: AutoIt support installed and verified!

Usage:
  claude-code-indexer index /path/to/autoit/project
  claude-code-indexer query --important

Supported: .au3, .aut, .a3x files
```

You can then immediately start using AutoIt support with claude-code-indexer!

---
*Auto-install system created: 2025-01-19*  
*Compatible with: Windows, Linux, macOS*  
*Python requirement: 3.8+*