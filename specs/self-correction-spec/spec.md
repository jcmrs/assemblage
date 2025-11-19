# Specification: Self-Correction Loop

This document specifies the design for `ITEM-014`: implementing a safe, one-retry-only self-correction loop for the `git commit` process.

## 1. Objective

To create a Python-based wrapper around `git commit` that can intelligently handle fixable `pre-commit` hook failures, thereby increasing automation and reducing friction, while adhering to strict safety principles.

## 2. Component Design

### 2.1. Commit Wrapper Script (`assemblage/commit_wrapper.py`)

A new, standalone script will be created to orchestrate the commit process.

1.  **Interface:** The script will accept a commit message via the `-m` flag, mimicking `git commit`. It will use Python's `argparse` for this.
2.  **Core Logic:**
    *   The script will execute `git commit` using `subprocess.run`, capturing `stdout`, `stderr`, and the `returncode`.
    *   **Success Path:** If the initial commit succeeds (`returncode == 0`), the script will print a success message and exit 0.
    *   **Failure Path:** If the commit fails (`returncode != 0`), the script will analyze the captured `stdout` and `stderr`.
        *   **Trigger Condition:** The self-correction logic will *only* trigger if the combined output contains the string `- files were modified by this hook`.
        *   **Unfixable Failure:** If the trigger condition is not met, the script will print the error from the failed commit and exit 1.
        *   **Fixable Failure (Self-Correction):**
            1.  Print a clear log message indicating a fix was detected and a re-commit is being attempted.
            2.  Execute `git add -u` to stage only the modifications made by the hook to already-tracked files. This is safer than `git add .`.
            3.  Re-execute the original `git commit` command.
            4.  If this second attempt succeeds, print a success message and exit 0.
            5.  If the second attempt fails, print the new error message and exit 1. **The script will not attempt any further retries.**

### 2.2. Test Design (`tests/test_commit_wrapper.py`)

A new test file will be created to validate the wrapper's logic using mocked subprocess calls.

1.  **`test_success_on_first_try`:** Mocks `subprocess.run` to return `returncode=0` on the first call. Asserts the script exits 0 and `subprocess` was called only once.
2.  **`test_successful_self_correction`:**
    *   Mocks `subprocess.run` to simulate the full success path:
        1.  `git commit` -> fails with `returncode=1` and the trigger string in `stdout`.
        2.  `git add -u` -> succeeds.
        3.  `git commit` -> succeeds with `returncode=0`.
    *   Asserts the script exits 0 and that `subprocess.run` was called three times with the correct arguments.
3.  **`test_failure_on_unfixable_error`:** Mocks `subprocess.run` to fail *without* the trigger string. Asserts the script exits 1 and `subprocess.run` was called only once.
4.  **`test_failure_on_second_attempt`:** Mocks `subprocess.run` to simulate a failure even after a successful `git add -u`. Asserts the script exits 1 and does not attempt a third commit.

### 2.3. Documentation

The `README.md` or a new developer guide will be updated to instruct users to use `python -m assemblage.commit_wrapper -m "..."` for commits going forward.

This specification provides a complete and safe plan for the Builder to execute.
