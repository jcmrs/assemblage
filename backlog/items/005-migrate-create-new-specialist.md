# ITEM-005: Migrate 'create-new-specialist' Utility to Python

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Rewrite the interactive `create-new-specialist.sh` utility as a Python script.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new Python module is created at `assemblage/tools/create_new_specialist.py`.
- [ ] The new module replicates the interactive prompts of the original script using Python's `input()` function.
- [ ] The script correctly appends the new specialist definition to the `config/specialists.yml` file using the `pyyaml` library.
- [ ] A new Pytest test file is created to validate the script's logic, likely using mocking to simulate user input and file system interaction.
- [ ] The old `tools/create-new-specialist.sh` script is deleted.
- [ ] All tests, when run with `pytest`, pass successfully.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/create-new-specialist-python/spec.md`
