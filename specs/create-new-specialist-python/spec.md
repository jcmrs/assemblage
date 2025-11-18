# Specification: `create-new-specialist` Utility in Python

This document specifies the design for `ITEM-005`: migrating the interactive `create-new-specialist.sh` utility to Python.

## 1. Objective

To create a Python script that interactively prompts the user for information about a new Cognitive Specialist and appends the new specialist's definition to the `config/specialists.yml` file.

## 2. Component Design

The utility will be a Python module located at `assemblage/tools/create_new_specialist.py`.

### 2.1. Main Logic (`assemblage/tools/create_new_specialist.py`)

The script will guide the user through a series of prompts to gather the necessary information.

1.  **Import necessary libraries:** `sys`, `pathlib`, `pyyaml`.
2.  **Define Constants:** `REGISTRY_FILE = Path("config/specialists.yml")`.
3.  **`prompt_user()` function:**
    *   A helper function that takes a prompt string, prints it, and returns the user's input from `sys.stdin.readline()`. This will make the script more testable.
4.  **`main()` function:**
    *   The script will print a welcome message.
    *   It will call `prompt_user()` to get the `specialist_id`, `description`, `output_anchor`, and a multi-line `guide_prompt`.
    *   For the multi-line `guide_prompt`, the script will instruct the user to type 'EOF' on a new line to finish, and will loop, reading lines until it sees 'EOF'.
    *   **Validation:** The script will perform basic validation:
        *   The `specialist_id` cannot be empty.
        *   The script will load the `specialists.yml` file using `pyyaml` and check if the entered `specialist_id` already exists. If it does, the script will print an error and exit.
    *   **YAML Generation:** The script will construct a Python dictionary representing the new specialist.
    *   **File Append:** The script will open `REGISTRY_FILE` in append mode (`'a'`). It will then use `yaml.dump()` to serialize the new specialist dictionary into a YAML string and write it to the end of the file, preceded by a separator for readability.
    *   The script will print a success message upon completion.
5.  The script will be made executable using the `if __name__ == "__main__":` block.

### 2.2. Test Design (`tests/tools/test_create_new_specialist.py`)

The Pytest test will validate the script's logic by mocking user input and the file system.

1.  **`test_successful_creation(monkeypatch, tmp_path)`:**
    *   Creates a dummy `specialists.yml` in a temporary directory (`tmp_path`).
    *   Mocks the `sys.stdin.readline` function to provide a sequence of pre-defined inputs (ID, description, etc.).
    *   Runs the `main()` function of the script.
    *   Asserts that the `specialists.yml` file now contains the new specialist's data, correctly formatted.
2.  **`test_id_already_exists(monkeypatch, tmp_path)`:**
    *   Creates a dummy `specialists.yml` that already contains a specialist ID.
    *   Mocks `sys.stdin.readline` to provide the *same* specialist ID as the first input.
    *   Runs the `main()` function and asserts that it prints an error message and exits with a non-zero status code.
3.  **`test_empty_id_fails(monkeypatch, tmp_path)`:**
    *   Mocks `sys.stdin.readline` to provide an empty string as the first input.
    *   Runs the `main()` function and asserts that it prints an error and exits.

### 2.3. Decommissioning

Upon successful implementation and testing, the `tools/create-new-specialist.sh` script will be deleted.

This specification provides a complete plan for the Builder to execute.
