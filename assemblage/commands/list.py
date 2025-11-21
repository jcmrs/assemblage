"""
assemblage.commands.list

Logic for the 'list' meta-command.
"""

import sys
from pathlib import Path

import yaml

RED = "\033[0;31m"
NC = "\033[0m"
COMMANDS_CONFIG_PATH = Path("config/commands.yml")


def run(args, config_path=COMMANDS_CONFIG_PATH):
    """Lists all available commands from the command registry."""
    print("--- Control Plane: Available Commands ---")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        for cmd_name, cmd_config in config.get("commands", {}).items():
            print(f"\n  {cmd_name}:")
            print(f"    {cmd_config.get('help', 'No description available.')}")

        # Also list built-in commands
        print("\n  list:")
        print("    List all available commands.")
        print("\n  register:")
        print("    Register a new command.")
        print("\n---------------------------------------")
        sys.exit(0)

    except FileNotFoundError:
        print(
            f"{RED}FATAL ERROR: Command registry not found at " f"'{config_path}'.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
