# ITEM-006: Migrate 'nudge' Utility to Python

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Rewrite the `nudge.sh` utility, which acts as a "firewall" and delivers behavioral microprompts, as a Python script.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new Python module is created at `assemblage/tools/nudge.py`.
- [ ] The script accepts two command-line arguments (`nudge_id` and `current_workbench`) using Python's `argparse` or `sys.argv`.
- [ ] The script uses the `pyyaml` library to parse `config/workbenches.yml` and `config/nudges.yml`.
- [ ] The script correctly implements the "firewall" logic, checking if the nudge is available for the given workbench.
- [ ] The script prints the correct nudge text or error message to the console.
- [ ] A new Pytest test file is created to validate all logic paths (successful nudge, blocked nudge, non-existent nudge).
- [ ] The old `tools/nudge.sh` script is deleted.
- [ ] All tests, when run with `pytest`, pass successfully.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/nudge-migration/spec.md`
