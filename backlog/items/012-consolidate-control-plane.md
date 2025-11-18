# ITEM-012: Consolidate Tool Logic into Control Plane

**Date Created:** 2025-11-18
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Refactor the Control Plane by moving the logic from the individual modules in `assemblage/tools/` directly into the `assemblage/control_plane.py` module as private functions. This will simplify the project structure.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * This work is a direct result of the Gap Analysis performed after the main Python Pivot, aimed at simplifying our internal architecture.
* **Product Definition (The "What"):**
    * N/A

## 3. "What" (Acceptance Criteria)

- [ ] The logic from `dashboard_generator.py`, `validate_assemblage.py`, `create_new_specialist.py`, and `nudge.py` is moved into `control_plane.py`.
- [ ] The `assemblage/tools/` directory and its contents are deleted.
- [ ] All `import` statements are updated to reflect the new, consolidated structure.
- [ ] All existing Pytest tests for the Control Plane continue to pass after the refactoring.
- [ ] The `product/migration_status.md` is updated to reflect the completion of this consolidation.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/control-plane-consolidation/spec.md`
