"""
test_validate.py

Tests for the 'validate' command.
"""

from unittest.mock import MagicMock, patch

from assemblage.commands import validate


@patch("assemblage.commands.validate.subprocess.run")
def test_validate_all_pass(mock_subprocess_run, tmp_path, monkeypatch):
    """Tests the validate command when all checks pass."""
    monkeypatch.chdir(tmp_path)

    # Mock git status to return no changes
    mock_subprocess_run.return_value = MagicMock(stdout="")

    # Create necessary files for checks
    (tmp_path / "ASSEMBLAGE.version").write_text("1.2.3")
    (tmp_path / "CHANGELOG.md").write_text("## [1.2.3] - 2025-11-19")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "workbenches.yml").write_text("workbenches: {}")
    (tmp_path / "config" / "specialists.yml").write_text("specialists: {}")

    with patch.object(validate.sys, "exit") as mock_exit:
        validate.run(None)
        mock_exit.assert_called_once_with(0)


@patch("assemblage.commands.validate.subprocess.run")
def test_validate_git_fails(mock_subprocess_run, tmp_path, monkeypatch):
    """Tests the validate command when the git integrity check fails."""
    monkeypatch.chdir(tmp_path)

    # Mock git status to return changes
    mock_subprocess_run.return_value = MagicMock(stdout=" M README.md")

    # Create other necessary files
    (tmp_path / "ASSEMBLAGE.version").write_text("1.2.3")
    (tmp_path / "CHANGELOG.md").write_text("## [1.2.3] - 2025-11-19")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "workbenches.yml").write_text("workbenches: {}")
    (tmp_path / "config" / "specialists.yml").write_text("specialists: {}")

    with patch.object(validate.sys, "exit") as mock_exit:
        validate.run(None)
        mock_exit.assert_called_once_with(1)


@patch("assemblage.commands.validate.subprocess.run")
def test_validate_version_fails(mock_subprocess_run, tmp_path, monkeypatch):
    """Tests the validate command when the version alignment check fails."""
    monkeypatch.chdir(tmp_path)

    mock_subprocess_run.return_value = MagicMock(stdout="")

    (tmp_path / "ASSEMBLAGE.version").write_text("1.2.3")
    (tmp_path / "CHANGELOG.md").write_text("## [1.2.4] - 2025-11-20")  # Mismatch
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "workbenches.yml").write_text("workbenches: {}")
    (tmp_path / "config" / "specialists.yml").write_text("specialists: {}")

    with patch.object(validate.sys, "exit") as mock_exit:
        validate.run(None)
        mock_exit.assert_called_once_with(1)
