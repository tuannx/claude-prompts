#!/usr/bin/env python3
"""
Simple AutoIt Support Installer (Windows-compatible)
No Unicode emojis, focused on functionality
"""
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path


def print_step(step, message):
    """Print step without Unicode"""
    print(f"[{step}] {message}")


def run_command(command, description, cwd=None):
    """Run command and return success"""
    print_step("CMD", f"{description}: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"ERROR: {description} failed")
            print(f"STDERR: {result.stderr}")
            return False
        
        print(f"SUCCESS: {description}")
        return True
        
    except Exception as e:
        print(f"ERROR: {description} failed: {e}")
        return False


def test_autoit_support():
    """Test AutoIt support is working"""
    print_step("TEST", "Testing AutoIt support...")
    
    test_script = '''
import sys
try:
    from claude_code_indexer.parsers import create_default_parser
    parser = create_default_parser()
    extensions = parser.get_supported_extensions()
    autoit_exts = [ext for ext in extensions if ext in [".au3", ".aut", ".a3x"]]
    
    if len(autoit_exts) >= 3 and parser.can_parse("test.au3"):
        print("SUCCESS: AutoIt support working")
        sys.exit(0)
    else:
        print("ERROR: AutoIt support not working")
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        test_file = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        success = result.returncode == 0
        print(f"Test result: {result.stdout.strip()}")
        return success
        
    finally:
        os.unlink(test_file)


def quick_install():
    """Quick installation process"""
    print("=" * 50)
    print("AutoIt Support Quick Installer")
    print("=" * 50)
    
    current_dir = Path(__file__).parent
    package_dir = current_dir / "claude_code_indexer"
    
    # Check if source exists
    if not package_dir.exists():
        print("ERROR: Package directory not found")
        return False
    
    # Check if already installed and working
    try:
        result = subprocess.run(
            ["claude-code-indexer", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print_step("INFO", f"Found: {result.stdout.strip()}")
            if test_autoit_support():
                print("\nSUCCESS: AutoIt support already installed and working!")
                return True
            else:
                print("WARNING: Installation found but AutoIt support not working")
        else:
            print_step("INFO", "No existing installation found")
    except Exception:
        print_step("INFO", "No existing installation found")
    
    # Install build tools
    print_step("INSTALL", "Installing build tools...")
    if not run_command("pip install build wheel", "Installing build"):
        return False
    
    # Build package
    print_step("BUILD", "Building package...")
    dist_dir = package_dir / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir, ignore_errors=True)
    
    if not run_command("python -m build", "Building package", cwd=package_dir):
        return False
    
    # Find wheel file
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        print("ERROR: No wheel file found")
        return False
    
    wheel_file = wheel_files[0]
    print_step("FOUND", f"Built: {wheel_file.name}")
    
    # Install package
    print_step("INSTALL", "Installing package...")
    if not run_command(f"pip install {wheel_file} --force-reinstall", "Installing package"):
        return False
    
    # Test installation
    print_step("TEST", "Testing installation...")
    if not test_autoit_support():
        print("ERROR: Installation failed verification")
        return False
    
    print("\n" + "=" * 50)
    print("SUCCESS: AutoIt support installed and verified!")
    print("=" * 50)
    print("\nUsage:")
    print("  claude-code-indexer index /path/to/autoit/project")
    print("  claude-code-indexer query --important")
    print("\nSupported: .au3, .aut, .a3x files")
    
    return True


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("""
Simple AutoIt Support Installer

Usage:
  python simple-autoit-installer.py

This installer will:
1. Check for existing installation
2. Build the claude-code-indexer package with AutoIt support
3. Install or update the package
4. Verify AutoIt support is working

No options needed - just run it!
""")
        return
    
    try:
        success = quick_install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInstallation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\nInstallation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()