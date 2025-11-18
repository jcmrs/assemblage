# Specification: Control Plane `validate` Command

This document specifies the design for `ITEM-008`: integrating the `validate_assemblage` logic into the Control Plane as the `validate` command.

## 1. Objective

To refactor the existing `validate_assemblage.py` module into a library and expose its functionality through a new `validate` sub-command on the main `control_plane.py` module.

## 2. Component Design

### 2.1. Refactor `assemblage/tools/validate_assemblage.py`

The existing script will be converted into a library module.

1.  **Remove `if __name__ == "__main__"`:** The block that calls `main()` will be removed.
2.  **Rename `main()` to `validate()`:** The main function will be renamed to `validate()` to better reflect its purpose as a callable function.
3.  **Return Value:** The `validate()` function will no longer call `sys.exit()`. Instead, it will return `True` for success and `False` for failure. The responsibility for exiting the process now belongs to the Control Plane, which is the caller.

### 2.2. Update `assemblage/control_plane.py`

The Control Plane module will be extended to include the new command.

1.  **Import:** Import the newly refactored `validate` function from `assemblage.tools.validate_assemblage`.
2.  **Add Sub-command:** A new sub-parser for the `validate` command will be added to the `argparse` setup.
3.  **Create Handler Function:** A new handler function, `validate_command(args)`, will be created.
    *   This function will call `validate_assemblage.validate()`.
    *   It will check the boolean return value.
    *   It will print a success or failure message.
    *   It will call `sys.exit()` with the appropriate code (0 for success, 1 for failure).
4.  **Wire Handler:** The `validate` sub-parser will be wired to the `validate_command` handler function.

### 2.3. Update `tests/test_control_plane.py`

The test suite for the Control Plane will be updated to include tests for the new `validate` command.

1.  **`test_validate_command_success(monkeypatch)`:**
    *   Patches `validate_assemblage.validate` to always return `True`.
    *   Mocks `sys.argv` to `['control_plane.py', 'validate']`.
    *   Runs `control_plane.main()` and asserts that it exits with code 0.
    *   Asserts that the patched `validate` function was called.
2.  **`test_validate_command_failure(monkeypatch)`:**
    *   Patches `validate_assemblage.validate` to always return `False`.
    *   Mocks `sys.argv` to `['control_plane.py', 'validate']`.
    *   Runs `control_plane.main()` and asserts that it exits with code 1.

### 2.4. Decommissioning

Upon successful implementation and testing, the old standalone test file, `tests/tools/test_validate_assemblage.py`, will be deleted.

This specification provides a complete plan for the Builder to execute.
