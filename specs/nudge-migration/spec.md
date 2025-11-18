# Specification: `nudge` Utility in Python

This document specifies the design for `ITEM-006`: migrating the `nudge.sh` utility to Python.

## 1. Objective

To create a Python script that reads configuration files to act as a "firewall" for behavioral nudges, printing a specific nudge message if it is available for a given workbench, or an error if it is not. This script will replace `nudge.sh`.

## 2. Component Design

The utility will be a Python module located at `assemblage/tools/nudge.py`.

### 2.1. Main Logic (`assemblage/tools/nudge.py`)

The script will take two command-line arguments and use them to look up information in YAML configuration files.

1.  **Import necessary libraries:** `sys`, `pathlib`, `argparse`, `pyyaml`.
2.  **Define Constants:** `WORKBENCH_CONFIG = Path("config/workbenches.yml")`, `NUDGE_LIBRARY = Path("config/nudges.yml")`.
3.  **`main()` function:**
    *   Use Python's `argparse` library to define and parse two required positional arguments: `nudge_id` (string) and `current_workbench` (string). This provides robust argument handling and auto-generates help messages.
    *   Load the `workbenches.yml` and `nudges.yml` files using `pyyaml`. Handle potential `FileNotFoundError`.
    *   **Firewall Logic:**
        *   Access the list of `available_nudges` for the specified `current_workbench` from the loaded workbench data.
        *   Check if the provided `nudge_id` is present in that list.
        *   If the `nudge_id` is **not** in the list, print a formatted error message explaining that the nudge is not available for that workbench and exit with `sys.exit(1)`.
    *   **Nudge Delivery:**
        *   If the firewall check passes, access the nudge text from the loaded nudge library data using the `nudge_id`.
        *   If the `nudge_id` does not exist in the library, print an error and exit.
        *   If it exists, print the formatted nudge text to the console and exit with `sys.exit(0)`.
4.  The script will be made executable using the `if __name__ == "__main__":` block.

### 2.2. Test Design (`tests/tools/test_nudge.py`)

The Pytest test will validate all logic paths by creating temporary configuration files.

1.  **Setup Fixture (`temp_configs`):**
    *   A Pytest fixture will create a temporary directory containing dummy `workbenches.yml` and `nudges.yml` files.
    *   The `workbenches.yml` will define an `architect` workbench with an `available_nudges` list containing `holistic_check`.
    *   The `nudges.yml` will define the `holistic_check` nudge.
2.  **`test_successful_nudge(temp_configs)`:**
    *   Mocks `sys.argv` to simulate the command-line arguments `['nudge.py', 'holistic_check', 'architect']`.
    *   Runs the `main()` function.
    *   Asserts that the script prints the correct nudge text and exits with code 0.
3.  **`test_blocked_nudge(temp_configs)`:**
    *   Mocks `sys.argv` to simulate `['nudge.py', 'holistic_check', 'builder']` (where 'builder' does not have this nudge available).
    *   Runs `main()` and asserts that it prints the "firewall" error message and exits with code 1.
4.  **`test_non_existent_nudge(temp_configs)`:**
    *   Mocks `sys.argv` to simulate `['nudge.py', 'fake_nudge', 'architect']`.
    *   Runs `main()` and asserts that it prints a "nudge not found" error and exits with code 1.
5.  **`test_no_arguments()`:**
    *   Mocks `sys.argv` with only the script name.
    *   Runs `main()` and asserts that `argparse` causes an exit with a non-zero code (due to missing arguments).

### 2.3. Decommissioning

Upon successful implementation and testing, the `tools/nudge.sh` script will be deleted.

This specification provides a complete plan for the Builder to execute.
