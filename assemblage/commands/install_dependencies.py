"""
assemblage.commands.install_dependencies

Logic for the 'install_dependencies' command.
"""

import subprocess
import sys

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"


def run(args):
    """
    Installs dependencies from requirements.txt using the current Python
    interpreter's pip.
    """
    print(f"\n{BLUE}--- Installing/Updating Dependencies ---{NC}")
    print(f"Using Python interpreter: {sys.executable}")

    try:
        # Define the command
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

        # Execute the command, streaming output live
        result = subprocess.run(
            cmd,
            check=False,  # We handle the error manually
            text=True,
            # Let stdout/stderr flow to the parent process
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        if result.returncode == 0:
            print(f"\n{GREEN}--- Dependencies are up to date. ---{NC}")
            sys.exit(0)
        else:
            print(
                f"\n{RED}--- Dependency installation failed with exit code "
                f"{result.returncode}. ---{NC}"
            )
            sys.exit(1)

    except FileNotFoundError:
        print(
            f"\n{RED}--- ERROR: 'requirements.txt' not found in the current "
            "directory. ---{NC}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}--- An unexpected error occurred: {e} ---{NC}")
        sys.exit(1)
