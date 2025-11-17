# Specification: Git Hook Migration to Python

This document specifies the design for `ITEM-004`: migrating the `pre-commit` Git hook to use our new Python-based toolchain.

## 1. Objective

To replace the existing Bash-based `pre-commit` hook with a new implementation that uses a Python script to run our chosen linter (`ruff`). This ensures that our code quality checks are aligned with our new Python-centric architecture.

## 2. Component Design

The solution will consist of two parts: a Python script to contain the linting logic, and a minimal wrapper in the `.githooks/pre-commit` file to execute it.

### 2.1. Python Hook Logic (`assemblage/tools/pre_commit_hook.py`)

A new Python script will be created to encapsulate the hook's logic. This makes it testable and keeps the hook file itself simple.

1.  **Import necessary libraries:** `subprocess`, `sys`.
2.  **`main()` function:**
    *   The function will run the `ruff` linter on the entire project.
    *   **Command:** `ruff check .`
    *   It will use `subprocess.run()`, checking the `returncode`.
    *   If `ruff` returns a non-zero exit code (indicating linting errors), the script will print an informative error message and exit with `sys.exit(1)`.
    *   If `ruff` succeeds (exit code 0), the script will print a success message and exit with `sys.exit(0)`.
3.  The script will be made executable using the `if __name__ == "__main__":` block.

### 2.2. The Hook File (`.githooks/pre-commit`)

The existing `pre-commit` file will be completely replaced with a new, minimal script. This script's only job is to execute the Python script. This avoids putting complex logic inside the hook file itself.

*   **File Content:**
    ```bash
    #!/bin/sh
    #
    # This hook executes the Python-based pre-commit logic.

    echo "--- Running Assemblage Pre-Commit Hook ---"

    # Ensure we are using the project's virtual environment if it exists
    if [ -d ".venv" ]; then
        # This works for both Windows (Git Bash) and Linux/macOS
        source .venv/bin/activate
    fi

    # Execute the Python script
    python -m assemblage.tools.pre_commit_hook

    # Capture the exit code from the Python script
    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "--- Pre-Commit Check FAILED. Aborting commit. ---" >&2
        exit 1
    else
        echo "--- Pre-Commit Check PASSED. ---"
    fi

    exit 0
    ```
*   **Permissions:** The file must be made executable.

### 2.3. Test Design (`tests/tools/test_pre_commit_hook.py`)

A Pytest test will be created to validate the hook's logic.

1.  **`test_hook_success_on_clean_code()`:**
    *   Mocks `subprocess.run` to simulate `ruff` running successfully (return code 0).
    *   Calls the `main()` function of the Python hook script.
    *   Asserts that the script exits with `sys.exit(0)`.
2.  **`test_hook_failure_on_lint_errors()`:**
    *   Mocks `subprocess.run` to simulate `ruff` finding errors (return code 1).
    *   Calls the `main()` function.
    *   Asserts that the script exits with `sys.exit(1)`.

### 2.4. Decommissioning

The old `.githooks/pre-commit` file will be overwritten as part of this process. No other files are to be deleted.

This specification provides a complete plan for the Builder to execute.
