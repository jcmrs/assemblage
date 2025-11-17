# ITEM-004: Migrate Git Hooks to Python-based Tooling

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Migrate the logic within the `.githooks/pre-commit` script from Bash to a Python script, and configure the hook to run the Python-based linter (`ruff`).

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] The logic of the `pre-commit` hook is rewritten in a Python script located at `assemblage/tools/pre_commit_hook.py`.
- [ ] The new Python script correctly invokes the `ruff` linter on the appropriate files.
- [ ] The `.githooks/pre-commit` file is replaced with a minimal shell script that sets up the Python environment (if needed) and executes the `assemblage/tools/pre_commit_hook.py` script.
- [ ] The hook functions correctly, blocking commits when linting errors are present.
- [ ] A Pytest test is created to validate the logic of the `pre_commit_hook.py` script.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/githook-migration/spec.md`
