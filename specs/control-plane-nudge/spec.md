# Specification: Control Plane `nudge` Command

This document specifies the design for `ITEM-010`: integrating the `nudge` logic into the Control Plane as the `nudge` command.

## 1. Objective

To refactor the existing `nudge.py` module into a library and expose its functionality through a new `nudge` sub-command on the main `control_plane.py` module.

## 2. Component Design

### 2.1. Refactor `assemblage/tools/nudge.py`

The existing script will be converted into a library module.

1.  **Remove `if __name__ == "__main__"`:** The block that calls `main()` will be removed.
2.  **Parameter Passing:** The `main()` function will be modified to accept the `nudge_id` and `current_workbench` as direct arguments, instead of parsing them from `sys.argv`.
3.  **Return Value:** The function will be modified to return `True` for success and `False` for failure, instead of calling `sys.exit()`.

### 2.2. Update `assemblage/control_plane.py`

The Control Plane module will be extended to include the new command.

1.  **Import:** Import the `main` function from `assemblage.tools.nudge` (renamed to `deliver_nudge()` for clarity).
2.  **Add Sub-command:** A new sub-parser for the `nudge` command will be added. It will be configured to accept two positional arguments: `nudge_id` and `current_workbench`.
3.  **Create Handler Function:** A new handler function, `nudge_command(args)`, will be created.
    *   This function will call `nudge.deliver_nudge(args.nudge_id, args.current_workbench)`.
    *   It will check the boolean return value and exit with the appropriate status code.

### 2.3. Update `tests/test_control_plane.py`

The test suite for the Control Plane will be updated to include tests for the new `nudge` command.

1.  **`test_nudge_command_success(monkeypatch)`:**
    *   Patches `nudge.deliver_nudge` to simulate a successful run (return `True`).
    *   Mocks `sys.argv` to `['control_plane.py', 'nudge', 'holistic_check', 'architect']`.
    *   Runs `control_plane.main()` and asserts that it exits with code 0.
    *   Asserts that the patched `deliver_nudge` function was called with the correct arguments.
2.  **`test_nudge_command_failure(monkeypatch)`:**
    *   Patches `nudge.deliver_nudge` to simulate a failure (return `False`).
    *   Mocks `sys.argv` to `['control_plane.py', 'nudge', 'holistic_check', 'builder']`.
    *   Runs `control_plane.main()` and asserts that it exits with code 1.

### 2.4. Decommissioning

Upon successful implementation and testing, the old standalone test file, `tests/tools/test_nudge.py`, will be deleted.

This specification provides a complete plan for the Builder to execute.
