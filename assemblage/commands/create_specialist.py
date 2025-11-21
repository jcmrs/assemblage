"""
assemblage.commands.create_specialist

Logic for the 'create_specialist' command.
"""

import sys
from pathlib import Path

import yaml

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"


def _prompt_user(prompt_text):
    """Prints a prompt and returns sanitized user input."""
    print(f"\n{BLUE}[PROMPT] {prompt_text}{NC}", file=sys.stderr)
    return sys.stdin.readline().strip()


def run(args):
    """Main function to orchestrate the specialist creation process."""
    print(f"{GREEN}--- Starting create-new-specialist Utility ---{NC}")
    registry_file = Path("config/specialists.yml")
    if not registry_file.is_file():
        print(
            f"{RED}ERROR: Specialist Registry not found at '{registry_file}'!{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    specialist_id = _prompt_user(
        "Enter the unique ID for the new specialist (e.g., 'mcp_architect'):"
    )
    if not specialist_id:
        print(f"{RED}ERROR: Specialist ID cannot be empty.{NC}", file=sys.stderr)
        sys.exit(1)

    with open(registry_file, "r") as f:
        existing_specialists = yaml.safe_load(f) or {{}}

    if specialist_id in existing_specialists.get("specialists", {{}}):
        print(
            f"{RED}ERROR: Specialist ID '{specialist_id}' already exists.{NC}",
            file=sys.stderr,
        )
        sys.exit(1)

    description = _prompt_user(
        f"Enter the one-sentence description for '{specialist_id}':"
    )
    output_anchor = _prompt_user(
        "Enter the output_anchor path (e.g., 'knowledge/research/report.md'):"
    )
    print(
        f"\n{BLUE}[PROMPT] Enter the multi-line 'guide_prompt' for this "
        f"specialist.{NC}",
        file=sys.stderr,
    )
    print(
        f"{BLUE}(Type 'EOF' on a new line when you are finished){NC}", file=sys.stderr
    )
    guide_prompt_lines = [line for line in sys.stdin]
    guide_prompt = "".join(guide_prompt_lines).replace("EOF\n", "")

    if "specialists" not in existing_specialists:
        existing_specialists["specialists"] = {{}}

    existing_specialists["specialists"][specialist_id] = {
        {
            "description": description,
            "output_anchor": output_anchor,
            "guide_prompt": guide_prompt,
        }
    }

    print(f"\n{GREEN}INFO: Registering new specialist '{specialist_id}'...{NC}")
    with open(registry_file, "w") as f:
        yaml.dump(
            existing_specialists, f, indent=2, default_flow_style=False, sort_keys=False
        )

    print(
        f"\n{GREEN}✅ Successfully provisioned new Cognitive Specialist: "
        f"'{specialist_id}'.{NC}"
    )
    print(
        f"{BLUE}Nudge: This is an 'Assemblage' change. You MUST now follow the "
        f"change protocol to commit it.{NC}"
    )
    sys.exit(0)
