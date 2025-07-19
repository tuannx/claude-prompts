'''
Unit tests for the LanguageDetector.
'''

import pytest
from claude_code_indexer.language_detector import LanguageDetector

@pytest.fixture
def detector():
    return LanguageDetector()

def test_detect_python_by_extension(detector):
    assert detector.detect_language("test.py") == "python"
    assert detector.detect_language("test.pyw") == "python"

def test_detect_javascript_by_extension(detector):
    assert detector.detect_language("test.js") == "javascript"
    assert detector.detect_language("test.mjs") == "javascript"

def test_detect_typescript_by_extension(detector):
    assert detector.detect_language("test.ts") == "typescript"
    assert detector.detect_language("test.tsx") == "typescript"

def test_detect_java_by_extension(detector):
    assert detector.detect_language("test.java") == "java"

def test_unknown_extension(detector):
    assert detector.detect_language("test.foo") is None

def test_no_extension(detector, tmp_path):
    p = tmp_path / "README"
    p.write_text("This is a test file.")
    assert detector.detect_language(str(p)) is None

def test_detect_by_python_shebang(detector, tmp_path):
    p = tmp_path / "my_script"
    p.write_text("#!/usr/bin/env python\nprint('hello')")
    assert detector.detect_language(str(p)) == "python"

def test_get_supported_languages(detector):
    langs = detector.get_supported_languages()
    assert "python" in langs
    assert "javascript" in langs
    assert "java" in langs

def test_get_supported_extensions(detector):
    exts = detector.get_supported_extensions()
    assert ".py" in exts
    assert ".js" in exts
    assert ".java" in exts

def test_is_supported_file(detector):
    assert detector.is_supported_file("test.py") is True
    assert detector.is_supported_file("test.txt") is False