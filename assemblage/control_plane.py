"""
control_plane.py

This module is the central, abstract entry point for all agent-tool
interactions within the Assemblage. It decouples the agent's intent from
the specific implementation of the tools.
"""

import argparse
import sys

from assemblage.tools import dashboard_generator

def observe_command(args):
    """Handler for the 'observe' command."""
    print("--- Control Plane: Executing 'observe' ---")
    try:
        dashboard_generator.generate()
        print("--- 'observe' command completed successfully. ---")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: The 'observe' command failed: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main entry point for the Assemblage Control Plane.
    Parses commands and dispatches them to the appropriate handlers.
    """
    parser = argparse.ArgumentParser(
        description="Assemblage Control Plane: Abstract interface for agent-tool interaction."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Define the 'observe' command
    parser_observe = subparsers.add_parser(
        "observe", help="Observe the state of the Assemblage and generate a status dashboard."
    )
    parser_observe.set_defaults(func=observe_command)

    # Add future commands here (e.g., validate, nudge)
    # parser_validate = subparsers.add_parser("validate", help="...")
    # parser_validate.set_defaults(func=validate_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
