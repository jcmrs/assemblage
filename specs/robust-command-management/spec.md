# Specification: Robust Command Management

This document provides the detailed technical blueprint for `ITEM-025`, implementing robust command management as defined in `ADR-018`.

## 1. Naming Convention Note

To maintain consistency with the `add_nudge`/`remove_nudge` commands implemented in `ITEM-024`, we will use the verbs `add`, `remove`, and `update` for these commands. The user-facing commands will be `add-command`, `remove-command`, and `update-command`.

## 2. Core Design: `EntryPointValidator`

The "robust" nature of this feature hinges on validating that a command's `entry_point` string points to a real, callable function. To encapsulate this logic and make it reusable, we will create a new helper function.

- **New Function:** in a new `assemblage/validators.py` module.

```python
# assemblage/validators.py
import importlib.util
import sys

def validate_entry_point(entry_point: str):
    """
    Validates if a string entry point (e.g., 'module.submodule.function') is valid.
    Raises ImportError or AttributeError if not valid.
    """
    if ":" not in entry_point and "." not in entry_point:
        raise ValueError("Entry point must be in 'path.to.module:function' format.")

    # Split module path from function name
    try:
        module_path, function_name = entry_point.rsplit(':', 1)
    except ValueError:
        # Fallback for older dot notation for backwards compatibility if needed
        module_path, function_name = entry_point.rsplit('.', 1)


    # Check if the module can be found
    spec = importlib.util.find_spec(module_path)
    if spec is None:
        raise ImportError(f"Module '{module_path}' not found.")

    # Import the module and check for the function
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, function_name):
        raise AttributeError(f"Function '{function_name}' not found in module '{module_path}'.")
```

## 3. Command Definitions

- **File:** `config/commands.yml`
- **Action:** Add the new command management definitions.

```yaml
  add-command:
    entry_point: "assemblage.commands.manage_commands.add"
    help: "Adds a new command to config/commands.yml."
    args:
      - name: "name"
        help: "The name of the new command."
      - name: "entry_point"
        help: "The entry point in 'module.path:function' format."
      - name: "help"
        help: "The help text for the command."

  remove-command:
    entry_point: "assemblage.commands.manage_commands.remove"
    help: "Removes a command from config/commands.yml."
    args:
      - name: "name"
        help: "The name of the command to remove."

  update-command:
    entry_point: "assemblage.commands.manage_commands.update"
    help: "Updates an existing command in config/commands.yml."
    args:
      - name: "name"
        help: "The name of the command to update."
      - name: "--entry-point"
        required: false
        help: "The new entry point."
      - name: "--help"
        required: false
        help: "The new help text."
```

## 4. `manage_commands.py` Module Design

A new module, `assemblage/commands/manage_commands.py`, will be created. It will use the `ConfigManager` and the new `validate_entry_point` function.

```python
# assemblage/commands/manage_commands.py
from pathlib import Path
import sys
from assemblage.config_manager import ConfigManager
from assemblage.validators import validate_entry_point

COMMANDS_PATH = Path("config/commands.yml")

def add(args):
    try:
        # 1. Validate the entry point *before* adding it
        validate_entry_point(args.entry_point)

        # 2. Add to config
        manager = ConfigManager(COMMANDS_PATH)
        command_data = {"entry_point": args.entry_point, "help": args.help}
        manager.add_entry(args.name, command_data)
        print(f"Successfully added command '{args.name}'.")
        sys.exit(0)
    except (ValueError, ImportError, AttributeError, KeyError, Exception) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def remove(args):
    # ... similar logic using manager.remove_entry ...

def update(args):
    # ... similar logic using manager.read_config, validate_entry_point (if provided), and manager.update_entry ...
```
*(The `remove` and `update` functions will follow a similar pattern, with `update` only validating the entry point if it's passed as an argument.)*

## 5. Test Plan

- **`tests/test_validators.py`**:
    - A new test file for the `validate_entry_point` function.
    - `test_valid_entry_point`: Should pass without error.
    - `test_invalid_module_raises_error`: Should raise `ImportError`.
    - `test_invalid_function_raises_error`: Should raise `AttributeError`.
    - `test_invalid_format_raises_error`: Should raise `ValueError`.

- **`tests/commands/test_manage_commands.py`**:
    - A new test file for the command logic.
    - Will patch `ConfigManager` and `validate_entry_point`.
    - `test_add_success`: Verify `validate_entry_point` and `manager.add_entry` are called correctly.
    - `test_add_validation_fails`: Verify that if `validate_entry_point` raises an error, the command fails gracefully and `manager.add_entry` is *not* called.
    - Similar tests for `remove` and `update`.
