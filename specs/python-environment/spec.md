# Specification: Python Project Environment Setup

This document specifies the design for `ITEM-001` from the backlog: establishing the foundational Python environment for the Assemblage.

## 1. Objective

To create the necessary directory structure, configuration files, and dependency lists to support a Python-based automation toolchain, and to decommission the old BATS framework.

## 2. Component Design & Implementation Steps

### Step 1: Decommission BATS Framework

The first action will be to remove the now-obsolete BATS testing framework.

1.  **Remove Submodules:** The `tests/libs` directory and its contents (`bats-core`, `bats-support`, `bats-assert`) will be properly removed as Git submodules.
    *   **Command:** `git submodule deinit -f tests/libs/bats-core`
    *   **Command:** `git submodule deinit -f tests/libs/bats-support`
    *   **Command:** `git submodule deinit -f tests/libs/bats-assert`
    *   **Command:** `git rm -f tests/libs/bats-core`
    *   **Command:** `git rm -f tests/libs/bats-support`
    *   **Command:** `git rm -f tests/libs/bats-assert`
    *   **Command:** `rm -rf .git/modules/tests/libs`
2.  **Update `.gitmodules`:** The `.gitmodules` file should be an empty file after the deinit process. This file will be removed from git.
    *   **Command:** `git rm .gitmodules`
3.  **Remove old test runner:** The `tests/run-tests.sh` script will be deleted.
    *   **Command:** `rm tests/run-tests.sh`

### Step 2: Create Python Directory Structure

A standard Python project structure will be created.

1.  **Create Source Directory:**
    *   **Command:** `mkdir assemblage`
2.  **Create `__init__.py`:** This file makes `assemblage` a package.
    *   **Command:** `touch assemblage/__init__.py`

### Step 3: Create Configuration Files

The project will be configured via `requirements.txt` and `pyproject.toml`.

1.  **Create `requirements.txt`:** This file will list our direct dependencies.
    *   **File Content:**
        ```
        # Core Dependencies
        pyyaml

        # Testing Dependencies
        pytest
        
        # Code Quality
        black
        ruff
        ```
2.  **Create `pyproject.toml`:** This file will configure our development tools.
    *   **File Content:**
        ```toml
        [tool.black]
        line-length = 88

        [tool.ruff]
        line-length = 88
        select = ["E", "F", "W", "I"] # Standard flake8 rules + isort
        ```

### Step 4: Update `.gitignore`

The `.gitignore` file must be updated to exclude Python-specific artifacts.

1.  **Append to `.gitignore`:** The following lines will be added to the existing `.gitignore` file.
    *   `.venv/`
    *   `__pycache__/`
    *   `*.pyc`

### Step 5: Update Documentation

The main `README.md` must be updated to reflect the new setup procedure.

1.  **Modify `README.md`:** The "Getting Started" section will be updated to include instructions for setting up a Python virtual environment and installing the dependencies from `requirements.txt`.
    *   **Example Text:** "This project uses Python for its automation scripts. To set up your local environment, create a virtual environment and install the required packages: `python -m venv .venv`, `source .venv/bin/activate` (or `\.venv\Scripts\activate` on Windows), and `pip install -r requirements.txt`."

This specification provides a complete plan for the Builder to execute.
