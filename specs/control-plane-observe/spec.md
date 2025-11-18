# Specification: Control Plane `observe` Command

This document specifies the design for `ITEM-002`: implementing the `observe` command of the Assemblage Control Plane.

## 1. Objective

To create the initial `control_plane.py` module and implement its first sub-command, `observe`. This command will be responsible for gathering system status and generating the `STATUS.md` and `status.json` dashboard files.

## 2. Component Design

### 2.1. Control Plane Entry Point (`assemblage/control_plane.py`)

This new file will be the central entry point for all agent-tool interactions.

1.  **Imports:** `argparse`, `sys`.
2.  **Structure:** The script will use `argparse` with `subparsers` to create a command-line interface like `git` (e.g., `control_plane <command>`).
3.  **`main()` function:**
    *   It will define a main parser.
    *   It will create a subparser for commands.
    *   It will define the `observe` command parser.
    *   It will parse the arguments.
    *   Based on the parsed command, it will call the appropriate function (e.g., if `args.command == 'observe'`, call `observe_command()`).
4.  **`observe_command()` function:**
    *   This function will import the necessary logic from a refactored `dashboard_generator.py` module.
    *   It will call the main function of the dashboard generator to perform the actual work.
    *   It will handle the exit code and print success or failure messages.

### 2.2. Dashboard Generator Logic (`assemblage/tools/dashboard_generator.py`)

The logic previously designed for `generate_dashboard.py` will be placed here. This keeps the Control Plane clean and separates the orchestration logic from the implementation logic.

1.  **File Name:** The file will be renamed to `dashboard_generator.py` to reflect its role as a library module, not a direct-entry script.
2.  **Content:** The file will contain all the data-gathering and file-generation functions previously designed:
    *   `get_assemblage_status()`
    *   `get_conveyor_belt_metrics()`
    *   `get_recent_activity()`
    *   `generate_json_output()`
    *   `generate_markdown_output()`
    *   A main `generate()` function that orchestrates the calls.
3.  **No `if __name__ == "__main__"`:** This module is intended to be imported and used by the Control Plane, not run directly.

### 2.3. Test Design (`tests/test_control_plane.py`)

A new test file will be created to test the Control Plane's command-line interface.

1.  **`test_observe_command_success(monkeypatch)`:**
    *   Mocks `sys.argv` to `['control_plane.py', 'observe']`.
    *   Patches the `dashboard_generator.generate` function to simulate a successful run.
    *   Runs the `main()` function of `control_plane.py`.
    *   Asserts that the patched `generate` function was called.
    *   Asserts that the script exits with code 0.
2.  **`test_invalid_command(capsys)`:**
    *   Mocks `sys.argv` to `['control_plane.py', 'invalid_command']`.
    *   Runs `main()` and asserts that `argparse` prints a usage error and the script exits with a non-zero code.

### 2.4. Decommissioning

The following files from the previous, now-obsolete plan will be deleted:
*   `assemblage/tools/generate_dashboard.py`
*   `tests/tools/test_generate_dashboard.py`
*   `specs/generate-dashboard-python/`

This specification provides a complete plan for the Builder to execute.
