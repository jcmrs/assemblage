# Specification: `validate-assemblage` Utility in Python

This document specifies the design for `ITEM-003`: migrating the `validate-assemblage` utility to Python.

## 1. Objective

To create a Python script that performs a full integrity validation of the Assemblage, replacing the `validate-assemblage.sh` script. The script must check for uncommitted Git changes, version alignment between `ASSEMBLAGE.version` and `CHANGELOG.md`, and the validity of all file paths in configuration files.

## 2. Component Design

The utility will be a Python module located at `assemblage/tools/validate_assemblage.py`. It will be designed to be executable and to exit with a non-zero status code upon any validation failure.

### 2.1. Main Logic (`assemblage/tools/validate_assemblage.py`)

The script will be composed of distinct functions for each validation check.

1.  **Import necessary libraries:** `pathlib`, `subprocess`, `sys`, `re`, `pyyaml`.
2.  **`check_git_integrity()` function:**
    *   Defines the list of "Assemblage" paths to check (e.g., `config/`, `tools/`, `guides/`, etc.).
    *   Runs `git status --porcelain -- <paths>` using `subprocess.run()`.
    *   If the command's `stdout` is not empty, it means there are uncommitted changes. The function will print an error message and return `False`. Otherwise, it returns `True`.
3.  **`check_version_alignment()` function:**
    *   Reads the version from `ASSEMBLAGE.version` using `pathlib`.
    *   Reads the content of `CHANGELOG.md`.
    *   Uses a regular expression (`re.search()`) to find the latest version number in the changelog (e.g., `## [x.y.z]`).
    *   If the versions do not match, it prints an error and returns `False`. Otherwise, it returns `True`.
4.  **`check_wiring_integrity()` function:**
    *   Uses the `pyyaml` library to load `config/workbenches.yml` and `config/specialists.yml`.
    *   Recursively traverses the loaded data structures, looking for any string value that looks like a file path (`.md`, `.sh`, `.py`, `.yml`, etc.).
    *   For each path found, it uses `pathlib.Path(path).exists()` to verify the file or directory exists.
    *   Ignores paths that contain template variables (e.g., `{{...}}`).
    *   If any path does not exist, it prints an error and returns `False`. Otherwise, it returns `True`.
5.  **`main()` function:**
    *   Calls each validation function in sequence.
    *   A list of check functions will be used to make the main loop clean: `checks = [check_git_integrity, check_version_alignment, check_wiring_integrity]`.
    *   If any function returns `False`, the script will print a master failure message and exit with `sys.exit(1)`.
    *   If all functions return `True`, the script will print a master success message and exit with `sys.exit(0)`.
    *   The script will be made executable using the `if __name__ == "__main__":` block.

### 2.2. Test Design (`tests/tools/test_validate_assemblage.py`)

The Pytest test will be comprehensive, testing both success and failure modes for each check. This will require creating temporary files and directories to simulate different states of the Assemblage.

1.  **`test_git_integrity_success()`:** Mocks the `subprocess.run` call to return an empty `stdout`, asserting the check passes.
2.  **`test_git_integrity_failure()`:** Mocks `subprocess.run` to return a non-empty `stdout`, asserting the check fails.
3.  **`test_version_alignment_success(tmp_path)`:** Creates temporary `ASSEMBLAGE.version` and `CHANGELOG.md` files with matching versions in a temporary directory (`tmp_path` fixture), asserting the check passes.
4.  **`test_version_alignment_failure(tmp_path)`:** Creates temporary files with mismatched versions, asserting the check fails.
5.  **`test_wiring_integrity_success(tmp_path)`:** Creates a temporary config file and the corresponding dummy files it points to, asserting the check passes.
6.  **`test_wiring_integrity_failure(tmp_path)`:** Creates a temporary config file pointing to a non-existent file, asserting the check fails.
7.  **`test_main_exit_code()`:** Mocks the check functions to return `True` or `False` and asserts that the `main` function calls `sys.exit()` with the correct code (`0` for success, `1` for failure).

### 2.3. Decommissioning

Upon successful implementation and testing, the `tools/validate-assemblage.sh` script will be deleted.

This specification provides a complete plan for the Builder to execute.
