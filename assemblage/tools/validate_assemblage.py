"""
validate_assemblage.py

Performs a full integrity validation of the Assemblage, replacing the
original Bash script.
"""

import re
import subprocess
import sys
from pathlib import Path

import yaml

# --- Configuration ---
ASSEMBLAGE_PATHS_TO_CHECK = [
    "config/",
    "guides/",
    "tools/",
    ".githooks/",
    "ASSEMBLAGE.version",
    "CHANGELOG.md",
    "FOUNDATION.md",
    "README.md",
    "GEMINI.md",
    "CLAUDE.md",
    "decisions/",
]
VERSION_FILE = Path("ASSEMBLAGE.version")
CHANGELOG_FILE = Path("CHANGELOG.md")
CONFIG_FILES_TO_CHECK = ["config/workbenches.yml", "config/specialists.yml"]

# --- ANSI Colors for Readability ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"  # No Color

# --- Helper Functions ---
def _log_section(name):
    print(f"\n--- CHECK: {name} ---")

def _log_success(message):
    print(f"{GREEN}[PASS] {message}{NC}")

def _log_failure(message):
    print(f"{RED}[FAIL] {message}{NC}", file=sys.stderr)

# --- Validation Checks ---

def check_git_integrity():
    """Checks for uncommitted changes in core Assemblage files."""
    _log_section("GIT-INTEGRITY")
    print("INFO: Checking for uncommitted changes in Assemblage files...")
    
    cmd = ["git", "status", "--porcelain"] + ASSEMBLAGE_PATHS_TO_CHECK
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        _log_failure("Git Integrity Check FAILED.")
        print("The following 'house' files are modified or untracked:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return False
    
    _log_success("Git Integrity Check PASSED.")
    return True

def check_version_alignment():
    """Checks if ASSEMBLAGE.version matches the latest in CHANGELOG.md."""
    _log_section("VERSION-ALIGNMENT")
    print("INFO: Checking version alignment...")

    if not VERSION_FILE.is_file() or not CHANGELOG_FILE.is_file():
        _log_failure("Version file or changelog not found.")
        return False

    current_version = VERSION_FILE.read_text().strip()
    changelog_content = CHANGELOG_FILE.read_text()
    
    # Regex to find the first version like ## [1.2.3]
    match = re.search(r"##\s*\[(\d+\.\d+\.\d+)\]", changelog_content)
    
    if not match:
        _log_failure("Could not find any version in CHANGELOG.md.")
        return False
        
    latest_changelog_version = match.group(1)

    if current_version != latest_changelog_version:
        _log_failure("Version Alignment Check FAILED.")
        print(f"  '{VERSION_FILE}' reports:   {current_version}", file=sys.stderr)
        print(f"  '{CHANGELOG_FILE}' reports: {latest_changelog_version}", file=sys.stderr)
        return False

    _log_success(f"Version Alignment Check PASSED. Version '{current_version}' is aligned.")
    return True

def check_wiring_integrity():
    """Checks config files for 'dead wires' (paths that don't exist)."""
    _log_section("WIRING-INTEGRITY")
    print("INFO: Checking for 'dead wires' in configuration...")
    
    all_paths_valid = True
    
    for config_file in CONFIG_FILES_TO_CHECK:
        if not Path(config_file).is_file():
            _log_failure(f"Configuration file not found: {config_file}")
            all_paths_valid = False
            continue
            
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)
        
        for path in _find_paths_in_yaml(data):
            if "{{" in path:  # Ignore template strings
                continue
            if not Path(path).exists():
                _log_failure(f"DEAD WIRE DETECTED in '{config_file}': Path '{path}' does not exist.")
                all_paths_valid = False

    if all_paths_valid:
        _log_success("Wiring Integrity Check PASSED.")
    return all_paths_valid

def _find_paths_in_yaml(data):
    """Recursively find all string values in a YAML data structure."""
    if isinstance(data, dict):
        for value in data.values():
            yield from _find_paths_in_yaml(value)
    elif isinstance(data, list):
        for item in data:
            yield from _find_paths_in_yaml(item)
    elif isinstance(data, str):
        # A simple heuristic to identify strings that are likely file paths
        if "." in data and "/" in data or data.endswith((".md", ".sh", ".py", ".yml")):
            yield data

# --- Main Orchestrator ---

def main():
    """
    Runs all validation checks and exits with an appropriate status code.
    """
    print(f"{BLUE}--- Running MASTER Assemblage Integrity Validation (Python) ---")
    
    checks = [
        check_git_integrity,
        check_version_alignment,
        check_wiring_integrity,
    ]
    
    results = [check() for check in checks]
    
    print("\n---")
    if all(results):
        _log_success("✅ MASTER Assemblage Integrity Protocol PASSED.")
        sys.exit(0)
    else:
        _log_failure("❌ MASTER Assemblage Integrity Protocol FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
