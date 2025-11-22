# ADR-016: Autonomous Dependency Management

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The System Owner currently has a significant blind spot: it cannot manage its own Python dependencies. When a new tool is required (e.g., `pytest-cov`), the `requirements.txt` file must be updated manually, and the installation must be run by an external actor. This breaks the autonomy of the agent and requires human intervention for a basic developer task.

## 2. Decision

We will implement an **Autonomous Dependency Management** capability within the Control Plane.

1.  **New Command:** A new `control_plane install_dependencies` command will be created.
2.  **Command Logic:** The command will perform the following actions:
    *   Read the `requirements.txt` file.
    *   Use `pip` to install all listed dependencies. The command will be executed as a subprocess from within the Python environment, ensuring it uses the correct `pip` instance.
    *   The command will be designed to be idempotent, meaning it can be run safely multiple times.
3.  **Future Integration:** This command establishes the foundation for true autonomy. In the future, when a tool fails due to a missing dependency (`ModuleNotFoundError`), the system's error handling can be taught to:
    1.  Identify the missing library.
    2.  Add it to `requirements.txt`.
    3.  Run `control_plane install_dependencies`.
    4.  Re-try the original failed command.

## 3. Rationale

*   **Practical Autonomy:** Gives the System Owner the "hands" to manage its own environment, a critical skill for an independent agent.
*   **Self-Sufficiency:** Eliminates a key area where human intervention is currently required, making the Assemblage more robust and self-contained.
*   **Foundation for Self-Healing:** Establishes the core capability required for the system to eventually diagnose and fix its own missing dependency errors.

## 4. Consequences

- This feature requires the AI to be able to execute shell commands that modify its own Python environment (`pip install`). This must be handled with care.
- It introduces a new command that will become a standard part of the system's setup and maintenance procedures.
