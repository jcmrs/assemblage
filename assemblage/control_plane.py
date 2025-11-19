"""
control_plane.py

This module is the central, abstract entry point for all agent-tool
interactions within the Assemblage. It is a single, consolidated source of
truth for all its capabilities.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from assemblage import code_search

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

# --- Private Logic for 'observe' command ---


def _get_assemblage_status():
    """Gets the current version."""
    print("INFO: Getting Assemblage version...")
    version_file = Path("ASSEMBLAGE.version")
    status = "✅ STABLE"
    status_json = "STABLE"
    version = version_file.read_text().strip()
    return {"status": status, "status_json": status_json, "version": version}


def _get_conveyor_belt_metrics():
    """Counts items in the ideas, backlog, and specs directories."""
    print("INFO: Gathering conveyor belt metrics...")
    ideas_count = len(list(Path("ideas").glob("*")))
    backlog_count = len(list(Path("backlog/items").glob("*")))
    specs_count = len(list(Path("specs").glob("*")))
    return {"ideas": ideas_count, "backlog": backlog_count, "specs": specs_count}


def _get_recent_activity(limit=5):
    """Gets the most recent Git log entries."""
    print("INFO: Fetching recent activity from Git...")
    command = ["git", "log", f"-n{limit}", "--pretty=format:%h|%s"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    log_entries = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        hash_val, message = line.split("|", 1)
        log_entries.append({"hash": hash_val, "message": message})
    return log_entries


def _generate_dashboard():
    """Main function to orchestrate the dashboard generation."""
    print("INFO: Starting dashboard generation...")
    output_md = Path("STATUS.md")
    output_json = Path("status.json")

    try:
        assemblage_health = _get_assemblage_status()
        conveyor_belt = _get_conveyor_belt_metrics()
        recent_activity = _get_recent_activity()

        final_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assemblage_health": assemblage_health,
            "project_progress": {
                "conveyor_belt": conveyor_belt,
                "recent_activity": recent_activity,
            },
        }

        print(f"INFO: Generating {output_json}...")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2)

        print(f"INFO: Generating {output_md}...")
        md_content = f"""# Assemblage Status Report

*Generated: {final_data['generated_at']}*

---

## 🏛️ Assemblage Health ("The House")

- **Integrity Status:** {final_data['assemblage_health']['status']}
- **Framework Version:** {final_data['assemblage_health']['version']}

---

## 🛋️ Project Progress ("The Furniture")

### "Conveyor Belt" Funnel
- **💡 Ideas:** {final_data['project_progress']['conveyor_belt']['ideas']}
- **📋 Backlog:** {final_data['project_progress']['conveyor_belt']['backlog']}
- **📐 Specs:** {final_data['project_progress']['conveyor_belt']['specs']}

