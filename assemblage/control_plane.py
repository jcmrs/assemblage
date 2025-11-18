"""
control_plane.py

This module is the central, abstract entry point for all agent-tool
interactions within the Assemblage. It decouples the agent's intent from
the specific implementation of the tools.
"""

import argparse
import sys

from assemblage.tools import (
    create_new_specialist,
    dashboard_generator,
    nudge,
    validate_assemblage,
)


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


def validate_command(args):
    """Handler for the 'validate' command."""
    print("--- Control Plane: Executing 'validate' ---")
    if validate_assemblage.validate():
        sys.exit(0)
    else:
        sys.exit(1)


def create_specialist_command(args):
    """Handler for the 'create_specialist' command."""
    print("--- Control Plane: Launching 'create_specialist' ---")
    if create_new_specialist.main():
        sys.exit(0)
    else:
        sys.exit(1)


def nudge_command(args):
    """Handler for the 'nudge' command."""
    print("--- Control Plane: Executing 'nudge' ---")
    if nudge.deliver_nudge(args.nudge_id, args.current_workbench):
        sys.exit(0)
    else:
        sys.exit(1)


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

    # Define the 'observe' command
    parser_observe = subparsers.add_parser(
        "observe",
        help="Observe the state of the Assemblage and generate a status dashboard.",
    )
    parser_observe.set_defaults(func=observe_command)

    # Define the 'validate' command
    parser_validate = subparsers.add_parser(
        "validate", help="Run a full integrity check of the Assemblage."
    )
    parser_validate.set_defaults(func=validate_command)

    # Define the 'create_specialist' command
    parser_create_specialist = subparsers.add_parser(
        "create_specialist",
        help="Launch the interactive wizard to create a new Cognitive Specialist.",
    )
    parser_create_specialist.set_defaults(func=create_specialist_command)

    # Define the 'nudge' command
    parser_nudge = subparsers.add_parser("nudge", help="Deliver a behavioral nudge.")
    parser_nudge.add_argument("nudge_id", help="The ID of the nudge to deliver.")
    parser_nudge.add_argument("current_workbench", help="The active workbench.")
    parser_nudge.set_defaults(func=nudge_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
