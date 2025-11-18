# ITEM-002: Implement Control Plane 'observe' Command

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Implement the `observe` command for the new Assemblage Control Plane. This command will be the first capability of the Control Plane, responsible for generating the project status dashboard.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-006-control-plane-architecture.md`
    * `decisions/ADR-005-python-pivot.md`
    * `decisions/ADR-002-dashboard-mvp.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new central module is created at `assemblage/control_plane.py`.
- [ ] The `control_plane.py` module implements a command-line interface (using `argparse`) that accepts an `observe` sub-command.
- [ ] The logic for generating the `STATUS.md` and `status.json` files is implemented and called by the `observe` command.
- [ ] Running `python -m assemblage.control_plane observe` successfully generates the two dashboard files.
- [ ] A new Pytest test file is created at `tests/test_control_plane.py` that validates the `observe` command.
- [ ] The old `tools/generate-dashboard.sh` script is deleted.
- [ ] The old `tests/tools/generate-dashboard.bats` test is deleted.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/control-plane-observe/spec.md`
