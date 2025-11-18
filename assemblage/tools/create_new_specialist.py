"""
create_new_specialist.py

This utility interactively prompts the user to create a new Cognitive
Specialist and appends it to the specialists.yml configuration file.
"""

import sys
from pathlib import Path
import yaml

# --- Constants ---
REGISTRY_FILE = Path("config/specialists.yml")
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"

# --- Helper Functions ---
def _prompt_user(prompt_text):
    """Prints a prompt and returns sanitized user input."""
    print(f"\n{BLUE}[PROMPT] {prompt_text}{NC}", file=sys.stderr)
    return sys.stdin.readline().strip()

def main():
    """Main function to orchestrate the specialist creation process."""
    print(f"{GREEN}--- Starting 'create-new-specialist' Utility ---{NC}")

    # 1. Check if registry file exists
    if not REGISTRY_FILE.is_file():
        print(f"{RED}ERROR: Specialist Registry not found at '{REGISTRY_FILE}'!{NC}", file=sys.stderr)
        sys.exit(1)

    # 2. Get specialist ID and validate
    specialist_id = _prompt_user("Enter the unique ID for the new specialist (e.g., 'mcp_architect'):")
    if not specialist_id:
        print(f"{RED}ERROR: Specialist ID cannot be empty.{NC}", file=sys.stderr)
        sys.exit(1)

    with open(REGISTRY_FILE, "r") as f:
        existing_specialists = yaml.safe_load(f) or {}
    
    if specialist_id in existing_specialists.get("specialists", {}):
        print(f"{RED}ERROR: Specialist ID '{specialist_id}' already exists.{NC}", file=sys.stderr)
        sys.exit(1)

    # 3. Get other details
    description = _prompt_user(f"Enter the one-sentence description for '{specialist_id}':")
    output_anchor = _prompt_user("Enter the output_anchor path (e.g., 'knowledge/research/report.md'):")
    
    print(f"\n{BLUE}[PROMPT] Enter the multi-line 'guide_prompt' for this specialist.{NC}", file=sys.stderr)
    print(f"{BLUE}(Type 'EOF' on a new line when you are finished){NC}", file=sys.stderr)
    
    guide_prompt_lines = []
    while True:
        line = sys.stdin.readline()
        if line.strip() == 'EOF':
            break
        guide_prompt_lines.append(line)
    guide_prompt = "".join(guide_prompt_lines)

    # 4. Construct the new specialist data
    if "specialists" not in existing_specialists:
        existing_specialists["specialists"] = {}
    existing_specialists["specialists"][specialist_id] = {
        "description": description,
        "output_anchor": output_anchor,
        "guide_prompt": guide_prompt
    }

    # 5. Write the updated data back to the registry file
    print(f"\n{GREEN}INFO: Registering new specialist '{specialist_id}'...{NC}")
    with open(REGISTRY_FILE, "w") as f:
        yaml.dump(existing_specialists, f, indent=2, default_flow_style=False, sort_keys=False)

    print(f"\n{GREEN}✅ Successfully provisioned new Cognitive Specialist: '{specialist_id}'.{NC}")
    print(f"{BLUE}Nudge: This is an 'Assemblage' change. You MUST now follow the change protocol to commit it.{NC}")
    sys.exit(0)

if __name__ == "__main__":
    main()
