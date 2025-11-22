"""
test_code_search.py

Tests for the incremental code search indexing logic.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from assemblage import code_search as cs

# --- Test Data ---
MOCK_FILE_1_CONTENT_V1 = "def function_one():\n    return 1"
MOCK_FILE_1_CONTENT_V2 = "def function_one_modified():\n    return 1.1"
MOCK_FILE_2_CONTENT = "class MyClass:\n    pass"


@pytest.fixture
def mock_env(tmp_path):
    """Sets up a temporary environment with mock files and patches."""
    # Create directories
    index_dir = tmp_path / ".assemblage_cache"
    index_dir.mkdir()

    # Patch constants to use the temp directory
    with patch.object(cs, "INDEX_DIR", index_dir), patch.object(
        cs, "INDEX_PATH", index_dir / "code_index.faiss"
    ), patch.object(
        cs, "METADATA_PATH", index_dir / "code_index_meta.json"
    ), patch.object(cs, "MANIFEST_PATH", index_dir / "index_manifest.json"):
        # Create mock files
        (tmp_path / "file1.py").write_text(MOCK_FILE_1_CONTENT_V1)
        (tmp_path / "file2.py").write_text(MOCK_FILE_2_CONTENT)

        yield tmp_path


@patch("assemblage.code_search.SentenceTransformer")
def test_initial_build(mock_st, mock_env, monkeypatch):
    """Tests that a full build from scratch works correctly."""
    # --- Setup ---
    monkeypatch.chdir(mock_env)
    mock_model_instance = MagicMock()
    mock_model_instance.get_sentence_embedding_dimension.return_value = 4
    # Each call to encode (for each file) returns one embedding
    mock_model_instance.encode.side_effect = [
        [[0.1, 0.2, 0.3, 0.4]],  # For file1
        [[0.5, 0.6, 0.7, 0.8]],  # For file2
    ]
    mock_st.return_value = mock_model_instance

    # Mock git ls-files to return our mock files
    with patch.object(
        cs, "_get_all_code_files", return_value={Path("file1.py"), Path("file2.py")}
    ):
        # --- Execution ---
        cs.build_index()

    # --- Assertions ---
    manifest = json.loads(
        (mock_env / ".assemblage_cache" / "index_manifest.json").read_text()
    )
    assert len(manifest["files"]) == 2
    assert manifest["next_faiss_id"] == 2

    metadata = json.loads(
        (mock_env / ".assemblage_cache" / "code_index_meta.json").read_text()
    )
    assert len(metadata) == 2
    assert "0" in metadata
    assert "1" in metadata


@patch("assemblage.code_search.SentenceTransformer")
def test_file_modification(mock_st, mock_env, monkeypatch):
    """Tests that modifying a file triggers a correct incremental update."""
    # --- Setup: Initial Build ---
    monkeypatch.chdir(mock_env)
    mock_model_instance = MagicMock()
    mock_model_instance.get_sentence_embedding_dimension.return_value = 4
    mock_model_instance.encode.side_effect = [
        [[0.1, 0.2, 0.3, 0.4]],  # Initial build file1
        [[0.5, 0.6, 0.7, 0.8]],  # Initial build file2
        [[0.9, 0.9, 0.9, 0.9]],  # Second build (only the modified file1)
    ]
    mock_st.return_value = mock_model_instance

    with patch.object(
        cs, "_get_all_code_files", return_value={Path("file1.py"), Path("file2.py")}
    ):
        cs.build_index()

    # --- Modification ---
    (mock_env / "file1.py").write_text(MOCK_FILE_1_CONTENT_V2)

    # --- Execution: Second Build ---
    with patch.object(
        cs, "_get_all_code_files", return_value={Path("file1.py"), Path("file2.py")}
    ):
        cs.build_index()

    # --- Assertions ---
    manifest = json.loads(
        (mock_env / ".assemblage_cache" / "index_manifest.json").read_text()
    )
    metadata = json.loads(
        (mock_env / ".assemblage_cache" / "code_index_meta.json").read_text()
    )

    assert manifest["files"]["file1.py"]["hash"] == cs._get_content_hash(
        MOCK_FILE_1_CONTENT_V2
    )
    assert manifest["next_faiss_id"] == 3

    metadata_content = {v["content"] for v in metadata.values()}
    assert MOCK_FILE_1_CONTENT_V1 not in metadata_content
    assert MOCK_FILE_2_CONTENT in metadata_content
    assert MOCK_FILE_1_CONTENT_V2 in metadata_content


@patch("assemblage.code_search.SentenceTransformer")
def test_file_deletion(mock_st, mock_env, monkeypatch):
    """Tests that deleting a file triggers a correct incremental update."""
    # --- Setup: Initial Build ---
    monkeypatch.chdir(mock_env)
    mock_model_instance = MagicMock()
    mock_model_instance.get_sentence_embedding_dimension.return_value = 4
    mock_model_instance.encode.side_effect = [
        [[0.1, 0.2, 0.3, 0.4]],  # file1
        [[0.5, 0.6, 0.7, 0.8]],  # file2
    ]
    mock_st.return_value = mock_model_instance

    with patch.object(
        cs, "_get_all_code_files", return_value={Path("file1.py"), Path("file2.py")}
    ):
        cs.build_index()

    # --- Deletion ---
    (mock_env / "file2.py").unlink()
    # Reset the mock's side_effect for the second run, where it won't be called
    mock_model_instance.encode.side_effect = []

    # --- Execution: Second Build ---
    with patch.object(cs, "_get_all_code_files", return_value={Path("file1.py")}):
        cs.build_index()

    # --- Assertions ---
    manifest = json.loads(
        (mock_env / ".assemblage_cache" / "index_manifest.json").read_text()
    )
    metadata = json.loads(
        (mock_env / ".assemblage_cache" / "code_index_meta.json").read_text()
    )

    assert "file2.py" not in manifest["files"]
    assert "file1.py" in manifest["files"]

    metadata_content = {v["content"] for v in metadata.values()}
    assert MOCK_FILE_2_CONTENT not in metadata_content
    assert MOCK_FILE_1_CONTENT_V1 in metadata_content
