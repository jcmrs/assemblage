"""
test_generate_dashboard.py

Tests for the generate_dashboard utility.
"""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from assemblage.tools import generate_dashboard

# Constants
OUTPUT_MD = Path("STATUS.md")
OUTPUT_JSON = Path("status.json")

@pytest.fixture(autouse=True)
def cleanup_files():
    """
    Fixture to automatically clean up generated files after each test.
    """
    yield
    if OUTPUT_MD.exists():
        OUTPUT_MD.unlink()
    if OUTPUT_JSON.exists():
        OUTPUT_JSON.unlink()

def test_script_runs_successfully_and_creates_files():
    """
    Tests that the main function runs without errors and creates the output files.
    """
    # We patch the subprocess call to avoid running git in tests
    with patch("subprocess.run") as mock_run:
        # Mock the return value of the git log command
        mock_process = MagicMock()
        mock_process.stdout = "abcdef1|Test commit"
        mock_run.return_value = mock_process

        generate_dashboard.main()

        assert OUTPUT_MD.is_file()
        assert OUTPUT_JSON.is_file()

def test_json_output_is_valid():
    """
    Tests that the generated JSON is valid and contains expected keys.
    """
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = "abcdef1|Test commit"
        mock_run.return_value = mock_process

        generate_dashboard.main()

        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert "assemblage_health" in data
        assert "project_progress" in data
        assert "version" in data["assemblage_health"]
        assert "recent_activity" in data["project_progress"]
        assert data["project_progress"]["recent_activity"][0]["hash"] == "abcdef1"

def test_markdown_output_contains_key_phrases():
    """
    Tests that the generated Markdown file contains expected content.
    """
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = "abcdef1|Test commit"
        mock_run.return_value = mock_process

        generate_dashboard.main()

        content = OUTPUT_MD.read_text(encoding="utf-8")

        assert "Assemblage Status Report" in content
        assert "Framework Version" in content
        assert "Test commit" in content
