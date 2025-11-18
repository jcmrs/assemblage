# ITEM-009: Integrate 'create-specialist' command into Control Plane

**Date Created:** 2025-11-18
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Integrate the `create_new_specialist` logic as the `create_specialist` sub-command in the central `assemblage/control_plane.py` module.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-007-control-plane-buildout.md`
* **Product Definition (The "What"):**
    * `product/control_plane_buildout.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `assemblage/control_plane.py` module is extended to accept a `create_specialist` sub-command.
- [ ] The `create_specialist` command handler imports and calls the main logic from the `assemblage/tools/create_new_specialist.py` module.
- [ ] The `assemblage/tools/create_new_specialist.py` module is refactored into a library.
- [ ] Running `python -m assemblage.control_plane create_specialist` launches the interactive wizard.
- [ ] The Pytest test for the `create_specialist` command is added to `tests/test_control_plane.py`.
- [ ] The old, standalone test file (`tests/tools/test_create_new_specialist.py`) is deleted.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/control-plane-create-specialist/spec.md`
