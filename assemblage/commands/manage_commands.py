"""
assemblage.commands.manage_commands

Provides commands for managing entries in the config/commands.yml file.
"""

import sys
from pathlib import Path

from assemblage.config_manager import ConfigManager
from assemblage.validators import validate_entry_point

# --- Constants and ANSI Colors ---
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

COMMANDS_PATH = Path("config/commands.yml")


def add(args):
    """Adds a new command."""
    try:
        # 1. Validate the entry point before adding it
        validate_entry_point(args.entry_point)

        # 2. Add to config
        manager = ConfigManager(COMMANDS_PATH)
        command_data = {"entry_point": args.entry_point, "help": args.help, "args": []}
        manager.add_entry(args.name, command_data)
        print(f"{GREEN}Successfully added command '{args.name}'.{NC}")
        sys.exit(0)
    except (ValueError, ImportError, AttributeError, KeyError) as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)


def remove(args):
    """Removes an existing command."""
    try:
        manager = ConfigManager(COMMANDS_PATH)
        manager.remove_entry(args.name)
        print(f"{GREEN}Successfully removed command '{args.name}'.{NC}")
        sys.exit(0)
    except (KeyError, Exception) as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)


def update(args):
    """Updates an existing command."""
    try:
        manager = ConfigManager(COMMANDS_PATH)
        # First, get the existing data
        config = manager.read_config()
        if args.name not in config:
            raise KeyError(f"Command '{args.name}' not found.")

        command_data = config[args.name]

        # Update fields if they were provided
        if args.entry_point:
            validate_entry_point(args.entry_point)
            command_data["entry_point"] = args.entry_point

        if args.help:
            command_data["help"] = args.help

        manager.update_entry(args.name, command_data)
        print(f"{GREEN}Successfully updated command '{args.name}'.{NC}")
        sys.exit(0)
    except (ValueError, ImportError, AttributeError, KeyError) as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)
