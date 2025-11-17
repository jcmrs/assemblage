# ITEM-003: Migrate 'validate-assemblage' Utility to Python

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Rewrite the `validate-assemblage.sh` utility as a Python script, including a new Pytest-based test. This is a critical utility for maintaining house integrity.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new Python module is created at `assemblage/tools/validate_assemblage.py`.
- [ ] The new module successfully performs all validation checks (Git status, version alignment, wiring integrity using `pyyaml`).
- [ ] The script exits with a non-zero exit code on failure.
- [ ] A new Pytest test file is created at `tests/tools/test_validate_assemblage.py` that validates both success and failure modes.
- [ ] The old `tools/validate-assemblage.sh` script is deleted.
- [ ] All tests, when run with `pytest`, pass successfully.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/validate-assemblage-python/spec.md`
