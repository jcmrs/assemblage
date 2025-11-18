# Specification: Control Plane `create-specialist` Command

This document specifies the design for `ITEM-009`: integrating the `create_new_specialist` logic into the Control Plane as the `create_specialist` command.

## 1. Objective

To refactor the existing `create_new_specialist.py` module into a library and expose its interactive functionality through a new `create_specialist` sub-command on the main `control_plane.py` module.

## 2. Component Design

### 2.1. Refactor `assemblage/tools/create_new_specialist.py`

The existing script will be converted into a library module.

1.  **Remove `if __name__ == "__main__"`:** The block that calls `main()` will be removed.
2.  **Return Value:** The `main()` function will be modified to return `True` for success and `False` for failure, instead of calling `sys.exit()`. This allows the Control Plane to manage the process exit code.

### 2.2. Update `assemblage/control_plane.py`

The Control Plane module will be extended to include the new command.

1.  **Import:** Import the `main` function from `assemblage.tools.create_new_specialist` (it can be renamed to `create()` for clarity if desired).
2.  **Add Sub-command:** A new sub-parser for the `create_specialist` command will be added to the `argparse` setup.
3.  **Create Handler Function:** A new handler function, `create_specialist_command(args)`, will be created.
    *   This function will call the main logic from the `create_new_specialist` module.
    *   It will check the boolean return value and exit with the appropriate status code.

### 2.3. Update `tests/test_control_plane.py`

The test suite for the Control Plane will be updated to include a test for the new `create_specialist` command.

1.  **`test_create_specialist_command_success(monkeypatch)`:**
    *   Patches the `create_new_specialist.main` function to simulate a successful run (e.g., return `True`).
    *   Mocks `sys.argv` to `['control_plane.py', 'create_specialist']`.
    *   Runs `control_plane.main()` and asserts that it exits with code 0.
    *   Asserts that the patched `main` function was called.

### 2.4. Decommissioning

Upon successful implementation and testing, the old standalone test file, `tests/tools/test_create_new_specialist.py`, will be deleted.

This specification provides a complete plan for the Builder to execute.
