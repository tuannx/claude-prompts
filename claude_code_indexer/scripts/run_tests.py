#!/usr/bin/env python3
"""
Convenient script to run the working test suite
"""

import subprocess
import sys
from pathlib import Path

# Define the working test files
WORKING_TESTS = [
    "tests/test_background_service_simple.py",
    "tests/test_cli_simple.py", 
    "tests/test_mcp.py",
    "tests/test_memory_cache_unit.py",
    "tests/test_autoit_parser.py",
    "tests/unit/"
]

def run_tests(with_coverage=False):
    """Run the working test suite"""
    cmd = [sys.executable, "-m", "pytest"] + WORKING_TESTS + ["-v"]
    
    if with_coverage:
        cmd.extend([
            "--cov=claude_code_indexer",
            "--cov-report=term-missing"
        ])
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

def run_specific_test(test_name):
    """Run a specific test file or test function"""
    if not test_name.startswith("tests/"):
        # Assume it's a test function, find the file
        for test_file in WORKING_TESTS:
            if Path(test_file).is_file():
                cmd = [sys.executable, "-m", "pytest", test_file, "-k", test_name, "-v"]
                break
        else:
            print(f"Could not find test: {test_name}")
            return 1
    else:
        cmd = [sys.executable, "-m", "pytest", test_name, "-v"]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Run all working tests
        print("🧪 Running all working tests...")
        exit_code = run_tests()
    elif sys.argv[1] == "--coverage":
        # Run with coverage
        print("🧪 Running all working tests with coverage...")
        exit_code = run_tests(with_coverage=True)
    elif sys.argv[1] == "--help":
        print("Usage:")
        print("  python run_tests.py                    # Run all working tests")
        print("  python run_tests.py --coverage         # Run with coverage report")
        print("  python run_tests.py test_cli_simple.py # Run specific test file")
        print("  python run_tests.py test_version       # Run specific test function")
        exit_code = 0
    else:
        # Run specific test
        test_name = sys.argv[1]
        print(f"🧪 Running specific test: {test_name}")
        exit_code = run_specific_test(test_name)
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    sys.exit(exit_code)