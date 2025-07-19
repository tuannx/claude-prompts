#!/usr/bin/env python3
"""
Automated installer for claude-code-indexer with AutoIt support
Automatically builds, installs, and updates the latest version with AutoIt parser
Features: auto-install, auto-update, comprehensive testing
"""
import os
import sys
import subprocess
import tempfile
import shutil
import json
import time
from pathlib import Path
from datetime import datetime


class AutoItSupportInstaller:
    """Automated installer for claude-code-indexer with AutoIt support"""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.package_dir = self.current_dir / "claude_code_indexer"
        self.config_file = self.current_dir / ".autoit_installer_config.json"
        self.test_results = []
        
    def print_step(self, step, message):
        """Print installation step with formatting"""
        print(f"[{step}] {message}")
    
    def run_command(self, command, description, cwd=None):
        """Run a command and handle errors"""
        self.print_step("CMD", f"{description}: {command}")
        
        try:
            # Set encoding to handle Unicode issues on Windows
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                env=env,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                print(f"ERROR: {description} failed")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
            
            print(f"SUCCESS: {description} completed")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"ERROR: {description} timed out")
            return False
        except Exception as e:
            print(f"ERROR: {description} failed with exception: {e}")
            return False
    
    def check_prerequisites(self):
        """Check if required tools are available"""
        self.print_step("CHECK", "Checking prerequisites...")
        
        # Check Python
        if sys.version_info < (3, 8):
            print("ERROR: Python 3.8+ required")
            return False
        
        # Check pip
        if not self.run_command("pip --version", "Checking pip"):
            return False
        
        # Check if source directory exists
        if not self.package_dir.exists():
            print(f"ERROR: Package directory not found: {self.package_dir}")
            return False
        
        self.print_step("OK", "Prerequisites check passed")
        return True
    
    def install_build_tools(self):
        """Install required build tools"""
        self.print_step("INSTALL", "Installing build tools...")
        
        build_tools = ["build", "wheel", "setuptools>=61.0"]
        
        for tool in build_tools:
            if not self.run_command(f"pip install {tool}", f"Installing {tool}"):
                return False
        
        return True
    
    def build_package(self):
        """Build the claude-code-indexer package with AutoIt support"""
        self.print_step("BUILD", "Building claude-code-indexer with AutoIt support...")
        
        # Clean previous builds
        dist_dir = self.package_dir / "dist"
        build_dir = self.package_dir / "build"
        
        if dist_dir.exists():
            shutil.rmtree(dist_dir, ignore_errors=True)
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        
        # Build package
        if not self.run_command(
            "python -m build",
            "Building package",
            cwd=self.package_dir
        ):
            return False
        
        # Verify build artifacts
        wheel_files = list(dist_dir.glob("*.whl"))
        if not wheel_files:
            print("ERROR: No wheel file generated")
            return False
        
        self.wheel_file = wheel_files[0]
        self.print_step("OK", f"Package built: {self.wheel_file.name}")
        return True
    
    def install_package(self):
        """Install the built package"""
        self.print_step("INSTALL", "Installing claude-code-indexer with AutoIt support...")
        
        # Install with force-reinstall to ensure we get the latest version
        if not self.run_command(
            f"pip install {self.wheel_file} --force-reinstall",
            "Installing package"
        ):
            return False
        
        return True
    
    def verify_installation(self):
        """Verify that AutoIt support is working"""
        self.print_step("VERIFY", "Verifying AutoIt support...")
        
        # Test 1: Check version
        if not self.run_command(
            "claude-code-indexer --version",
            "Checking version"
        ):
            return False
        
        # Test 2: Check AutoIt parser support using Python
        test_script = '''
import sys
try:
    from claude_code_indexer.parsers import create_default_parser
    parser = create_default_parser()
    
    # Check AutoIt extensions
    extensions = parser.get_supported_extensions()
    autoit_exts = [ext for ext in extensions if ext in [".au3", ".aut", ".a3x"]]
    
    print(f"AutoIt extensions supported: {autoit_exts}")
    print(f"Can parse .au3: {parser.can_parse('test.au3')}")
    
    if len(autoit_exts) >= 3 and parser.can_parse('test.au3'):
        print("SUCCESS: AutoIt support verified!")
        sys.exit(0)
    else:
        print("ERROR: AutoIt support not working")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
'''
        
        # Write test script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_script)
            test_file = f.name
        
        try:
            success = self.run_command(
                f"python {test_file}",
                "Testing AutoIt parser support"
            )
            return success
        finally:
            os.unlink(test_file)
    
    def create_sample_test(self):
        """Create a sample AutoIt file and test parsing"""
        self.print_step("TEST", "Creating sample AutoIt test...")
        
        sample_autoit = '''
#include <GUIConstantsEx.au3>

Global $g_hMainGUI
Global $g_sTitle = "AutoIt Test Application"

Func Main()
    Local $hGUI = CreateMainWindow()
    ShowMainWindow()
EndFunc

Func CreateMainWindow()
    $g_hMainGUI = GUICreate($g_sTitle, 400, 300)
    Local $idButton = GUICtrlCreateButton("Test", 10, 10, 100, 30)
    Return $g_hMainGUI
EndFunc

Func ShowMainWindow()
    GUISetState(@SW_SHOW, $g_hMainGUI)
EndFunc

HotKeySet("{ESC}", "ExitApp")

Func ExitApp()
    Exit
EndFunc

Main()
'''
        
        # Create temporary AutoIt file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.au3', delete=False) as f:
            f.write(sample_autoit)
            autoit_file = f.name
        
        try:
            # Test parsing with Python API (to avoid Unicode issues)
            test_script = f'''
import sys
try:
    from claude_code_indexer.parsers import create_default_parser
    
    parser = create_default_parser()
    result = parser.parse_file("{autoit_file}")
    
    print(f"Parse result: {{result.success}}")
    print(f"Language: {{result.language}}")
    print(f"Nodes: {{len(result.nodes)}}")
    print(f"Relationships: {{len(result.relationships)}}")
    
    if result.success and result.language == "autoit" and len(result.nodes) > 0:
        print("SUCCESS: Sample AutoIt file parsed successfully!")
        sys.exit(0)
    else:
        print("ERROR: Sample parsing failed")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR: {{e}}")
    sys.exit(1)
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_script)
                test_file = f.name
            
            try:
                success = self.run_command(
                    f"python {test_file}",
                    "Testing sample AutoIt file parsing"
                )
                return success
            finally:
                os.unlink(test_file)
                
        finally:
            os.unlink(autoit_file)
    
    def load_config(self):
        """Load installer configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "last_install": None,
            "last_version": None,
            "auto_update": True,
            "install_count": 0
        }
    
    def save_config(self, config):
        """Save installer configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.print_step("WARN", f"Could not save config: {e}")
    
    def get_current_version(self):
        """Get currently installed version"""
        try:
            result = subprocess.run(
                ["claude-code-indexer", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Extract version from output like "claude-code-indexer, version 1.10.0"
                output = result.stdout.strip()
                if "version" in output:
                    return output.split("version")[-1].strip()
            return None
        except Exception:
            return None
    
    def get_package_version(self):
        """Get version from package source"""
        try:
            pyproject_file = self.package_dir / "pyproject.toml"
            if pyproject_file.exists():
                with open(pyproject_file, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.strip().startswith('version ='):
                            # Extract version from line like 'version = "1.10.0"'
                            return line.split('=')[1].strip().strip('"\'')
            return None
        except Exception:
            return None
    
    def check_for_updates(self):
        """Check if an update is available"""
        self.print_step("UPDATE", "Checking for updates...")
        
        current_version = self.get_current_version()
        package_version = self.get_package_version()
        
        self.print_step("INFO", f"Current version: {current_version}")
        self.print_step("INFO", f"Package version: {package_version}")
        
        if current_version is None:
            self.print_step("INFO", "No current installation found - will install")
            return True
        
        if package_version is None:
            self.print_step("WARN", "Could not determine package version")
            return False
        
        # Simple version comparison (works for semantic versioning)
        if current_version != package_version:
            self.print_step("UPDATE", f"Update available: {current_version} -> {package_version}")
            return True
        
        self.print_step("OK", "Already up to date")
        return False
    
    def add_test_result(self, test_name, success, details=""):
        """Add a test result to the results list"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite"""
        self.print_step("TEST", "Running comprehensive test suite...")
        
        all_passed = True
        
        # Test 1: Version check
        try:
            result = subprocess.run(
                ["claude-code-indexer", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            success = result.returncode == 0 and "claude-code-indexer" in result.stdout
            self.add_test_result("version_check", success, result.stdout.strip())
            if not success:
                all_passed = False
        except Exception as e:
            self.add_test_result("version_check", False, str(e))
            all_passed = False
        
        # Test 2: Parser import test
        try:
            test_script = '''
