"""
test_control_plane.py

Tests for the refactored, dynamic Control Plane.
"""

from unittest.mock import MagicMock, patch

import pytest
import yaml

from assemblage import control_plane


@pytest.fixture
def mock_config_file(tmp_path):
    """Creates a temporary commands.yml file."""
    config_content = {
        "commands": {
            "test_cmd": {
                "entry_point": "assemblage.commands.test_cmd.run",
                "help": "A test command.",
                "arguments": [
                    {"name": "--flag", "action": "store_true", "help": "A test flag."}
                ],
            }
        }
    }
    config_path = tmp_path / "commands.yml"
    with open(config_path, "w") as f:
        yaml.dump(config_content, f)
    return config_path


@patch("importlib.import_module")
def test_dynamic_command_loading_and_execution(mock_import_module, mock_config_file):
    """
    Tests that the control plane can load a command from YAML, parse args,
    and call the correct entry point.
    """
    # --- Setup Mocks ---
    # Mock the module and function that should be dynamically imported
    mock_command_module = MagicMock()
    mock_run_function = MagicMock()
    mock_command_module.run = mock_run_function
    mock_import_module.return_value = mock_command_module

    # Mock sys.argv to simulate command line input
    test_argv = ["control_plane.py", "test_cmd", "--flag"]

    # --- Patching ---
    with patch.object(control_plane, "COMMANDS_CONFIG_PATH", mock_config_file):
        with patch.object(control_plane.sys, "argv", test_argv):
            # --- Execution ---
            control_plane.main()

    # --- Assertions ---
    # Assert that the correct module was imported
    mock_import_module.assert_called_once_with("assemblage.commands.test_cmd")

    # Assert that the 'run' function was called
    mock_run_function.assert_called_once()

    # Assert that the parsed arguments were passed to the 'run' function
    called_args = mock_run_function.call_args[0][0]
    assert called_args.command == "test_cmd"
    assert called_args.flag is True


def test_list_command_entry_point():
    """Tests that the built-in 'list' command is wired up."""
    test_argv = ["control_plane.py", "list"]
    with patch.object(control_plane.sys, "argv", test_argv):
        with patch("importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_import.return_value = mock_module

            control_plane.main()

            mock_import.assert_called_once_with("assemblage.commands.list")
            mock_module.run.assert_called_once()
