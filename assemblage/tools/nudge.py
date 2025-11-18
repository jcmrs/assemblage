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

def deliver_nudge(nudge_id, current_workbench):
    """
    Checks firewall rules and delivers a nudge if available.
    Returns True on success, False on failure.
    """
    try:
        with open(WORKBENCH_CONFIG, "r") as f:
            workbenches_data = yaml.safe_load(f)
        with open(NUDGE_LIBRARY, "r") as f:
            nudges_data = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"{RED}ERROR: Configuration file not found: {e}{NC}", file=sys.stderr)
        return False

    # Firewall Logic
    try:
        available_nudges = workbenches_data["workbenches"][current_workbench][
            "available_nudges"
        ]
    except KeyError:
        print(
            f"{RED}ERROR: Workbench '{current_workbench}' not found in {WORKBENCH_CONFIG}{NC}",
            file=sys.stderr,
        )
        return False

    if nudge_id not in available_nudges:
        print(
            f"{RED}[NUDGE FAIL] Nudge '{nudge_id}' is NOT available for the '{current_workbench}' Workbench.{NC}",
            file=sys.stderr,
        )
        print(
            f"{YELLOW}This is a 'How' (Platform) Guardrail to prevent 'interference'.{NC}",
            file=sys.stderr,
        )
        return False

    # Nudge Delivery
    nudge_text = nudges_data.get("nudges", {}).get(nudge_id)

    if not nudge_text:
        print(
            f"{RED}ERROR: Nudge ID '{nudge_id}' does not exist in the Nudge Library.{NC}",
            file=sys.stderr,
        )
        return False

    # Success
    print(f"\n{CYAN}💡 NUDGE ({nudge_id}):{NC}")
    print(f"{CYAN}---------------------------------{NC}")
    print(nudge_text)
    print(f"{CYAN}---------------------------------{NC}\n")
    return True
