"""
assemblage.commands.index

Logic for the 'index' command.
"""

import sys

from assemblage import code_search

RED = "\033[0;31m"
NC = "\033[0m"


def run(args):
    """Handler for the 'index' command."""
    print("--- Control Plane: Executing 'index' ---")
    try:
        code_search.build_index()
        sys.exit(0)
    except Exception as e:
        print(f"{RED}ERROR: Indexing failed: {e}{NC}", file=sys.stderr)
        sys.exit(1)
