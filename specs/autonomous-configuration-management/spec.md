# Specification: Autonomous Configuration Management

This document provides the detailed technical blueprint for `ITEM-024`, implementing the core utilities for Autonomous Configuration Management as defined in `ADR-017`.

## 1. Core Design: A Reusable YAML Management Utility

Instead of implementing YAML reading/writing logic inside each new command (`add_command`, `add_nudge`, etc.), we will create a centralized, reusable utility module. This is a critical architectural decision to avoid code duplication and ensure consistent, safe handling of our configuration files.

- **New Module:** `assemblage/config_manager.py`

This module will contain a generic `ConfigManager` class.

### `ConfigManager` Class Design

```python
# assemblage/config_manager.py
from pathlib import Path
import yaml

class ConfigManager:
    def __init__(self, config_path: Path):
        """
        Initializes the manager for a specific YAML config file.
        """
        self.path = config_path
        if not self.path.exists():
            # Create the file with an empty dict if it doesn't exist
            self.path.write_text(yaml.dump({}))

    def read_config(self) -> dict:
        """Reads and parses the YAML file."""
        with open(self.path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def write_config(self, data: dict):
        """Writes a dictionary to the YAML file."""
        with open(self.path, "w", encoding="utf-8") as f:
            # Use a standard format for consistency
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def add_entry(self, key: str, value: dict, unique: bool = True):
        """Adds a new top-level entry."""
        config = self.read_config()
        if unique and key in config:
            raise KeyError(f"Entry '{key}' already exists in {self.path.name}.")
        config[key] = value
        self.write_config(config)

    def remove_entry(self, key: str):
        """Removes a top-level entry."""
        config = self.read_config()
        if key not in config:
            raise KeyError(f"Entry '{key}' not found in {self.path.name}.")
        del config[key]
        self.write_config(config)

    def update_entry(self, key: str, value: dict):
        """Updates an existing top-level entry."""
        config = self.read_config()
        if key not in config:
            raise KeyError(f"Entry '{key}' not found in {self.path.name}.")
        config[key] = value
        self.write_config(config)
```

## 2. Command Definitions

We will start by implementing only the commands for managing `nudges`, as they are the simplest case and will prove the `ConfigManager` utility. The `command` and `specialist` management commands will be implemented in their own backlog items (`ITEM-025`, etc.), but they will *use* this same `ConfigManager`.

- **File:** `config/commands.yml`
- **Action:** Add the new `add_nudge`, `remove_nudge`, and `update_nudge` command definitions.

```yaml
  add_nudge:
    entry_point: "assemblage.commands.manage_nudges.add"
    help: "Adds a new nudge to config/nudges.yml."
    args:
      - name: "id"
        help: "The unique ID for the new nudge (e.g., nudge_commit_message_check)."
      - name: "text"
        help: "The text content of the nudge."

  remove_nudge:
    entry_point: "assemblage.commands.manage_nudges.remove"
    help: "Removes a nudge from config/nudges.yml."
    args:
      - name: "id"
        help: "The ID of the nudge to remove."

  update_nudge:
    entry_point: "assemblage.commands.manage_nudges.update"
    help: "Updates an existing nudge in config/nudges.yml."
    args:
      - name: "id"
        help: "The ID of the nudge to update."
      - name: "text"
        help: "The new text content for the nudge."
```

## 3. `manage_nudges.py` Module Design

A new module, `assemblage/commands/manage_nudges.py`, will be created. It will use the `ConfigManager`.

```python
# assemblage/commands/manage_nudges.py
from pathlib import Path
import sys
from assemblage.config_manager import ConfigManager

NUDGES_PATH = Path("config/nudges.yml")

def add(args):
    manager = ConfigManager(NUDGES_PATH)
    try:
        manager.add_entry(args.id, args.text)
        print(f"Successfully added nudge '{args.id}'.")
        sys.exit(0)
    except (KeyError, Exception) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def remove(args):
    # ... similar logic using manager.remove_entry ...

def update(args):
    # ... similar logic using manager.update_entry ...
```
*(The `remove` and `update` functions will follow the same pattern as `add`)*

## 4. Test Plan

- **`tests/test_config_manager.py`**:
    - A new test file for the core utility.
    - Will use `tmp_path` to create a temporary YAML file.
    - `test_add_entry`: Verify a new entry is added correctly.
    - `test_add_duplicate_raises_error`: Verify `KeyError` is raised for duplicates.
    - `test_remove_entry`: Verify an entry is removed.
    - `test_remove_nonexistent_raises_error`: Verify `KeyError` is raised.
    - `test_update_entry`: Verify an entry is updated.

- **`tests/commands/test_manage_nudges.py`**:
    - A new test file for the command logic.
    - Will patch the `ConfigManager` to avoid actual file I/O.
    - `test_add_success`: Verify the `add` function calls `manager.add_entry` with the correct arguments.
    - `test_add_failure`: Verify that if `manager.add_entry` raises an error, the command prints to stderr and exits with 1.
    - Similar tests for `remove` and `update`.

This blueprint establishes a robust, reusable foundation for all future configuration management tasks.
