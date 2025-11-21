"""
assemblage.commands.status

Logic for the 'status' command.
"""

import json
import sys
from datetime import datetime

from assemblage import code_search

RED = "\033[0;31m"
NC = "\033[0m"


def run(args):
    """Handler for the 'status' command."""
    if args.index:
        print("--- Control Plane: Checking 'index' status ---")
        if code_search.INDEX_PATH.exists():
            mod_time = datetime.fromtimestamp(
                code_search.INDEX_PATH.stat().st_mtime
            ).isoformat()
            with open(code_search.METADATA_PATH, "r") as f:
                item_count = len(json.load(f))
            print("✅ Index found.")
            print(f"   - Last built: {mod_time}")
            print(f"   - Indexed items: {item_count}")
        else:
            print("❌ Index not found. Run 'control_plane index' to build it.")
        sys.exit(0)
    else:
        print("Please specify a status to check (e.g., --index).")
        sys.exit(1)
