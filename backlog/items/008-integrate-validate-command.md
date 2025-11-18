# ITEM-008: Integrate 'validate' command into Control Plane

**Date Created:** 2025-11-18
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Integrate the `validate_assemblage` logic as the `validate` sub-command in the central `assemblage/control_plane.py` module.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-007-control-plane-buildout.md`
* **Product Definition (The "What"):**
    * `product/control_plane_buildout.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `assemblage/control_plane.py` module is extended to accept a `validate` sub-command.
- [ ] The `validate` command handler imports and calls the main logic from the `assemblage/tools/validate_assemblage.py` module.
- [ ] The `assemblage/tools/validate_assemblage.py` module is refactored into a library (i.e., its `if __name__ == "__main__"` block is removed).
- [ ] Running `python -m assemblage.control_plane validate` executes the full integrity check.
- [ ] The Pytest test for the `validate` command is added to `tests/test_control_plane.py`.
- [ ] The old, standalone test file (`tests/tools/test_validate_assemblage.py`) is deleted.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/control-plane-validate/spec.md`
