# ADR-028: Comprehensive Command Argument Management

**Date:** 2025-11-24
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The implementation of `ITEM-025: Robust Command Management` successfully provided commands to add, remove, and update command definitions in `config/commands.yml`. However, the `update-command` functionality is incomplete: it allows for changing a command's `entry_point` and `help` text, but provides no mechanism to add, remove, or modify the arguments (`args`) associated with that command. This is a significant gap, as it means any change to a command's interface still requires manual editing of the YAML file, undermining the goal of full programmatic control.

## 2. Decision

We will implement **Comprehensive Command Argument Management** by enhancing the `update-command` command and potentially creating new, dedicated sub-commands.

This will involve:

1.  **`update-command --add-arg`:** A new flag for the `update-command` that takes key-value pairs to define a new argument (e.g., `--add-arg name=--foo help='Does a thing' required=true`).
2.  **`update-command --remove-arg`:** A new flag to remove an existing argument by its name (e.g., `--remove-arg --foo`).
3.  **`update-command --update-arg`:** A new flag to modify an existing argument (e.g., `--update-arg name=--foo help='Does a new thing'`).

This functionality will be built upon the existing `ConfigManager` utility. The logic will involve reading the command's data, modifying the `args` list within that data structure, and writing it back.

## 3. Rationale

*   **Completes the Lifecycle:** Provides full, programmatic control over the entire command definition lifecycle, including its arguments.
*   **Eliminates Manual Edits:** Removes the last remaining reason for manually editing `config/commands.yml` for command-related changes.
*   **Enhances Autonomy:** Further empowers the System Owner to manage its own capabilities and interfaces without human intervention.
*   **Consistency:** Brings the management of command arguments in line with the management of the commands themselves.

## 4. Consequences

- The `update-command` will become significantly more complex, parsing multiple new flags and their values.
- Robust validation will be needed for the argument definitions being added or updated.
- This change solidifies the `ConfigManager` as the central point of control for all system configuration.
