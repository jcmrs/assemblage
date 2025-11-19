# Idea: Dynamic Tool Registration and Discovery

## 1. Concept

To evolve the Control Plane from a static, manually-edited module into a dynamic system that can register and discover new capabilities, in alignment with the Extensibility cornerstone.

## 2. Problem

Currently, adding a new command to the Control Plane requires manually editing `control_plane.py` to add the `argparse` setup, the import statement, and the handler function. This is a direct modification of the core "brain" and is not scalable.

## 3. Proposed Solution

Implement a registration-based architecture for the Control Plane.

1.  **Configuration File:** Create a `config/control_plane.yml` file. This file would contain a list of all registered commands, their entry point functions, and their `argparse` definitions.
    ```yaml
    commands:
      observe:
        entry_point: "assemblage.lib.observe.run"
        help: "Observe the state of the Assemblage."
      validate:
        entry_point: "assemblage.lib.validate.run"
        help: "Run a full integrity check."
    ```
2.  **Dynamic Loading:** The `control_plane.py` `main()` function would be refactored. Instead of having hardcoded command definitions, it would:
    *   Read `config/control_plane.yml`.
    *   Dynamically build the `argparse` sub-parsers based on the file's contents.
    *   Dynamically import and call the specified `entry_point` function for the chosen command.
3.  **New Meta-Commands:**
    *   `control_plane register <command_name> <entry_point>`: A new command that programmatically adds a new tool to the `control_plane.yml` file.
    *   `control_plane list_commands`: A command that lists all currently registered commands and their help text.

## 4. Value Proposition

- **True Extensibility:** New tools can be added without touching the core Control Plane code, dramatically reducing the risk of breaking changes.
- **Improved Discoverability:** The AI can ask the system what it is capable of.
- **Cleaner Architecture:** Separates the Control Plane's orchestration logic from its configuration.
