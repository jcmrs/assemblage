"""
test_observe.py

Tests for the 'observe' command.
"""

import json
from unittest.mock import MagicMock, patch

from assemblage.commands import observe


@patch("subprocess.run")
def test_observe_run_success(mock_subprocess_run, tmp_path, monkeypatch):
    """
    Tests the successful run of the observe command.
    """
    # --- Setup Mocks ---
    # Mock the git log command
    git_log_output = "abcde|Commit message 1\nfghij|Commit message 2"
    mock_subprocess_run.return_value = MagicMock(
        capture_output=True, text=True, check=True, stdout=git_log_output
    )

    # Create mock file structure
    (tmp_path / "ASSEMBLAGE.version").write_text("1.0.0")
    (tmp_path / "ideas").mkdir()
    (tmp_path / "ideas" / "idea1.md").touch()
    (tmp_path / "backlog" / "items").mkdir(parents=True)
    (tmp_path / "backlog" / "items" / "item1.md").touch()
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "spec1").mkdir()

    # --- Patching and Execution ---
    # Change the current working directory to the temporary directory for the test
    monkeypatch.chdir(tmp_path)
    with patch.object(observe.sys, "exit") as mock_exit:
        observe.run(None)

    # --- Assertions ---
    # Check that the JSON and MD files were created
    json_output_path = tmp_path / "status.json"
    md_output_path = tmp_path / "STATUS.md"
    assert json_output_path.exists()
    assert md_output_path.exists()

    # Check the content of the JSON file
    with open(json_output_path, "r") as f:
        data = json.load(f)

    assert data["assemblage_health"]["version"] == "1.0.0"
    assert data["project_progress"]["conveyor_belt"]["ideas"] == 1
    assert data["project_progress"]["conveyor_belt"]["backlog"] == 1
    assert len(data["project_progress"]["recent_activity"]) == 2
    assert data["project_progress"]["recent_activity"][0]["hash"] == "abcde"

    mock_exit.assert_called_once_with(0)
