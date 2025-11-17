"""
test_validate_assemblage.py

Tests for the validate_assemblage utility.
"""

import os
import subprocess
from unittest.mock import patch, MagicMock

import pytest
from assemblage.tools import validate_assemblage

# --- Mocks and Fixtures ---

@pytest.fixture
def mock_subprocess_run():
    """Fixture to mock subprocess.run."""
    with patch("subprocess.run") as mock_run:
        yield mock_run

@pytest.fixture
def temp_assemblage_files(tmp_path):
    """Fixture to create a temporary file structure for testing."""
    # Create dummy files and directories
    config_dir = tmp_path / "config"
    guides_dir = tmp_path / "guides"
    config_dir.mkdir()
    guides_dir.mkdir()
    
    # Version and Changelog
    (tmp_path / "ASSEMBLAGE.version").write_text("1.0.0")
    (tmp_path / "CHANGELOG.md").write_text("## [1.0.0] - Initial Version")
    
    # Config file with a valid path
    (guides_dir / "a_guide.md").write_text("guide content")
    (config_dir / "workbenches.yml").write_text(
        "workbenches:\n  explorer:\n    context_anchors:\n      - 'guides/a_guide.md'"
    )
    (config_dir / "specialists.yml").write_text("specialists: {}")

    # Other dummy files
    (tmp_path / "FOUNDATION.md").touch()
    (tmp_path / "README.md").touch()
    (tmp_path / "GEMINI.md").touch()
    (tmp_path / "CLAUDE.md").touch()
    (tmp_path / "decisions").mkdir()
    (tmp_path / "tools").mkdir()

    # Patch the constants in the module to point to the temp directory
    with patch.object(validate_assemblage, "ASSEMBLAGE_PATHS_TO_CHECK", ["."]), \
         patch.object(validate_assemblage, "VERSION_FILE", tmp_path / "ASSEMBLAGE.version"), \
         patch.object(validate_assemblage, "CHANGELOG_FILE", tmp_path / "CHANGELOG.md"), \
         patch.object(validate_assemblage, "CONFIG_FILES_TO_CHECK", [str(config_dir / "workbenches.yml"), str(config_dir / "specialists.yml")]):
        yield tmp_path


# --- Test Cases ---

def test_check_git_integrity_success(mock_subprocess_run):
    """Test that git integrity check passes when there is no output."""
    mock_process = MagicMock()
    mock_process.stdout = ""
    mock_subprocess_run.return_value = mock_process
    
    assert validate_assemblage.check_git_integrity() is True

def test_check_git_integrity_failure(mock_subprocess_run):
    """Test that git integrity check fails when there is output."""
    mock_process = MagicMock()
    mock_process.stdout = "M README.md"
    mock_subprocess_run.return_value = mock_process
    
    assert validate_assemblage.check_git_integrity() is False

def test_check_version_alignment_success(temp_assemblage_files, monkeypatch):
    """Test that version alignment check passes with matching versions."""
    monkeypatch.chdir(temp_assemblage_files)
    assert validate_assemblage.check_version_alignment() is True

def test_check_version_alignment_failure(temp_assemblage_files, monkeypatch):
    """Test that version alignment check fails with mismatched versions."""
    monkeypatch.chdir(temp_assemblage_files)
    (temp_assemblage_files / "ASSEMBLAGE.version").write_text("2.0.0")
    assert validate_assemblage.check_version_alignment() is False

def test_check_wiring_integrity_success(temp_assemblage_files, monkeypatch):
    """Test that wiring check passes when all paths exist."""
    monkeypatch.chdir(temp_assemblage_files)
    assert validate_assemblage.check_wiring_integrity() is True

def test_check_wiring_integrity_failure(temp_assemblage_files, monkeypatch):
    """Test that wiring check fails when a path is broken."""
    monkeypatch.chdir(temp_assemblage_files)
    (temp_assemblage_files / "config" / "workbenches.yml").write_text(
        "workbenches:\n  explorer:\n    context_anchors:\n      - 'guides/non_existent.md'"
    )
    assert validate_assemblage.check_wiring_integrity() is False

def test_main_exit_code_success(mock_subprocess_run, temp_assemblage_files, monkeypatch):
    """Test that main() exits with 0 on full success."""
    monkeypatch.chdir(temp_assemblage_files)
    mock_process = MagicMock()
    mock_process.stdout = ""
    mock_subprocess_run.return_value = mock_process
    
    with pytest.raises(SystemExit) as e:
        validate_assemblage.main()
    assert e.type == SystemExit
    assert e.value.code == 0

def test_main_exit_code_failure(mock_subprocess_run, temp_assemblage_files, monkeypatch):
    """Test that main() exits with 1 on any failure."""
    monkeypatch.chdir(temp_assemblage_files)
    mock_process = MagicMock()
    mock_process.stdout = "M README.md" # Git integrity fails
    mock_subprocess_run.return_value = mock_process
    
    with pytest.raises(SystemExit) as e:
        validate_assemblage.main()
    assert e.type == SystemExit
    assert e.value.code == 1
