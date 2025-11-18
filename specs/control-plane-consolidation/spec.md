# Specification: Control Plane Consolidation

This document specifies the design for `ITEM-012`: consolidating all tool logic into the central `control_plane.py` module.

## 1. Objective

To simplify the project's architecture by eliminating the `assemblage/tools/` directory and moving all its logic directly into `control_plane.py`. This will make the Control Plane a true single-file source of truth for its capabilities.

## 2. Component Design & Implementation Steps

### Step 1: Consolidate Logic into `control_plane.py`

1.  **Action:** All logic from the following files will be moved into `control_plane.py`:
    *   `assemblage/tools/dashboard_generator.py`
    *   `assemblage/tools/validate_assemblage.py`
    *   `assemblage/tools/create_new_specialist.py`
    *   `assemblage/tools/nudge.py`
2.  **Implementation:**
    *   The functions from these modules will be redefined as private functions within `control_plane.py` (e.g., `_generate_dashboard()`, `_validate_assemblage()`).
    *   All necessary imports (`yaml`, `subprocess`, `re`, `pathlib`) will be consolidated at the top of `control_plane.py`.
    *   The public-facing command handlers (`observe_command`, `validate_command`, etc.) will be updated to call these new internal private functions.

### Step 2: Decommission `assemblage/tools/`

Once the logic is moved, the now-empty `tools` directory will be removed.

1.  **Action:** Delete the entire `assemblage/tools/` directory.

### Step 3: Update Test Implementation

The tests must be updated to reflect the new internal structure of the Control Plane.

1.  **Action:** Modify `tests/test_control_plane.py`.
2.  **Implementation:** All `monkeypatch.setattr` calls that currently target the external modules (e.g., `control_plane.validate_assemblage`) will be updated to target the new private functions within the `control_plane` module itself (e.g., `control_plane._validate_assemblage`).

### Step 4: Validation

1.  **Action:** Run the full test suite for the Control Plane.
2.  **Expected Result:** All tests in `tests/test_control_plane.py` must pass, proving that the refactoring did not change the external behavior of the Control Plane.

This specification provides a complete plan for the Builder to execute.
