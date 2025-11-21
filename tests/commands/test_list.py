"""
test_list.py

Tests for the 'list' meta-command.
"""

from unittest.mock import patch

import yaml

from assemblage.commands import list as list_command


def test_list_run(capsys, tmp_path):
    """
    Tests that the list command correctly reads a given YAML file
    and prints the formatted output.
    """
    # --- Setup ---
    mock_config = {
        "commands": {
            "cmd1": {"help": "Help for cmd1."},
            "cmd2": {"help": "Help for cmd2."},
        }
    }
    config_path = tmp_path / "temp_commands.yml"
    config_path.write_text(yaml.dump(mock_config))

    # --- Execution ---
    with patch.object(list_command.sys, "exit") as mock_exit:
        # Run the command, passing the path to our temp file
        list_command.run(None, config_path=config_path)

        # Capture the output
        captured = capsys.readouterr()

        # --- Assertions ---
        assert "cmd1:" in captured.out
        assert "Help for cmd1." in captured.out
        assert "cmd2:" in captured.out
        assert "Help for cmd2." in captured.out
        assert "list:" in captured.out
        assert "register:" in captured.out
        mock_exit.assert_called_once_with(0)
