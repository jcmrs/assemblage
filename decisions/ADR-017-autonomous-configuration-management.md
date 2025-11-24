# ADR-017: Autonomous Configuration Management

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Assemblage's core operational parameters are defined in YAML configuration files (`config/commands.yml`, `config/nudges.yml`, `config/specialists.yml`). While these files provide flexibility, the current method of modifying them involves manual editing (either by the Vision Owner or by the System Owner through brittle `replace` operations). In an AI-First environment, this manual intervention represents a significant gap in the system's autonomy and introduces potential for errors. The System Owner should be able to manage its own configuration programmatically and safely.

## 2. Decision

We will implement **Autonomous Configuration Management** by introducing a set of `control_plane` commands designed to programmatically manage the Assemblage's configuration files.

Specifically, we will develop commands to:

1.  **Manage `config/commands.yml`:**
    *   `control_plane add_command <name> --entry-point <path> --help <text>`
    *   `control_plane remove_command <name>`
    *   `control_plane update_command <name> --entry-point <path> --help <text>`

2.  **Manage `config/nudges.yml`:**
    *   `control_plane add_nudge <id> <text>`
    *   `control_plane remove_nudge <id>`
    *   `control_plane update_nudge <id> <new_text>`

3.  **Manage `config/specialists.yml`:**
    *   `control_plane add_specialist <id> --description <text> --prompt <path>`
    *   `control_plane remove_specialist <id>`
    *   `control_plane update_specialist <id> --description <text> --prompt <path>`

**Underlying Mechanism:**
Each of these commands will:
*   Read the target YAML file.
*   Parse its content into a Python dictionary.
*   Perform the requested modification (add, update, or delete an entry).
*   **Validate** the modified configuration against a predefined schema or logical rules (e.g., ensuring `entry_point` for commands is a valid Python path, ensuring unique IDs).
*   Write the updated dictionary back to the YAML file, preserving its structure and comments where feasible.

## 3. Rationale

*   **Enhanced Autonomy:** Enables the System Owner to self-manage its operational parameters, aligning with the AI-First principle.
*   **Reduced Errors:** Programmatic management eliminates human error associated with manual YAML editing (e.g., syntax errors, incorrect indentation).
*   **Streamlined Workflow:** Integrates configuration changes directly into the `control_plane` workflow, making the system more cohesive.
*   **Foundation for Advanced Learning:** Provides the necessary infrastructure for future capabilities where the System Owner might autonomously propose and implement configuration changes based on its learning.

## 4. Consequences

- This will introduce several new `control_plane` commands and corresponding Python modules.
- Requires robust YAML parsing, manipulation, and writing logic, potentially involving a library that preserves YAML structure/comments.
- Introduces the need for schema validation for configuration files to ensure integrity.
- The `control_plane new` command will need to be updated to reflect these new configuration management capabilities.
