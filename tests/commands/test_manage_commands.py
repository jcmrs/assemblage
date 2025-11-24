"""
tests.commands.test_manage_commands

Tests for the command management commands.
"""

import sys
from unittest.mock import MagicMock

import pytest

# Mock dependencies before importing the module to be tested
mock_config_manager = MagicMock()
sys.modules["assemblage.config_manager"] = MagicMock(ConfigManager=mock_config_manager)

mock_validator = MagicMock()
sys.modules["assemblage.validators"] = MagicMock(validate_entry_point=mock_validator)

from assemblage.commands import manage_commands  # noqa: E402


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset mocks before each test."""
    mock_config_manager.reset_mock()
    mock_validator.reset_mock()
    mock_validator.side_effect = None  # Explicitly reset side_effect
    mock_instance = MagicMock()
    # Configure the mock instance that will be returned by ConfigManager()
    mock_config_manager.return_value = mock_instance
    yield mock_instance


def create_args_mock(name, entry_point=None, help_text=None):
    """Helper to create a mock that behaves like argparse.Namespace."""
    mock = MagicMock()
    mock.name = name
    mock.entry_point = entry_point
    mock.help = help_text
    return mock


def test_add_success(reset_mocks, capsys):
    """Tests successful addition of a command."""
    mock_instance = reset_mocks
    args = create_args_mock(
        name="new-cmd", entry_point="path:func", help_text="A new command."
    )

    with pytest.raises(SystemExit) as e:
        manage_commands.add(args)

    assert e.value.code == 0
    mock_validator.assert_called_once_with("path:func")
    mock_instance.add_entry.assert_called_once_with(
        "new-cmd", {"entry_point": "path:func", "help": "A new command.", "args": []}
    )
    captured = capsys.readouterr()
    assert "Successfully added command" in captured.out


def test_add_validation_fails(reset_mocks, capsys):
    """Tests that the command fails if entry point validation fails."""
    mock_instance = reset_mocks
    mock_validator.side_effect = ImportError("Module not found.")
    args = create_args_mock(
        name="new-cmd", entry_point="bad:path", help_text="A new command."
    )

    with pytest.raises(SystemExit) as e:
        manage_commands.add(args)

    assert e.value.code == 1
    mock_validator.assert_called_once_with("bad:path")
    mock_instance.add_entry.assert_not_called()
    captured = capsys.readouterr()
    assert "Error: Module not found." in captured.err


def test_remove_success(reset_mocks, capsys):
    """Tests successful removal of a command."""
    mock_instance = reset_mocks
    args = create_args_mock(name="old-cmd")

    with pytest.raises(SystemExit) as e:
        manage_commands.remove(args)

    assert e.value.code == 0
    mock_instance.remove_entry.assert_called_once_with("old-cmd")
    captured = capsys.readouterr()
    assert "Successfully removed command" in captured.out


def test_update_success_all_fields(reset_mocks, capsys):
    """Tests successful update of a command with all fields."""
    mock_instance = reset_mocks
    mock_instance.read_config.return_value = {
        "existing-cmd": {"entry_point": "old:path", "help": "Old help."}
    }
    args = create_args_mock(
        name="existing-cmd", entry_point="new:path", help_text="New help."
    )

    with pytest.raises(SystemExit) as e:
        manage_commands.update(args)

    assert e.value.code == 0
    mock_validator.assert_called_once_with("new:path")
    mock_instance.update_entry.assert_called_once_with(
        "existing-cmd", {"entry_point": "new:path", "help": "New help."}
    )
    captured = capsys.readouterr()
    assert "Successfully updated command" in captured.out
