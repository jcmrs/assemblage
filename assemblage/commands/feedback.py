"""
assemblage.commands.feedback

Logic for the 'feedback' command.
"""

import re
import subprocess
import sys
from datetime import datetime, timezone

import yaml

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def _run_git_command(command):
    """Runs a Git command and returns its stdout."""
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, encoding="utf-8"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(
            f"{RED}ERROR: Git command failed: {' '.join(command)}{NC}", file=sys.stderr
        )
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def _generate_self_report(commit_hash):
    """Gathers objective data about the commit."""
    print(
        f"{YELLOW}--- Generating AI Self-Report for commit {commit_hash[:7]} ---" + NC
    )

    # 1. Validate Commit
    _run_git_command(["git", "cat-file", "-e", commit_hash])

    # 2. Get Commit Message & Task ID
    commit_message = _run_git_command(["git", "show", "-s", "--format=%B", commit_hash])
    task_id_match = re.search(r"(ITEM|ADR)-(\d+)", commit_message, re.IGNORECASE)
    task_id = task_id_match.group(0).upper() if task_id_match else "N/A"

    # 3. Get Commit Stats
    stat_output = _run_git_command(
        ["git", "show", "--shortstat", "--oneline", commit_hash]
    )
    stats_line = stat_output.split("\n")[-1]

    files_changed = re.search(r"(\d+) file", stats_line)
    insertions = re.search(r"(\d+) insertion", stats_line)
    deletions = re.search(r"(\d+) deletion", stats_line)

    # 4. Test Analysis
    files_output = _run_git_command(
        ["git", "show", "--name-only", "--oneline", commit_hash]
    )
    changed_files = files_output.split("\n")[1:]  # Skip the commit message line
    tests_impacted = sum(1 for file in changed_files if file.startswith("tests/"))

    report = {
        "commit_hash": commit_hash,
        "task_id": task_id,
        "files_changed": int(files_changed.group(1)) if files_changed else 0,
        "lines_added": int(insertions.group(1)) if insertions else 0,
        "lines_deleted": int(deletions.group(1)) if deletions else 0,
        "tests_impacted": tests_impacted,
        "self_correction_loops": "N/A",  # Per blueprint
    }
    return report


def _prompt_for_rating(prompt_text):
    """Prompts for a rating between 1 and 5."""
    while True:
        try:
            value = input(f"{BLUE}[PROMPT] {prompt_text} (1-5): {NC}")
            rating = int(value)
            if 1 <= rating <= 5:
                return rating
            else:
                print(f"{RED}Please enter a number between 1 and 5.{NC}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{NC}")


def _prompt_for_multiline(prompt_text):
    """Prompts for multi-line text input."""
    print(f"{BLUE}[PROMPT] {prompt_text} (type 'EOF' on a new line when done):{NC}")
    lines = []
    while True:
        try:
            line = input()
            if line == "EOF":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


def _prompt_vision_owner_review():
    """Interactively prompts the user for their subjective review."""
    print(f"\n{YELLOW}--- Vision Owner Review ---{NC}")
    review = {
        "clarity_rating": _prompt_for_rating("Clarity of the work and commit"),
        "efficiency_rating": _prompt_for_rating("Efficiency of the implementation"),
        "correctness_rating": _prompt_for_rating("Correctness and robustness"),
        "positive_notes": _prompt_for_multiline("Positive notes / what went well?"),
        "improvement_areas": _prompt_for_multiline("Areas for improvement?"),
    }
    return review


def _save_feedback(data):
    """Saves the feedback data to a timestamped YAML file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"feedback/{timestamp}.yml"

    print(f"\n{GREEN}INFO: Saving feedback to '{filename}'...{NC}")
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, indent=2, default_flow_style=False, sort_keys=False)
    return filename


def run(args):
    """Orchestrates the entire two-phase feedback process."""
    print(f"{GREEN}--- Initializing Structured Feedback Channel ---{NC}")

    # Phase 1: AI Self-Report
    self_report = _generate_self_report(args.commit)

    print("\n" + "=" * 40)
    print("AI SELF-REPORT:")
    for key, value in self_report.items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")
    print("=" * 40 + "\n")

    # Phase 2: Vision Owner Review
    vision_owner_review = _prompt_vision_owner_review()

    # Combine and Save
    final_payload = {
        "ai_self_report": self_report,
        "vision_owner_review": vision_owner_review,
    }

    filename = _save_feedback(final_payload)

    print(f"\n{GREEN}✅ Feedback successfully recorded in '{filename}'.{NC}")
    sys.exit(0)
