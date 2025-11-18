"""
nudge.py

This utility acts as a "firewall" for behavioral nudges, delivering a
microprompt from a library if it is available for the given workbench.
"""

import argparse
import sys
from pathlib import Path
import yaml

# --- Constants ---
WORKBENCH_CONFIG = Path("config/workbenches.yml")
NUDGE_LIBRARY = Path("config/nudges.yml")
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

def main():
    """Main function to parse args and deliver a nudge."""
    parser = argparse.ArgumentParser(
        description="Deliver a behavioral nudge based on the current workbench."
    )
    parser.add_argument("nudge_id", help="The unique ID of the nudge to deliver.")
    parser.add_argument(
        "current_workbench", help="The ID of the currently active workbench."
    )
    args = parser.parse_args()

    try:
        with open(WORKBENCH_CONFIG, "r") as f:
            workbenches_data = yaml.safe_load(f)
        with open(NUDGE_LIBRARY, "r") as f:
            nudges_data = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"{RED}ERROR: Configuration file not found: {e}{NC}", file=sys.stderr)
        sys.exit(1)

    # Firewall Logic
    try:
        available_nudges = workbenches_data["workbenches"][args.current_workbench][
            "available_nudges"
        ]
    except KeyError:
        print(
            f"{RED}ERROR: Workbench '{args.current_workbench}' not found in {WORKBENCH_CONFIG}{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.nudge_id not in available_nudges:
        print(
            f"{RED}[NUDGE FAIL] Nudge '{args.nudge_id}' is NOT available for the '{args.current_workbench}' Workbench.{NC}",
            file=sys.stderr,
        )
        print(
            f"{YELLOW}This is a 'How' (Platform) Guardrail to prevent 'interference'.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Nudge Delivery
    nudge_text = nudges_data.get("nudges", {}).get(args.nudge_id)

    if not nudge_text:
        print(
            f"{RED}ERROR: Nudge ID '{args.nudge_id}' does not exist in the Nudge Library.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Success
    print(f"\n{CYAN}💡 NUDGE ({args.nudge_id}):{NC}")
    print(f"{CYAN}---------------------------------{NC}")
    print(nudge_text)
    print(f"{CYAN}---------------------------------{NC}\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
