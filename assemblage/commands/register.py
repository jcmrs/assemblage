"""
assemblage.commands.register

Logic for the 'register' meta-command.
"""

import sys
from pathlib import Path

import yaml

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

COMMANDS_CONFIG_PATH = Path("config/commands.yml")


def _prompt_user(prompt_text):
    """Prints a prompt and returns sanitized user input."""
    print(f"\n{BLUE}[PROMPT] {prompt_text}{NC}", file=sys.stderr)
    return sys.stdin.readline().strip()


def run(args):
    """Interactively registers a new command in config/commands.yml."""
    print(f"{GREEN}--- Starting New Command Registration ---{NC}")

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

    cmd_name = _prompt_user("Enter the name of the new command (e.g., 'my_command'):")
    if not cmd_name:
        print(f"{RED}ERROR: Command name cannot be empty.{NC}", file=sys.stderr)
        sys.exit(1)

    if cmd_name in config.get("commands", {}):
        print(f"{RED}ERROR: Command '{cmd_name}' already exists.{NC}", file=sys.stderr)
        sys.exit(1)

    entry_point = _prompt_user(
        "Enter the Python entry point (e.g., 'assemblage.commands.my_command.run'):"
    )
    help_text = _prompt_user("Enter the one-line help text for this command:")

    new_command_config = {"entry_point": entry_point, "help": help_text}

    # Optional: Add arguments
    if _prompt_user("Does this command have arguments? (y/n)").lower() == "y":
        arguments = []
        while True:
            arg_name = _prompt_user(
                "Enter argument name (e.g., 'my_arg' or '--my-flag'):"
            )
            if not arg_name:
                break
            arg_help = _prompt_user(f"Enter help text for '{arg_name}':")
            arg_dict = {"name": arg_name, "help": arg_help}

            if _prompt_user("Is this a flag (e.g., store_true)? (y/n)").lower() == "y":
                arg_dict["action"] = "store_true"

            if _prompt_user("Is this argument required? (y/n)").lower() == "y":
                arg_dict["required"] = True

            arguments.append(arg_dict)
            if _prompt_user("Add another argument? (y/n)").lower() != "y":
                break
        new_command_config["arguments"] = arguments

    if "commands" not in config:
        config["commands"] = {{}}
    config["commands"][cmd_name] = new_command_config

    try:
        with open(COMMANDS_CONFIG_PATH, "w") as f:
            yaml.dump(config, f, indent=2, default_flow_style=False, sort_keys=False)
        print(
            f"\n{GREEN}✅ Command '{cmd_name}' successfully registered in "
            f"'{COMMANDS_CONFIG_PATH}'.{NC}"
        )
        sys.exit(0)
    except Exception as e:
        print(
            f"An unexpected error occurred while writing to file: {e}", file=sys.stderr
        )
        sys.exit(1)
