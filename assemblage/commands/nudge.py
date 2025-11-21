"""
assemblage.commands.nudge

Logic for the 'nudge' command.
"""

import sys
from pathlib import Path

import yaml

# --- Constants and ANSI Colors ---
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"


def run(args):
    """Checks firewall rules and delivers a nudge if available."""
    nudge_id = args.nudge_id
    current_workbench = args.current_workbench

    workbench_config = Path("config/workbenches.yml")
    nudge_library = Path("config/nudges.yml")

    try:
        with open(workbench_config, "r") as f:
            workbenches_data = yaml.safe_load(f)
        with open(nudge_library, "r") as f:
            nudges_data = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"{RED}ERROR: Configuration file not found: {e}{NC}", file=sys.stderr)
        sys.exit(1)

    try:
        available_nudges = workbenches_data["workbenches"][current_workbench][
            "available_nudges"
        ]
    except KeyError:
        print(
            f"{RED}ERROR: Workbench '{current_workbench}' not found in "
            f"{workbench_config}{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    if nudge_id not in available_nudges:
        print(
            f"{RED}[NUDGE FAIL] Nudge '{nudge_id}' is NOT available for the "
            f"'{current_workbench}' Workbench.{NC}",
            file=sys.stderr,
        )
        print(
            f"{YELLOW}This is a 'How' (Platform) Guardrail to prevent "
            f"'interference'.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    nudge_text = nudges_data.get("nudges", {}).get(nudge_id)
    if not nudge_text:
        print(
            f"{RED}ERROR: Nudge ID '{nudge_id}' does not exist in the Nudge "
            f"Library.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"\n{CYAN}💡 NUDGE ({nudge_id}):{NC}")
    print(f"{CYAN}---------------------------------{NC}")
    print(nudge_text)
    print(f"{CYAN}---------------------------------{NC}\n")
    sys.exit(0)
