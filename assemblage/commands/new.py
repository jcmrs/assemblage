"""
assemblage.commands.new

Logic for the 'new' command.
"""

import sys

from assemblage import stager

RED = "\033[0;31m"
NC = "\033[0m"


def run(args):
    """Handler for the 'new' command of the Context Staging System."""
    print("--- Control Plane: Initializing Context Staging System ---")
    try:
        handler = stager.get_stage_handler(
            args.type, args.title, from_adr=args.from_adr, from_item=args.from_item
        )
        briefing = handler.run()
        print(briefing)
        sys.exit(0)
    except (ValueError, FileNotFoundError) as e:
        print(f"{RED}ERROR: Could not create new document: {e}{NC}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
