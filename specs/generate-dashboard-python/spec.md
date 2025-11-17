# Specification: `generate-dashboard` Utility in Python

This document specifies the design for `ITEM-002`: migrating the `generate-dashboard` utility to Python.

## 1. Objective

To create a Python script that gathers status information about the Assemblage and project progress, and outputs it into `STATUS.md` and `status.json` files. This script will replace the original Bash script.

## 2. Component Design

The utility will be a Python module located at `assemblage/tools/generate_dashboard.py`. It will be executable as a module.

### 2.1. Main Logic (`assemblage/tools/generate_dashboard.py`)

The script will be structured with clear functions for each data-gathering step.

1.  **Import necessary libraries:** `pathlib`, `subprocess`, `datetime`, `json`.
2.  **Define constants:** `OUTPUT_MD = Path("STATUS.md")`, `OUTPUT_JSON = Path("status.json")`.
3.  **`get_assemblage_status()` function:**
    *   Runs `python -m assemblage.tools.validate_assemblage` using `subprocess.run()`.
    *   Checks the `returncode`. Returns a dictionary `{"status": "STABLE" or "UNSTABLE", "version": "x.y.z"}`.
    *   Reads `ASSEMBLAGE.version` using `pathlib`.
4.  **`get_conveyor_belt_metrics()` function:**
    *   Uses `pathlib` to count items in `ideas/`, `backlog/items/`, and `specs/`.
    *   Returns a dictionary of the counts.
5.  **`get_recent_activity()` function:**
    *   Runs `git log -n 5 --pretty=format:'%h|%s'` using `subprocess.run()`.
    *   Parses the output string into a list of dictionaries, each with "hash" and "message" keys.
6.  **`generate_json_output()` function:**
    *   Takes all the data dictionaries as arguments.
    *   Constructs a final dictionary representing the full JSON structure.
    *   Uses `json.dump()` to write the dictionary to `OUTPUT_JSON` with indentation for readability.
7.  **`generate_markdown_output()` function:**
    *   Takes all the data dictionaries as arguments.
    *   Uses an f-string or other templating method to build the Markdown report string.
    *   Writes the string to `OUTPUT_MD` using `Path.write_text()`.
8.  **`main()` function:**
    *   Orchestrates the calls to all the above functions in sequence.
    *   Includes print statements to log progress to the console.
    *   The script will be made executable using the `if __name__ == "__main__":` block.

### 2.2. Test Design (`tests/tools/test_generate_dashboard.py`)

The Pytest test will validate the script's behavior.

1.  **`test_script_runs_successfully()`:**
    *   Imports the `main` function from the script.
    *   Runs `main()`.
    *   Asserts that `OUTPUT_MD` and `OUTPUT_JSON` exist.
2.  **`test_json_output_is_valid()`:**
    *   Runs the script.
    *   Reads `OUTPUT_JSON` using `json.load()`.
    *   Asserts that the loaded data is a dictionary.
    *   Asserts that key fields exist (e.g., `assert "assemblage_health" in data`).
3.  **`test_markdown_output_contains_key_phrases()`:**
    *   Runs the script.
    *   Reads `OUTPUT_MD` using `Path.read_text()`.
    *   Asserts that the content contains expected substrings (e.g., "Assemblage Status Report", "Framework Version").
4.  **Setup/Teardown:** A Pytest fixture will be used to ensure the generated `STATUS.md` and `status.json` files are deleted after each test run to ensure test isolation.

### 2.3. Decommissioning

Upon successful implementation and testing, the following files will be deleted:
*   `tools/generate-dashboard.sh`
*   `tests/tools/generate-dashboard.bats`
*   `specs/dashboard-utility/` (the old spec)

This specification provides a complete plan for the Builder to execute.
