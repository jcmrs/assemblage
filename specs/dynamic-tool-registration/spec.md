# Specification: Dynamic Tool Registration

This document provides the detailed technical blueprint for `ITEM-018`, implementing the Dynamic Tool Registration architecture as defined in `ADR-011`.

## 1. File and Directory Structure

The following new files and directories will be created:

- `config/commands.yml`: The central command registry.
- `assemblage/commands/`: A new directory to house all command logic.
- `assemblage/commands/__init__.py`: To make it a package.
- `assemblage/commands/observe.py`: Module for the `observe` command.
- `assemblage/commands/validate.py`: Module for the `validate` command.
- `assemblage/commands/create_specialist.py`: Module for the `create_specialist` command.
- `assemblage/commands/nudge.py`: Module for the `nudge` command.
- `assemblage/commands/index.py`: Module for the `index` command.
- `assemblage/commands/query.py`: Module for the `query` command.
- `assemblage/commands/status.py`: Module for the `status` command.
- `assemblage/commands/new.py`: Module for the `new` command.
- `assemblage/commands/list.py`: Module for the `list` meta-command.
- `assemblage/commands/register.py`: Module for the `register` meta-command.
- `tests/commands/`: A new directory for testing the new command modules.

## 2. `config/commands.yml` Initial Content

The file will be initialized with all existing commands.

```yaml
# The single source of truth for all Control Plane commands.
commands:
  observe:
    entry_point: "assemblage.commands.observe.run"
    help: "Observe the state of the Assemblage and generate a status dashboard."
  validate:
    entry_point: "assemblage.commands.validate.run"
    help: "Run a full integrity check of the Assemblage."
  create_specialist:
    entry_point: "assemblage.commands.create_specialist.run"
    help: "Launch the interactive wizard to create a new Cognitive Specialist."
  nudge:
    entry_point: "assemblage.commands.nudge.run"
    help: "Deliver a behavioral nudge."
    arguments:
      - name: "nudge_id"
        help: "The ID of the nudge to deliver."
      - name: "current_workbench"
        help: "The active workbench."
  index:
    entry_point: "assemblage.commands.index.run"
    help: "Build the code intelligence index."
  query:
    entry_point: "assemblage.commands.query.run"
    help: "Perform a semantic query on the codebase."
    arguments:
      - name: "query"
        help: "The natural language query string."
  status:
    entry_point: "assemblage.commands.status.run"
    help: "Check the status of a system."
    arguments:
      - name: "--index"
        action: "store_true"
        help: "Check the status of the code index."
  new:
    entry_point: "assemblage.commands.new.run"
    help: "Create a new process document from a template."
    arguments:
      - name: "--type"
        required: true
        choices: ["item"]
        help: "The type of document to create."
      - name: "--title"
        required: true
        help: "The title of the new document."
      - name: "--from-adr"
        help: "The ID of the source ADR to link from."
      - name: "--from-item"
        help: "The ID of the source backlog item to link from."
```

## 3. Refactoring `assemblage/control_plane.py`

This module will be completely refactored into a dynamic loader.

- **Remove All Command Logic:** All `_function` and `function_command` handlers will be deleted.
- **New Dependencies:** `import yaml`, `import importlib`.
- **New `main()` Logic:**
    1. Load and parse `config/commands.yml`.
    2. Create the main `ArgumentParser`.
    3. Loop through the `commands` dictionary from the YAML file.
    4. For each command, dynamically create a sub-parser using `subparsers.add_parser()`.
    5. For each argument defined for a command, dynamically call `sub_parser.add_argument()`. The `action` key (e.g., `store_true`) must be handled correctly.
    6. Use `sub_parser.set_defaults(func=...)` to store a *lambda function* or a partial that captures the `entry_point` string.
    7. After parsing args, dynamically import the module from the stored `entry_point` string (e.g., using `importlib.import_module`).
    8. Get the function from the imported module (e.g., using `getattr`).
    9. Execute the function, passing it the `args`.

## 4. Creating Command Modules

- For each command, a new file will be created in `assemblage/commands/`.
- The logic from `control_plane.py` will be moved into a `run(args)` function in the corresponding new module.
- Any helper functions (like `_check_git_integrity`) will be moved into a shared `assemblage/commands/helpers.py` module if used by multiple commands, or kept within the command module if used by only one.

## 5. Implementing Meta-Commands

- **`assemblage/commands/list.py`**:
    - `run(args)` function will load `config/commands.yml`, iterate through the commands, and print their names and help text in a formatted way.
- **`assemblage/commands/register.py`**:
    - `run(args)` function will launch an interactive prompt sequence using `input()` to ask for the command name, entry point, help text, and arguments.
    - It will then load `config/commands.yml`, add the new command data, and write the file back, preserving YAML formatting.

## 6. Test Plan

- **Refactor Existing Tests:** All tests that currently call `control_plane.main()` will need to be updated or mocked to work with the new dynamic dispatch.
- **New Tests for `control_plane.py`:**
    - A test to ensure it correctly parses `config/commands.yml` and builds the `argparse` structure.
    - A test to ensure it correctly calls the specified entry point.
- **New Tests for `assemblage/commands/`:**
    - Unit tests for each new command module in `tests/commands/`.
    - A test for `list.py` to ensure it prints the correct output.
    - A test for `register.py` that uses a mock `input` and a temporary `commands.yml` to verify a new command is added correctly.

This blueprint provides a comprehensive and actionable plan for the Builder.
