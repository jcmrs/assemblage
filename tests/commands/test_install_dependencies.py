"""
test_install_dependencies.py

Tests for the 'install_dependencies' command.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from assemblage.commands import install_dependencies


@patch("assemblage.commands.install_dependencies.subprocess.run")
def test_install_success(mock_subprocess_run, capsys):
    """
    Tests the success case where pip returns a 0 exit code.
    """
    # --- Arrange ---
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    # --- Act & Assert ---
    with pytest.raises(SystemExit) as e:
        install_dependencies.run(None)

    # Check that the exit code is 0
    assert e.value.code == 0

    # Check that subprocess.run was called correctly
    expected_cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    mock_subprocess_run.assert_called_once_with(
        expected_cmd,
        check=False,
        text=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    # Check that a success message was printed
    captured = capsys.readouterr()
    assert "Dependencies are up to date" in captured.out


@patch("assemblage.commands.install_dependencies.subprocess.run")
def test_install_failure(mock_subprocess_run, capsys):
    """
    Tests the failure case where pip returns a non-zero exit code.
    """
    # --- Arrange ---
    mock_subprocess_run.return_value = MagicMock(returncode=1)

    # --- Act & Assert ---
    with pytest.raises(SystemExit) as e:
        install_dependencies.run(None)

    # Check that the exit code is 1
    assert e.value.code == 1

    # Check that subprocess.run was called correctly
    expected_cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    mock_subprocess_run.assert_called_once_with(
        expected_cmd,
        check=False,
        text=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    # Check that a failure message was printed
    captured = capsys.readouterr()
    assert "Dependency installation failed" in captured.out
