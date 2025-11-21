"""
assemblage.commands.validate

Logic for the 'validate' command.
"""

import re
import subprocess
import sys
from pathlib import Path

import yaml

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"


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


def run(args):
    """Runs all validation checks and returns True if all pass, otherwise False."""
    print(f"{BLUE}--- Running MASTER Assemblage Integrity Validation ---{NC}")
    checks = [_check_git_integrity, _check_version_alignment, _check_wiring_integrity]
    results = [check() for check in checks]
    print("\n---")
    if all(results):
        _log_success("✅ MASTER Assemblage Integrity Protocol PASSED.")
        sys.exit(0)
    else:
        _log_failure("❌ MASTER Assemblage Integrity Protocol FAILED.")
        sys.exit(1)
