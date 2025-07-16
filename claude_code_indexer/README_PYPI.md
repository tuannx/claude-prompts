# Publishing Instructions for PyPI

Since this is running in a non-interactive environment, here are the steps to publish:

## Option 1: Using .pypirc file

Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TEST-API-TOKEN-HERE
```

Then run:
```bash
python -m twine upload --repository testpypi dist/*
```

## Option 2: Using environment variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-API-TOKEN-HERE
python -m twine upload --repository testpypi dist/*
```

## Option 3: Direct command with token

```bash
python -m twine upload --repository testpypi \
  --username __token__ \
  --password pypi-YOUR-API-TOKEN-HERE \
  dist/*
```

## Getting API Tokens

1. Go to https://test.pypi.org and create an account
2. Go to Account Settings → API tokens
3. Create a new API token for uploading
4. Use the token with username `__token__`

## After successful test upload

Install and test from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps claude-code-indexer
```

If everything works, upload to production PyPI:
```bash
python -m twine upload dist/*
```