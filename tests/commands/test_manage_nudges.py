"""
tests.commands.test_manage_nudges

Tests for the nudge management commands.
"""

import sys
from unittest.mock import MagicMock

import pytest

# Mock the ConfigManager before importing the module to be tested
mock_config_manager = MagicMock()
sys.modules["assemblage.config_manager"] = MagicMock(ConfigManager=mock_config_manager)

from assemblage.commands import manage_nudges  # noqa: E402


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset mocks before each test."""
    mock_config_manager.reset_mock()
    # We need to mock the instance methods as well
    mock_instance = MagicMock()
    mock_config_manager.return_value = mock_instance
    yield mock_instance


def test_add_success(reset_mocks, capsys):
    """Tests successful addition of a nudge."""
    mock_instance = reset_mocks
    args = MagicMock(id="new_nudge", text="Do the thing.")

    with pytest.raises(SystemExit) as e:
        manage_nudges.add(args)

    assert e.value.code == 0
    mock_instance.add_entry.assert_called_once_with("new_nudge", "Do the thing.")
    captured = capsys.readouterr()
    assert "Successfully added nudge" in captured.out


def test_add_failure(reset_mocks, capsys):
    """Tests failed addition of a nudge."""
    mock_instance = reset_mocks
    mock_instance.add_entry.side_effect = KeyError("Entry already exists.")
    args = MagicMock(id="new_nudge", text="Do the thing.")

    with pytest.raises(SystemExit) as e:
        manage_nudges.add(args)

    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Entry already exists." in captured.err


def test_remove_success(reset_mocks, capsys):
    """Tests successful removal of a nudge."""
    mock_instance = reset_mocks
    args = MagicMock(id="old_nudge")

    with pytest.raises(SystemExit) as e:
        manage_nudges.remove(args)

    assert e.value.code == 0
    mock_instance.remove_entry.assert_called_once_with("old_nudge")
    captured = capsys.readouterr()
    assert "Successfully removed nudge" in captured.out


def test_update_success(reset_mocks, capsys):
    """Tests successful update of a nudge."""
    mock_instance = reset_mocks
    args = MagicMock(id="existing_nudge", text="Do the new thing.")

    with pytest.raises(SystemExit) as e:
        manage_nudges.update(args)

    assert e.value.code == 0
    mock_instance.update_entry.assert_called_once_with(
        "existing_nudge", "Do the new thing."
    )
    captured = capsys.readouterr()
    assert "Successfully updated nudge" in captured.out
