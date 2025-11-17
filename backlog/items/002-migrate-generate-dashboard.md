# ITEM-002: Migrate 'generate-dashboard' Utility to Python

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Rewrite the `generate-dashboard.sh` utility as a Python script, including a new Pytest-based test.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
    * `decisions/ADR-002-dashboard-mvp.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new Python module is created at `assemblage/tools/generate_dashboard.py`.
- [ ] The new module successfully performs all data gathering and generates `STATUS.md` and `status.json` as originally specified.
- [ ] A new Pytest test file is created at `tests/tools/test_generate_dashboard.py` that fully validates the script's functionality.
- [ ] The old `tools/generate-dashboard.sh` script is deleted.
- [ ] The old `tests/tools/generate-dashboard.bats` test is deleted.
- [ ] All tests, when run with `pytest`, pass successfully.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/generate-dashboard-python/spec.md`
