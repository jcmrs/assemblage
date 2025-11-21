"""
control_plane.py

This module is the central, abstract entry point for all agent-tool
interactions within the Assemblage. It is a dynamic command loader that
builds its capabilities from a declarative configuration file.
"""

import argparse
import importlib
import sys
from pathlib import Path

import yaml

# --- Constants ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

COMMANDS_CONFIG_PATH = Path("config/commands.yml")


def main():
    """
    Main entry point for the Assemblage Control Plane.
    Parses commands and dispatches them to the appropriate handlers.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Assemblage Control Plane: Abstract interface for agent-tool interaction."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Dynamic Command Loading ---
    try:
        with open(COMMANDS_CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(
            f"{RED}FATAL ERROR: Command registry not found at "
            f"'{COMMANDS_CONFIG_PATH}'.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    for cmd_name, cmd_config in config.get("commands", {}).items():
        sub_parser = subparsers.add_parser(cmd_name, help=cmd_config.get("help"))

        # Dynamically add arguments
        for arg in cmd_config.get("arguments", []):
            arg_name = arg.pop("name")
            sub_parser.add_argument(arg_name, **arg)

        # Set the entry point for the command
        sub_parser.set_defaults(entry_point=cmd_config["entry_point"])

    # --- Built-in Meta-Commands (not in YAML) ---
    # 'list' command
    list_parser = subparsers.add_parser("list", help="List all available commands.")
    list_parser.set_defaults(entry_point="assemblage.commands.list.run")

    # 'register' command
    register_parser = subparsers.add_parser("register", help="Register a new command.")
    register_parser.set_defaults(entry_point="assemblage.commands.register.run")

    args = parser.parse_args()

    # --- Dynamic Command Execution ---
    try:
        module_path, function_name = args.entry_point.rsplit(".", 1)
        module = importlib.import_module(module_path)
        command_function = getattr(module, function_name)
        command_function(args)
    except (ImportError, AttributeError) as e:
        print(
            f"{RED}FATAL ERROR: Could not load entry point '{args.entry_point}': "
            f"{e}{NC}",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(
            f"{RED}An unexpected error occurred while running command "
            f"'{args.command}': {e}{NC}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
