"""
test_control_plane.py

Tests for the main control_plane module.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from assemblage import control_plane


def test_observe_command_success(monkeypatch):
    """
    Tests that the 'observe' command successfully calls the internal logic.
    """
    mock_generate = MagicMock(return_value=True)
    monkeypatch.setattr(control_plane, "_generate_dashboard", mock_generate)
    monkeypatch.setattr(sys, "argv", ["control_plane.py", "observe"])

    with pytest.raises(SystemExit) as e:
        control_plane.main()

    assert e.value.code == 0
    mock_generate.assert_called_once()


def test_invalid_command(capsys):
    """
    Tests that an invalid command exits with an error.
    """
    with patch("sys.argv", ["control_plane.py", "invalid_command"]):
        with pytest.raises(SystemExit) as e:
            control_plane.main()

        assert e.value.code != 0
        captured = capsys.readouterr()
        assert "usage: control_plane.py" in captured.err
        assert "invalid choice: 'invalid_command'" in captured.err


def test_validate_command_success(monkeypatch):
    """
    Tests that the 'validate' command exits with 0 on success.
    """
    mock_validate = MagicMock(return_value=True)
    monkeypatch.setattr(control_plane, "_validate_assemblage", mock_validate)
    monkeypatch.setattr(sys, "argv", ["control_plane.py", "validate"])

    with pytest.raises(SystemExit) as e:
        control_plane.main()

    assert e.value.code == 0
    mock_validate.assert_called_once()


def test_validate_command_failure(monkeypatch):
    """
    Tests that the 'validate' command exits with 1 on failure.
    """
    mock_validate = MagicMock(return_value=False)
    monkeypatch.setattr(control_plane, "_validate_assemblage", mock_validate)
    monkeypatch.setattr(sys, "argv", ["control_plane.py", "validate"])

    with pytest.raises(SystemExit) as e:
        control_plane.main()

    assert e.value.code == 1
    mock_validate.assert_called_once()


def test_create_specialist_command_success(monkeypatch):
    """
    Tests that the 'create_specialist' command exits with 0 on success.
    """
    mock_create = MagicMock(return_value=True)
    monkeypatch.setattr(control_plane, "_create_new_specialist", mock_create)
    monkeypatch.setattr(sys, "argv", ["control_plane.py", "create_specialist"])

    with pytest.raises(SystemExit) as e:
        control_plane.main()

    assert e.value.code == 0


def test_nudge_command_success(monkeypatch):
    """
    Tests that the 'nudge' command exits with 0 on success.
    """
    mock_nudge = MagicMock(return_value=True)
    monkeypatch.setattr(control_plane, "_deliver_nudge", mock_nudge)
    monkeypatch.setattr(
        sys, "argv", ["control_plane.py", "nudge", "some_nudge", "some_workbench"]
    )

    with pytest.raises(SystemExit) as e:
        control_plane.main()

    assert e.value.code == 0
    mock_nudge.assert_called_once_with("some_nudge", "some_workbench")


def test_nudge_command_failure(monkeypatch):
    """
    Tests that the 'nudge' command exits with 1 on failure.
    """
    mock_nudge = MagicMock(return_value=False)
    monkeypatch.setattr(control_plane, "_deliver_nudge", mock_nudge)
    monkeypatch.setattr(
        sys, "argv", ["control_plane.py", "nudge", "blocked_nudge", "builder"]
    )

    with pytest.raises(SystemExit) as e:
        control_plane.main()

    assert e.value.code == 1
    mock_nudge.assert_called_once_with("blocked_nudge", "builder")