import sys
try:
    from claude_code_indexer.parsers import create_default_parser
    from claude_code_indexer.parsers.autoit_parser import AutoItParser
    print("SUCCESS: Parser imports working")
    sys.exit(0)
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
                self.add_test_result("parser_import", success, result.stdout.strip())
                if not success:
                    all_passed = False
            finally:
                os.unlink(test_file)
                
        except Exception as e:
            self.add_test_result("parser_import", False, str(e))
            all_passed = False
        
        # Test 3: AutoIt extension support
        try:
            test_script = '''
import sys
try:
    from claude_code_indexer.parsers import create_default_parser
    parser = create_default_parser()
    extensions = parser.get_supported_extensions()
    autoit_exts = [ext for ext in extensions if ext in [".au3", ".aut", ".a3x"]]
    can_parse = parser.can_parse("test.au3")
    
    if len(autoit_exts) >= 3 and can_parse:
        print(f"SUCCESS: AutoIt support working - {autoit_exts}")
        sys.exit(0)
    else:
        print(f"ERROR: AutoIt support incomplete - {autoit_exts}, can_parse={can_parse}")
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
                self.add_test_result("autoit_extensions", success, result.stdout.strip())
                if not success:
                    all_passed = False
            finally:
                os.unlink(test_file)
                
        except Exception as e:
            self.add_test_result("autoit_extensions", False, str(e))
            all_passed = False
        
        # Test 4: AutoIt file parsing
        autoit_code = '''
