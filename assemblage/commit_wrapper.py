"""
commit_wrapper.py

A wrapper around 'git commit' that implements a one-retry self-correction
loop for pre-commit hooks that modify files.
"""

import argparse
import subprocess
import sys

# --- ANSI Colors for Readability ---
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def run_command(command):
    """Runs a command and returns the result."""
    return subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def main():
    """
    Main entry point for the commit wrapper.
    """
    parser = argparse.ArgumentParser(
        description="A wrapper for git commit with a self-correction loop."
    )
    parser.add_argument("-m", "--message", required=True, help="Commit message")
    args = parser.parse_args()

    commit_command = ["git", "commit", "-m", args.message]

    # --- First Attempt ---
    print(f"{YELLOW}--- Attempting commit... ---{NC}")
    result = run_command(commit_command)

    if result.returncode == 0:
        print(f"{GREEN}✅ Commit successful on the first attempt.{NC}")
        print(result.stdout)
        sys.exit(0)

    # --- First Attempt Failed: Analyze and Potentially Retry ---
    print(f"{RED}--- Initial commit failed. Analyzing output... ---{NC}")

    combined_output = result.stdout + result.stderr
    if "- files were modified by this hook" in combined_output:
        print(
            f"{YELLOW}--- Fixable error detected. "
            f"Staging fixes and re-trying... ---{NC}"
        )

        # --- Second Attempt ---
        run_command(["git", "add", "-u"])

        print(f"{YELLOW}--- Re-attempting commit... ---{NC}")
        second_result = run_command(commit_command)

        if second_result.returncode == 0:
            print(f"{GREEN}✅ Self-correction successful! Commit has passed.{NC}")
            print(second_result.stdout)
            sys.exit(0)
        else:
            print(
                f"{RED}❌ Self-correction failed. The commit still fails after "
                f"fixes.{NC}"
            )
            print(second_result.stdout, file=sys.stderr)
            print(second_result.stderr, file=sys.stderr)
            sys.exit(1)
    else:
        print(
            f"{RED}❌ Unfixable error detected. No self-correction will be "
            f"attempted.{NC}"
        )
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
