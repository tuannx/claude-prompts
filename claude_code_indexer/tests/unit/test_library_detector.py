'''
Unit tests for the LibraryDetector.
'''

import pytest
import ast
from claude_code_indexer.library_detector import LibraryDetector

@pytest.fixture
def detector():
    return LibraryDetector()

def test_detect_no_libraries(detector):
    code = "print('Hello, world!')"
    tree = ast.parse(code)
    libraries = detector.detect_libraries(tree, "test.py", code)
    assert len(libraries) == 0

def test_detect_single_python_library(detector):
    code = "import requests\nresponse = requests.get('https://example.com')"
    tree = ast.parse(code)
    libraries = detector.detect_libraries(tree, "test.py", code)
    assert "requests" in libraries
    assert libraries["requests"].category == "web"
    assert libraries["requests"].usage_count > 0

def test_detect_multiple_python_libraries(detector):
    code = '''
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.rand(10, 5))
'''
    tree = ast.parse(code)
    libraries = detector.detect_libraries(tree, "test.py", code)
    assert "pandas" in libraries
    assert "numpy" in libraries
    assert libraries["pandas"].category == "ml"
    assert libraries["numpy"].category == "ml"

def test_categorize_library(detector):
    assert detector._categorize_library("flask") == "web"
    assert detector._categorize_library("tensorflow") == "ml"
    assert detector._categorize_library("boto3") == "cloud"
    assert detector._categorize_library("some_unknown_lib") == "other"

def test_handle_malformed_ast(detector):
    # This test checks if the detector handles a malformed AST gracefully.
    # A malformed AST is simulated by passing None.
    libraries = detector.detect_libraries(None, "test.py", "")
    assert len(libraries) == 0
