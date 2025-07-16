# Publishing to PyPI

This guide explains how to publish the claude-code-indexer package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts at:
   - https://pypi.org/account/register/ (production)
   - https://test.pypi.org/account/register/ (testing)

2. **Install build tools**:
   ```bash
   pip install --upgrade build twine
   ```

3. **API Token**: Generate API tokens from PyPI account settings

## Publishing Steps

### 1. Update Version

Update version in these files:
- `pyproject.toml`
- `setup.py`
- `claude_code_indexer/__init__.py`
- Update `CHANGELOG.md`

### 2. Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info
```

### 3. Build the Package

```bash
python -m build
```

This creates:
- `dist/claude-code-indexer-X.X.X.tar.gz` (source distribution)
- `dist/claude_code_indexer-X.X.X-py3-none-any.whl` (wheel)

### 4. Test with TestPyPI (Optional)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ --no-deps claude-code-indexer
```

### 5. Upload to PyPI

```bash
python -m twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token

### 6. Verify Installation

```bash
# Install from PyPI
pip install claude-code-indexer

# Test the installation
claude-code-indexer --version
claude-code-indexer --help
```

## Automated Publishing (GitHub Actions)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Post-Publishing

1. **Create GitHub Release**:
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

2. **Update Documentation**:
   - Update README with new features
   - Update installation instructions

3. **Announce**:
   - GitHub release notes
   - Social media if applicable

## Troubleshooting

### Common Issues

1. **Version already exists**: Increment version number
2. **Invalid metadata**: Check setup.py and pyproject.toml
3. **Missing files**: Ensure MANIFEST.in includes all necessary files
4. **Authentication failed**: Check API token and username

### Testing Locally

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from local wheel
pip install dist/claude_code_indexer-*.whl

# Test
claude-code-indexer --help
```

## Best Practices

1. **Semantic Versioning**: Follow MAJOR.MINOR.PATCH
2. **Test Thoroughly**: Test on multiple Python versions
3. **Documentation**: Keep README and CHANGELOG updated
4. **Dependencies**: Pin minimum versions, not exact versions
5. **Security**: Never commit API tokens to repository