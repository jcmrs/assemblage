# ITEM-003: Implement Control Plane 'validate' Command

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Implement the `validate` command for the Assemblage Control Plane. This command will run a full integrity check of the Assemblage.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-006-control-plane-architecture.md`
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `assemblage/control_plane.py` module is extended to accept a `validate` sub-command.
- [ ] The logic for validating the assemblage is implemented in `assemblage/tools/validate_assemblage.py` and called by the `validate` command.
- [ ] Running `python -m assemblage.control_plane validate` successfully runs the integrity checks and exits with the correct status code.
- [ ] The Pytest test for the `validate` command is added to `tests/test_control_plane.py`.
- [ ] The old `tools/validate-assemblage.sh` script is deleted.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/control-plane-validate/spec.md`
