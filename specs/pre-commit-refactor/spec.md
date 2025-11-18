# Specification: Git Hook Refactor to `pre-commit` Framework

This document specifies the design for `ITEM-011`: refactoring our Git hook implementation to use the standard `pre-commit` Python framework.

## 1. Objective

To replace our custom hybrid hook with a declarative, Python-native solution. This will make our hook management simpler, more robust, and fully aligned with our new architecture.

## 2. Component Design & Implementation Steps

### Step 1: Update Dependencies

1.  **Action:** Add the `pre-commit` package to our `requirements.txt` file.

### Step 2: Create Declarative Configuration

A new configuration file will define our hooks.

1.  **Action:** Create a new file named `.pre-commit-config.yaml` in the project root.
2.  **File Content:** The file will be configured to use `ruff` and `black` to lint and format our Python code.
    ```yaml
    repos:
    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.6.0
        hooks:
        -   id: check-yaml
        -   id: end-of-file-fixer
        -   id: trailing-whitespace
    -   repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.5.0
        hooks:
        -   id: ruff
            args: [--fix]
        -   id: ruff-format
    ```

### Step 3: Decommission Old Hook Implementation

The old, custom hook files will be removed.

1.  **Action:** Delete the following files:
    *   `.githooks/pre-commit`
    *   `assemblage/tools/pre_commit_hook.py`
    *   `tests/tools/test_pre_commit_hook.py`

### Step 4: Update Documentation

The `README.md` must be updated with the new setup instructions for the `pre-commit` framework.

1.  **Action:** Modify the "Environment Setup" section of `README.md`.
2.  **New Instructions:** Add the command `pre-commit install` to the setup steps, explaining that this command installs the git hooks into the local `.git` directory.

### Step 5: Validation (Manual)

Because this change affects the commit process itself, the final validation will be a manual test.

1.  **Action:** After the new framework is in place, I will intentionally introduce a linting error into a Python file.
2.  I will then attempt to `git commit` that file.
3.  **Expected Result:** The commit should be blocked by the `pre-commit` hook, and `ruff` should report the error. This will prove the new system is working correctly.
4.  I will then revert the change to the file.

This specification provides a complete plan for the Builder to execute.
