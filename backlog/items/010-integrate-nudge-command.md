# ITEM-010: Integrate 'nudge' command into Control Plane

**Date Created:** 2025-11-18
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Integrate the `nudge` logic as the `nudge` sub-command in the central `assemblage/control_plane.py` module.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-007-control-plane-buildout.md`
* **Product Definition (The "What"):**
    * `product/control_plane_buildout.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `assemblage/control_plane.py` module is extended to accept a `nudge` sub-command with its required arguments (`nudge_id`, `current_workbench`).
- [ ] The `nudge` command handler imports and calls the main logic from the `assemblage/tools/nudge.py` module.
- [ ] The `assemblage/tools/nudge.py` module is refactored into a library.
- [ ] Running `python -m assemblage.control_plane nudge <id> <workbench>` executes the nudge logic.
- [ ] The Pytest test for the `nudge` command is added to `tests/test_control_plane.py`.
- [ ] The old, standalone test file (`tests/tools/test_nudge.py`) is deleted.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/control-plane-nudge/spec.md`
