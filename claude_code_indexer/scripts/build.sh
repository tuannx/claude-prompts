#!/bin/bash
# Build script for Claude Code Indexer

set -e  # Exit on error

echo "🔨 Building Claude Code Indexer..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[BUILD]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $python_version"

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/
print_success "Cleaned build directories"

# Install dependencies
print_status "Installing dependencies..."
pip install -e . > /dev/null 2>&1
pip install pytest pytest-cov > /dev/null 2>&1
print_success "Dependencies installed"

# Run tests
print_status "Running tests..."
echo ""

# Run all tests with coverage
if python -m pytest tests/ -v --cov=claude_code_indexer --cov-report=term-missing; then
    print_success "All tests passed!"
else
    print_error "Tests failed! Please fix the issues before building."
    exit 1
fi

echo ""

# Check code style (optional, uncomment if using flake8/black)
# print_status "Checking code style..."
# flake8 claude_code_indexer/
# black --check claude_code_indexer/
# print_success "Code style check passed"

# Build the package
print_status "Building package..."
python -m build > /dev/null 2>&1
print_success "Package built successfully"

# Verify the build
print_status "Verifying build..."
wheel_file=$(ls dist/*.whl | head -n 1)
if [ -f "$wheel_file" ]; then
    print_success "Wheel file created: $(basename $wheel_file)"
else
    print_error "Wheel file not found!"
    exit 1
fi

# Check package contents
print_status "Checking package contents..."
unzip -l "$wheel_file" | grep -E "(\.py|\.json|\.md)" | wc -l | xargs -I {} echo "Files in package: {}"

# Install in test environment (optional)
print_status "Testing installation..."
python -m venv test_env > /dev/null 2>&1
source test_env/bin/activate
pip install "$wheel_file" > /dev/null 2>&1

# Test the installed command
if claude-code-indexer --version > /dev/null 2>&1; then
    version=$(claude-code-indexer --version | awk '{print $3}')
    print_success "Installation test passed! Version: $version"
else
    print_error "Installation test failed!"
    deactivate
    rm -rf test_env
    exit 1
fi

deactivate
rm -rf test_env

# Summary
echo ""
echo "📦 Build Summary:"
echo "  - Package: $(basename $wheel_file)"
echo "  - Size: $(du -h $wheel_file | cut -f1)"
echo "  - Version: $version"
echo ""

print_success "Build completed successfully! 🎉"
echo ""
echo "Next steps:"
echo "  1. Test locally: pip install dist/*.whl"
echo "  2. Upload to PyPI: python -m twine upload dist/*"
echo "  3. Tag release: git tag -a v$version -m 'Release v$version'"