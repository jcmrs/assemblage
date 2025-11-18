# Specification: Documentation Audit and Update for Python Pivot

This document specifies the design for `ITEM-007`: auditing and updating all core documentation to reflect the architectural pivot to Python.

## 1. Objective

To rewrite and update all relevant guides, protocols, and configuration files to remove references to the old Bash/BATS framework and replace them with instructions and configurations relevant to the new Python/Pytest framework. This ensures the Assemblage's "manuals" are accurate and usable.

## 2. Component Design & Implementation Steps

This project involves modifying multiple Markdown and YAML files. The work is broken down by file.

### Step 1: Update `guides/SYSTEM/utility-test-protocol.md`

This guide is the most outdated. It will be completely rewritten.

1.  **Action:** Overwrite the file.
2.  **New Content:**
    *   The new protocol will mandate the use of `Pytest`.
    *   It will state that for every `assemblage/tools/my_script.py`, a corresponding `tests/tools/test_my_script.py` must be created.
    *   It will specify that the test suite is run by simply executing `pytest` in the terminal.
    *   It will remove all references to BATS and `.bats` files.

### Step 2: Update `guides/SYSTEM/assemblage-change-protocol.md`

This protocol needs significant updates to its "Run Utility Integrity Test" and "Run Lint Check" steps.

1.  **Action:** Use `replace` to modify specific sections.
2.  **Changes:**
    *   **Step 3 (Utility Integrity Test):** The command will be changed from `tools/run-assemblage-tests.sh` to `pytest`. The description will be updated to refer to Pytest and Python tests.
    *   **Step 5 (Lint Check):** The command will be changed from `tools/lint.sh` to `ruff check .` and `black --check .`.

### Step 3: Update `guides/SYSTEM/onboarding-protocol.md`

The practical exam for new AIs must be updated to reflect the Python environment.

1.  **Action:** Use `replace` to modify specific questions in the exam.
2.  **Changes:**
    *   **Question 4 (House Change Protocol):** The expected answer will now involve `pytest` and `ruff`/`black`.
    *   **Question 6 (Integrity Check):** The command will be changed from `tools/validate-assemblage.sh` to `python -m assemblage.tools.validate_assemblage`.
    *   The "Study the House" section will be updated to point to the new Python files and remove references to the old Bash scripts.

### Step 4: Update `config/workbenches.yml`

The `utilities` section of the `auditor` workbench needs to be updated.

1.  **Action:** Use `replace` to modify the `utilities` list.
2.  **Changes:**
    *   `tools/validate-assemblage.sh` will be changed to `assemblage.tools.validate_assemblage`.
    *   Any other migrated utilities listed will be similarly updated.

### Step 5: Decommission `tools/lint.sh`

The `lint.sh` script is now obsolete, as `ruff` and `black` are run directly.

1.  **Action:** Delete the file.
    *   **Command:** `git rm tools/lint.sh`

This specification provides a complete plan for the Builder to execute.
