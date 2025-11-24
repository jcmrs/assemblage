"""
assemblage.commands.manage_nudges

Provides commands for managing entries in the config/nudges.yml file.
"""

import sys
from pathlib import Path

from assemblage.config_manager import ConfigManager

# --- Constants and ANSI Colors ---
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

NUDGES_PATH = Path("config/nudges.yml")


def add(args):
    """Adds a new nudge."""
    try:
        manager = ConfigManager(NUDGES_PATH)
        manager.add_entry(args.id, args.text)
        print(f"{GREEN}Successfully added nudge '{args.id}'.{NC}")
        sys.exit(0)
    except (KeyError, Exception) as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)


def remove(args):
    """Removes an existing nudge."""
    try:
        manager = ConfigManager(NUDGES_PATH)
        manager.remove_entry(args.id)
        print(f"{GREEN}Successfully removed nudge '{args.id}'.{NC}")
        sys.exit(0)
    except (KeyError, Exception) as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)


def update(args):
    """Updates an existing nudge."""
    try:
        manager = ConfigManager(NUDGES_PATH)
        manager.update_entry(args.id, args.text)
        print(f"{GREEN}Successfully updated nudge '{args.id}'.{NC}")
        sys.exit(0)
    except (KeyError, Exception) as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)