### Recent Activity
"""
        for entry in final_data["project_progress"]["recent_activity"]:
            md_content += f"- `{entry['hash']}`: {entry['message']}\n"
        output_md.write_text(md_content, encoding="utf-8")

        print("INFO: Dashboard generation complete.")
        print(f"INFO: View the report: {output_md}")
        return True

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"ERROR: A required file or command failed: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return False


# --- Private Logic for 'validate' command ---


def _log_section(name):
    print(f"\n--- CHECK: {name} ---")


def _log_success(message):
    print(f"{GREEN}[PASS] {message}{NC}")


def _log_failure(message):
    print(f"{RED}[FAIL] {message}{NC}", file=sys.stderr)


def _check_git_integrity():
    _log_section("GIT-INTEGRITY")
    print("INFO: Checking for uncommitted changes...")
    paths_to_check = [
        "config/",
        "guides/",
        ".githooks/",
        "ASSEMBLAGE.version",
        "CHANGELOG.md",
        "FOUNDATION.md",
        "README.md",
        "GEMINI.md",
        "CLAUDE.md",
        "decisions/",
    ]
    cmd = ["git", "status", "--porcelain"] + paths_to_check
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        _log_failure("Git Integrity Check FAILED.")
        print("The following 'house' files are modified or untracked:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return False
    _log_success("Git Integrity Check PASSED.")
    return True


def _check_version_alignment():
    _log_section("VERSION-ALIGNMENT")
    print("INFO: Checking version alignment...")
    version_file = Path("ASSEMBLAGE.version")
    changelog_file = Path("CHANGELOG.md")
    if not version_file.is_file() or not changelog_file.is_file():
        _log_failure("Version file or changelog not found.")
        return False
    current_version = version_file.read_text().strip()
    changelog_content = changelog_file.read_text()
    match = re.search(r"##\s*\[(\d+\.\d+\.\d+)\]", changelog_content)
    if not match:
        _log_failure("Could not find any version in CHANGELOG.md.")
        return False
    latest_changelog_version = match.group(1)
    if current_version != latest_changelog_version:
        _log_failure("Version Alignment Check FAILED.")
        print(f"  '{version_file}' reports:   {current_version}", file=sys.stderr)
        print(
            f"  '{changelog_file}' reports: {latest_changelog_version}",
            file=sys.stderr,
        )
        return False
    _log_success(
        f"Version Alignment Check PASSED. Version '{current_version}' is aligned."
    )
    return True


def _find_paths_in_yaml(data):
    if isinstance(data, dict):
        for value in data.values():
            yield from _find_paths_in_yaml(value)
    elif isinstance(data, list):
        for item in data:
            yield from _find_paths_in_yaml(item)
    elif isinstance(data, str) and (
        ("." in data and "/" in data) or data.endswith((".md", ".sh", ".py", ".yml"))
    ):
        yield data


def _check_wiring_integrity():
    _log_section("WIRING-INTEGRITY")
    print("INFO: Checking for 'dead wires' in configuration...")
    all_paths_valid = True
    config_files_to_check = ["config/workbenches.yml", "config/specialists.yml"]
    for config_file in config_files_to_check:
        if not Path(config_file).is_file():
            _log_failure(f"Configuration file not found: {config_file}")
            all_paths_valid = False
            continue
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)
        for path in _find_paths_in_yaml(data):
            if "{{" in path:
                continue
            if not Path(path).exists():
                _log_failure(
                    f"DEAD WIRE DETECTED in '{config_file}': "
                    f"Path '{path}' does not exist."
                )
                all_paths_valid = False
    if all_paths_valid:
        _log_success("Wiring Integrity Check PASSED.")
    return all_paths_valid


def _validate_assemblage():
    """Runs all validation checks and returns True if all pass, otherwise False."""
    print(f"{BLUE}--- Running MASTER Assemblage Integrity Validation ---{NC}")
    checks = [_check_git_integrity, _check_version_alignment, _check_wiring_integrity]
    results = [check() for check in checks]
    print("\n---")
    if all(results):
        _log_success("✅ MASTER Assemblage Integrity Protocol PASSED.")
        return True
    else:
        _log_failure("❌ MASTER Assemblage Integrity Protocol FAILED.")
        return False


# --- Private Logic for 'create_specialist' command ---


def _prompt_user(prompt_text):
    """Prints a prompt and returns sanitized user input."""
    print(f"\n{BLUE}[PROMPT] {prompt_text}{NC}", file=sys.stderr)
    return sys.stdin.readline().strip()


def _create_new_specialist():
    """Main function to orchestrate the specialist creation process."""
    print(f"{GREEN}--- Starting create-new-specialist Utility ---{NC}")
    registry_file = Path("config/specialists.yml")
    if not registry_file.is_file():
        print(
            f"{RED}ERROR: Specialist Registry not found at '{registry_file}'!{NC}",
            file=sys.stderr,
        )
        return False
    specialist_id = _prompt_user(
        "Enter the unique ID for the new specialist (e.g., 'mcp_architect'):"
    )
    if not specialist_id:
        print(f"{RED}ERROR: Specialist ID cannot be empty.{NC}", file=sys.stderr)
        return False
    with open(registry_file, "r") as f:
        existing_specialists = yaml.safe_load(f) or {}
    if specialist_id in existing_specialists.get("specialists", {}):
        print(
            f"{RED}ERROR: Specialist ID '{specialist_id}' already exists.{NC}",
            file=sys.stderr,
        )
        return False
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
        existing_specialists["specialists"] = {}
    existing_specialists["specialists"][specialist_id] = {
        "description": description,
        "output_anchor": output_anchor,
        "guide_prompt": guide_prompt,
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
    return True


# --- Private Logic for 'nudge' command ---


def _deliver_nudge(nudge_id, current_workbench):
    """Checks firewall rules and delivers a nudge if available."""
    workbench_config = Path("config/workbenches.yml")
    nudge_library = Path("config/nudges.yml")
    try:
        with open(workbench_config, "r") as f:
            workbenches_data = yaml.safe_load(f)
        with open(nudge_library, "r") as f:
            nudges_data = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"{RED}ERROR: Configuration file not found: {e}{NC}", file=sys.stderr)
        return False
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
        return False
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
        return False
    nudge_text = nudges_data.get("nudges", {}).get(nudge_id)
    if not nudge_text:
        print(
            f"{RED}ERROR: Nudge ID '{nudge_id}' does not exist in the Nudge "
            f"Library.{NC}",
            file=sys.stderr,
        )
        return False
    print(f"\n{CYAN}💡 NUDGE ({nudge_id}):{NC}")
    print(f"{CYAN}---------------------------------{NC}")
    print(nudge_text)
    print(f"{CYAN}---------------------------------{NC}\n")
    return True


# --- Public Command Handlers ---


def observe_command(args):
    """Handler for the 'observe' command."""
    print("--- Control Plane: Executing 'observe' ---")
    if _generate_dashboard():
        sys.exit(0)
    else:
        sys.exit(1)


def validate_command(args):
    """Handler for the 'validate' command."""
    print("--- Control Plane: Executing 'validate' ---")
    if _validate_assemblage():
        sys.exit(0)
    else:
        sys.exit(1)


def create_specialist_command(args):
    """Handler for the 'create_specialist' command."""
    print("--- Control Plane: Launching 'create_specialist' ---")
    if _create_new_specialist():
        sys.exit(0)
    else:
        sys.exit(1)


def nudge_command(args):
    """Handler for the 'nudge' command."""
    print("--- Control Plane: Executing 'nudge' ---")
    if _deliver_nudge(args.nudge_id, args.current_workbench):
        sys.exit(0)
    else:
        sys.exit(1)


def index_command(args):
    """Handler for the 'index' command."""
    print("--- Control Plane: Executing 'index' ---")
    try:
        code_search.build_index()
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Indexing failed: {e}", file=sys.stderr)
        sys.exit(1)


def query_command(args):
    """Handler for the 'query' command."""
    print("--- Control Plane: Executing 'query' ---")
    try:
        results = code_search.search_index(args.query)
        # Format and print results as per ADR-009
        print(f'\n## Code Query Results for: "{args.query}"\n')
        if not results:
            print("No relevant code snippets found.")
            sys.exit(0)

        print(f"**Top {len(results)} Results:**\n")
        for i, res in enumerate(results):
            print("---")
            print(f"**{i+1}. File:** `{res['path']}`")
            print(f"**Lines:** {res['line']}")
            print(f"**Confidence Score:** {res['score']:.2f}\n")
            print(f"```python\n{res['content']}\n```")
        print("---\n")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Query failed: {e}", file=sys.stderr)
        sys.exit(1)


def status_command(args):
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


# --- Main Entry Point ---


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

    parser_observe = subparsers.add_parser(
        "observe",
        help="Observe the state of the Assemblage and generate a status dashboard.",
    )
    parser_observe.set_defaults(func=observe_command)

    parser_validate = subparsers.add_parser(
        "validate", help="Run a full integrity check of the Assemblage."
    )
    parser_validate.set_defaults(func=validate_command)

    parser_create_specialist = subparsers.add_parser(
        "create_specialist",
        help="Launch the interactive wizard to create a new Cognitive Specialist.",
    )
    parser_create_specialist.set_defaults(func=create_specialist_command)

    parser_nudge = subparsers.add_parser("nudge", help="Deliver a behavioral nudge.")
    parser_nudge.add_argument("nudge_id", help="The ID of the nudge to deliver.")
    parser_nudge.add_argument("current_workbench", help="The active workbench.")
    parser_nudge.set_defaults(func=nudge_command)

    # Code Query System commands
    parser_index = subparsers.add_parser(
        "index", help="Build the code intelligence index."
    )
    parser_index.set_defaults(func=index_command)

    parser_query = subparsers.add_parser(
        "query", help="Perform a semantic query on the codebase."
    )
    parser_query.add_argument("query", help="The natural language query string.")
    parser_query.set_defaults(func=query_command)

    parser_status = subparsers.add_parser(
        "status", help="Check the status of a system."
    )
    parser_status.add_argument(
        "--index", action="store_true", help="Check the status of the code index."
    )
    parser_status.set_defaults(func=status_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