#include <GUIConstantsEx.au3>

Global $g_hGUI
Global $g_sTitle = "Test App"

Func Main()
    Local $hGUI = CreateGUI()
    ShowGUI()
EndFunc

Func CreateGUI()
    $g_hGUI = GUICreate($g_sTitle, 400, 300)
    Return $g_hGUI
EndFunc

Func ShowGUI()
    GUISetState(@SW_SHOW, $g_hGUI)
EndFunc

HotKeySet("{F1}", "ShowHelp")

Func ShowHelp()
    MsgBox(0, "Help", "F1 Help")
EndFunc

Main()
'''
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.au3', delete=False) as f:
                f.write(autoit_code)
                autoit_file = f.name
            
            test_script = f'''
import sys
try:
    from claude_code_indexer.parsers import create_default_parser
    parser = create_default_parser()
    result = parser.parse_file("{autoit_file}")
    
    functions = [n for n in result.nodes.values() if n.node_type == "function"]
    imports = [n for n in result.nodes.values() if n.node_type == "import"]
    variables = [n for n in result.nodes.values() if n.node_type == "variable"]
    
    if result.success and len(functions) >= 4 and len(imports) >= 1 and len(variables) >= 2:
        print(f"SUCCESS: Parsed {{len(result.nodes)}} nodes, {{len(functions)}} functions")
        sys.exit(0)
    else:
        print(f"ERROR: Parse failed or incomplete - success={{result.success}}, functions={{len(functions)}}")
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {{e}}")
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
                self.add_test_result("autoit_parsing", success, result.stdout.strip())
                if not success:
                    all_passed = False
            finally:
                os.unlink(test_file)
                os.unlink(autoit_file)
                
        except Exception as e:
            self.add_test_result("autoit_parsing", False, str(e))
            all_passed = False
        
        # Test 5: Integration test
        try:
            test_script = '''
import sys
try:
    from claude_code_indexer.indexer import CodeGraphIndexer
    indexer = CodeGraphIndexer()
    
    # Test that indexer uses AutoIt parser
    can_parse = indexer.parser.can_parse("test.au3")
    
    if can_parse:
        print("SUCCESS: Indexer integration working")
        sys.exit(0)
    else:
        print("ERROR: Indexer integration failed")
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
                self.add_test_result("indexer_integration", success, result.stdout.strip())
                if not success:
                    all_passed = False
            finally:
                os.unlink(test_file)
                
        except Exception as e:
            self.add_test_result("indexer_integration", False, str(e))
            all_passed = False
        
        return all_passed
    
    def print_test_results(self):
        """Print comprehensive test results"""
        self.print_step("RESULTS", "Test Results Summary")
        print("-" * 50)
        
        passed = sum(1 for r in self.test_results if r["success"])
        total = len(self.test_results)
        
        for result in self.test_results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"  {status} {result['test']}")
            if result["details"]:
                print(f"      {result['details']}")
        
        print("-" * 50)
        print(f"Total: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {total - passed} test(s) failed")
        
        return passed == total
    
    def auto_update(self):
        """Perform automatic update if available"""
        config = self.load_config()
        
        # Check if auto-update is enabled
        if not config.get("auto_update", True):
            self.print_step("SKIP", "Auto-update disabled")
            return True
        
        # Check for updates
        if not self.check_for_updates():
            return True  # Already up to date
        
        self.print_step("UPDATE", "Performing automatic update...")
        return self.install_or_update()
    
    def install_or_update(self):
        """Run installation or update process"""
        config = self.load_config()
        is_update = self.get_current_version() is not None
        
        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Build Tools", self.install_build_tools),
            ("Package Build", self.build_package),
            ("Installation", self.install_package),
            ("Comprehensive Tests", self.run_comprehensive_tests),
        ]
        
        for step_name, step_func in steps:
            print(f"\n--- {step_name} ---")
            if not step_func():
                print(f"\n❌ FAILED: {step_name}")
                if step_name == "Comprehensive Tests":
                    self.print_test_results()
                print("Installation/Update aborted.")
                return False
        
        # Update configuration
        config["last_install"] = datetime.now().isoformat()
        config["last_version"] = self.get_package_version()
        config["install_count"] = config.get("install_count", 0) + 1
        self.save_config(config)
        
        return True
    
    def install(self):
        """Run the complete installation process with auto-update and testing"""
        print("=" * 60)
        print("🚀 AutoIt Support Installer for claude-code-indexer")
        print("   Features: Auto-Install, Auto-Update, Comprehensive Testing")
        print("=" * 60)
        
        start_time = time.time()
        
        # Load configuration
        config = self.load_config()
        
        # Check if this is an update or fresh install
        current_version = self.get_current_version()
        is_update = current_version is not None
        
        if is_update:
            self.print_step("INFO", f"Current installation detected: {current_version}")
            if not self.check_for_updates():
                self.print_step("INFO", "No updates needed - running verification tests...")
                if self.run_comprehensive_tests():
                    self.print_test_results()
                    print("\n✅ System verified - AutoIt support is working correctly!")
                    return True
                else:
                    self.print_test_results()
                    print("\n⚠️  Tests failed - attempting reinstall...")
        
        # Perform installation or update
        if not self.install_or_update():
            return False
        
        # Print comprehensive test results
        self.print_test_results()
        
        # Calculate installation time
        elapsed_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        action = "UPDATE" if is_update else "INSTALLATION"
        print(f"✅ {action} COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n⏱️  Installation time: {elapsed_time:.1f} seconds")
        print(f"📊 Tests: {len([r for r in self.test_results if r['success']])}/{len(self.test_results)} passed")
        print(f"🔄 Install count: {config.get('install_count', 0)}")
        print("\n📋 AutoIt support is now available in claude-code-indexer!")
        print("\n🔧 Usage examples:")
        print("   claude-code-indexer index /path/to/autoit/project")
        print("   claude-code-indexer query --important")
        print("   claude-code-indexer search function_name")
        print("\n📚 Supported AutoIt files: .au3, .aut, .a3x")
        print("\n🎉 Happy coding!")
        
        return True


def main():
    """Main entry point"""
    installer = AutoItSupportInstaller()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ["--test", "-t"]:
            # Run tests only
            print("🧪 Running AutoIt Support Tests...")
            installer.run_comprehensive_tests()
            installer.print_test_results()
            return
        elif arg in ["--update", "-u"]:
            # Check for updates and install if available
            print("🔄 Checking for AutoIt Support Updates...")
            try:
                success = installer.auto_update()
                sys.exit(0 if success else 1)
            except Exception as e:
                print(f"❌ Update failed: {e}")
                sys.exit(1)
        elif arg in ["--quick", "-q"]:
            # Quick install/verify
            print("⚡ Quick AutoIt Support Install...")
            try:
                # Just verify if already installed, otherwise install
                if installer.get_current_version():
                    print("Already installed - running quick verification...")
                    installer.run_comprehensive_tests()
                    installer.print_test_results()
                else:
                    success = installer.install()
                    sys.exit(0 if success else 1)
            except Exception as e:
                print(f"❌ Quick install failed: {e}")
                sys.exit(1)
        elif arg in ["--help", "-h"]:
            print("""
AutoIt Support Installer for claude-code-indexer

Usage:
  python install-autoit-support.py [options]

Options:
  (no args)     Full installation with auto-update and testing
  --test, -t    Run comprehensive tests only
  --update, -u  Check for updates and install if available
  --quick, -q   Quick install or verification
  --help, -h    Show this help message

Features:
  • Automatic building and installation
  • Version detection and auto-update
  • Comprehensive test suite (5 tests)
  • Configuration persistence
  • One-click setup

Examples:
  python install-autoit-support.py        # Full install
  python install-autoit-support.py -t     # Test only
  python install-autoit-support.py -u     # Update check
  python install-autoit-support.py -q     # Quick install
""")
            return
    
    # Default: full installation
    try:
        success = installer.install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()