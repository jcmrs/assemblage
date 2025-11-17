"""
pre_commit_hook.py

This script contains the logic for the pre-commit hook. It runs the `ruff`
linter to ensure code quality before a commit is made.
"""

import subprocess
import sys

# --- ANSI Colors for Readability ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"  # No Color

def main():
    """
    Runs the ruff linter and exits with an appropriate status code.
    """
    print(f"{BLUE}INFO: Running 'ruff' linter...{NC}")
    
    command = ["ruff", "check", "."]
    
    try:
        # We stream the output directly to the console
        result = subprocess.run(command, check=False) 
        
        if result.returncode != 0:
            print(f"\n{RED}LINTING ERRORS FOUND.{NC}", file=sys.stderr)
            sys.exit(1)
            
        print(f"{GREEN}LINTING PASSED.{NC}")
        sys.exit(0)
        
    except FileNotFoundError:
        print(f"{RED}ERROR: 'ruff' command not found.{NC}", file=sys.stderr)
        print("Please ensure you have installed the project dependencies from requirements.txt", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

