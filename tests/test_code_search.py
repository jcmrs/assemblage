"""
test_code_search.py

Tests for the core code search and indexing logic.
"""

import json

import pytest

from assemblage import code_search


@pytest.fixture
def mock_codebase(tmp_path):
    """Creates a temporary directory with mock python files."""
    p = tmp_path / "src"
    p.mkdir()
    file1 = p / "file1.py"
    file1.write_text(
        '"""This is a docstring."""\n\n'
        "import os\n\n"
        "class MyClass:\n"
        "    pass\n\n"
        "def function_for_adding(a, b):\n"
        '    """This function adds two numbers."""\n'
        ""
        "    return a + b\n"
    )

    file2 = p / "file2.py"
    file2.write_text(
        "def function_for_subtracting(a, b):\n"
        '    """This function subtracts two numbers."""\n'
        ""
        "    return a - b\n"
    )

    # Also create a gitignore in the root
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.txt\n.venv/\n")

    return tmp_path


def test_build_index(mock_codebase, monkeypatch):
    """
    Tests that the index is built correctly.
    """

    # We need to patch _get_all_code_files to work with our temp dir
    def mock_get_files():
        return list(mock_codebase.glob("**/*.py"))

    monkeypatch.setattr(code_search, "_get_all_code_files", mock_get_files)

    # We also need to patch the location of the index
    monkeypatch.setattr(code_search, "INDEX_DIR", mock_codebase / ".assemblage_cache")
    monkeypatch.setattr(
        code_search, "INDEX_PATH", mock_codebase / ".assemblage_cache/code_index.faiss"
    )
    monkeypatch.setattr(
        code_search,
        "METADATA_PATH",
        mock_codebase / ".assemblage_cache/code_index_meta.json",
    )

    code_search.build_index()

    assert (mock_codebase / ".assemblage_cache/code_index.faiss").exists()
    meta_path = mock_codebase / ".assemblage_cache/code_index_meta.json"
    assert meta_path.exists()

    with open(meta_path, "r") as f:
        metadata = json.load(f)

    # Should find 3 chunks: MyClass, function_for_adding, function_for_subtracting
    assert len(metadata) == 3
    assert metadata[1]["path"] == str(mock_codebase / "src/file1.py")


def test_search_index(mock_codebase, monkeypatch):
    """
    Tests that the search function returns relevant results.
    """

    # Set up the mock environment and build the index first
    def mock_get_files():
        return list(mock_codebase.glob("**/*.py"))

    monkeypatch.setattr(code_search, "_get_all_code_files", mock_get_files)
    index_dir = mock_codebase / ".assemblage_cache"
    monkeypatch.setattr(code_search, "INDEX_DIR", index_dir)
    monkeypatch.setattr(code_search, "INDEX_PATH", index_dir / "code_index.faiss")
    monkeypatch.setattr(
        code_search, "METADATA_PATH", index_dir / "code_index_meta.json"
    )

    code_search.build_index()

    # Now, perform the search
    results = code_search.search_index("logic for subtraction")

    assert len(results) > 0
    top_result = results[0]

    assert top_result["path"] == str(mock_codebase / "src/file2.py")
    assert top_result["line"] > 0
    assert "return a - b" in top_result["content"]
