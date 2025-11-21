"""
test_register.py

Tests for the 'register' meta-command.
"""

from unittest.mock import patch

import yaml

from assemblage.commands import register


def test_register_new_command_no_args(tmp_path):
    """
    Tests the successful registration of a new command without arguments.
    """
    # --- Setup ---
    # Initial empty config file
    initial_config_path = tmp_path / "commands.yml"
    initial_config_path.write_text(yaml.dump({"commands": {}}))

    # Mock user input
    mock_input = [
        "new_cmd",  # Command name
        "my.entry.point",  # Entry point
        "My help text.",  # Help text
        "n",  # No arguments
    ]

    # --- Mocking and Execution ---
    with patch.object(register, "COMMANDS_CONFIG_PATH", initial_config_path):
        with patch("sys.stdin.readline", side_effect=mock_input):
            with patch.object(register.sys, "exit") as mock_exit:
                register.run(None)

    # --- Assertions ---
    # Check that the file was written correctly
    final_config = yaml.safe_load(initial_config_path.read_text())

    assert "new_cmd" in final_config["commands"]
    assert final_config["commands"]["new_cmd"]["entry_point"] == "my.entry.point"
    assert final_config["commands"]["new_cmd"]["help"] == "My help text."
    assert "arguments" not in final_config["commands"]["new_cmd"]

    mock_exit.assert_called_once_with(0)


def test_register_new_command_with_args(tmp_path):
    """
    Tests the successful registration of a new command with arguments.
    """
    # --- Setup ---
    initial_config_path = tmp_path / "commands.yml"
    initial_config_path.write_text(yaml.dump({"commands": {}}))

    mock_input = [
        "another_cmd",  # Command name
        "another.entry.point",  # Entry point
        "More help.",  # Help text
        "y",  # Yes, it has arguments
        "--flag1",  # First arg name
        "Flag 1 help.",  # First arg help
        "y",  # Yes, it's a flag
        "n",  # Not required
        "y",  # Yes, add another argument
        "pos_arg",  # Second arg name
        "Positional arg help.",  # Second arg help
        "n",  # Not a flag
        "y",  # Yes, it's required
        "n",  # No more arguments
    ]

    # --- Mocking and Execution ---
    with patch.object(register, "COMMANDS_CONFIG_PATH", initial_config_path):
        with patch("sys.stdin.readline", side_effect=mock_input):
            with patch.object(register.sys, "exit") as mock_exit:
                register.run(None)

    # --- Assertions ---
    final_config = yaml.safe_load(initial_config_path.read_text())

    new_cmd_config = final_config["commands"]["another_cmd"]
    assert new_cmd_config["entry_point"] == "another.entry.point"

    args = new_cmd_config["arguments"]
    assert len(args) == 2

    assert args[0]["name"] == "--flag1"
    assert args[0]["action"] == "store_true"

    assert args[1]["name"] == "pos_arg"
    assert args[1]["required"] is True

    mock_exit.assert_called_once_with(0)
