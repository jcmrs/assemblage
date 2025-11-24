"""
tests.test_code_chunking

Tests for the AST-based code chunking logic.
"""

from pathlib import Path

from assemblage.code_search import _split_code_into_chunks

# --- Test Data ---

CODE_SIMPLE_FUNCTION = """
def hello():
    print("Hello, World!")
"""

CODE_FUNCTION_WITH_DECORATOR = """
@my_decorator
def hello():
    print("Hello, World!")
"""

CODE_CLASS_WITH_METHOD = """
class MyClass:
    def method(self):
        return 1
"""

CODE_MULTIPLE_NODES = """
import os

def func_one():
    pass

class MyClass:
    pass

def func_two():
    pass
"""

CODE_SYNTAX_ERROR = """
def hello()
    print("Hello!")
"""


def test_simple_function():
    """Tests a single, simple function."""
    chunks = _split_code_into_chunks(Path("test.py"), CODE_SIMPLE_FUNCTION)
    assert len(chunks) == 1
    assert chunks[0]["content"].strip() == CODE_SIMPLE_FUNCTION.strip()
    assert chunks[0]["line"] == 2


def test_function_with_decorator():
    """Tests that decorators are handled gracefully."""
    chunks = _split_code_into_chunks(Path("test.py"), CODE_FUNCTION_WITH_DECORATOR)
    assert len(chunks) == 1
    # ast.get_source_segment does NOT include the decorator,
    # which is a known limitation. We are testing that it correctly
    # extracts the function definition itself.
    assert "@my_decorator" not in chunks[0]["content"]
    assert chunks[0]["content"].strip().startswith("def hello():")
    assert chunks[0]["line"] == 3


def test_class_with_method():
    """Tests that a class is captured as a single chunk."""
    chunks = _split_code_into_chunks(Path("test.py"), CODE_CLASS_WITH_METHOD)
    assert len(chunks) == 1
    assert "class MyClass:" in chunks[0]["content"]
    assert "def method(self):" in chunks[0]["content"]
    assert chunks[0]["line"] == 2


def test_multiple_top_level_nodes():
    """Tests a file with multiple functions and classes."""
    chunks = _split_code_into_chunks(Path("test.py"), CODE_MULTIPLE_NODES)
    assert len(chunks) == 3
    contents = [c["content"] for c in chunks]
    assert "def func_one():" in contents[0]
    assert "class MyClass:" in contents[1]
    assert "def func_two():" in contents[2]


def test_syntax_error_file(capsys):
    """Tests that a file with a syntax error is skipped gracefully."""
    chunks = _split_code_into_chunks(Path("test.py"), CODE_SYNTAX_ERROR)
    assert len(chunks) == 0
    captured = capsys.readouterr()
    assert "WARNING: Skipping test.py due to syntax error" in captured.out
