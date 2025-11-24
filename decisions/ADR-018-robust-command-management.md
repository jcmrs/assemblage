# ADR-018: Robust Command Management

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Control Plane's dynamic command loading mechanism relies on `config/commands.yml`. While the `register` command exists, it is currently basic:
1.  It does not validate the `entry_point` (e.g., checking if the module/function actually exists).
2.  There are no mechanisms to `unregister` or `update` existing commands programmatically.
This leads to a brittle system where invalid commands can be registered, and managing the command lifecycle requires manual editing of the YAML file, which is prone to errors and breaks the autonomous workflow.

## 2. Decision

We will implement a **Robust Command Management** system within the Control Plane. This will involve:

1.  **`control_plane register <name> --entry-point <path> --help <text>`:**
    *   Enhance this command to perform basic validation of the `entry_point` (e.g., attempt to `importlib.util.find_spec` the module path).
    *   Ensure the command name is unique.
2.  **`control_plane unregister <name>`:**
    *   A new command to safely remove a command definition from `config/commands.yml`.
    *   It will confirm the command exists before attempting removal.
3.  **`control_plane update_command <name> --entry-point <path> --help <text>`:**
    *   A new command to modify an existing command's `entry_point` or `help` text.
    *   It will perform the same validation as `register` for the new `entry_point`.

These commands will leverage the underlying YAML management capabilities developed for Autonomous Configuration Management (`ADR-017`).

## 3. Rationale

*   **System Stability:** Prevents the registration of invalid commands, reducing runtime errors.
*   **Improved Autonomy:** Allows the System Owner to manage its own command set programmatically, without manual YAML editing.
*   **Maintainability:** Simplifies the process of adding, removing, or modifying commands, making the system easier to evolve.
*   **Consistency:** Ensures that command definitions adhere to expected standards.

## 4. Consequences

- Requires new modules and logic for command validation and manipulation of `config/commands.yml`.
- Builds upon the foundation laid by `ADR-017` (Autonomous Configuration Management).
- The `control_plane` will gain more self-management capabilities.
