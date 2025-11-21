# ADR-011: Dynamic Tool Registration

**Date:** 2025-11-19
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The `control_plane.py` module, while consolidated, has become a monolithic bottleneck. To add any new capability, the core file itself must be manually edited to add imports, handler functions, and `argparse` definitions. This violates the Open/Closed Principle (open for extension, closed for modification) and does not scale. It represents a significant architectural weakness that hinders true extensibility and increases the risk of introducing breaking changes into our most critical module.

This ADR reverses the consolidation performed in `ITEM-012`. That consolidation was a necessary intermediate step to clean up the legacy `tools/` directory. We now have the stability and insight required to take the next, more mature architectural step: true decoupling.

## 2. Decision

We will refactor the Control Plane into a **Dynamic Command Loader** driven by a declarative configuration file.

1.  **Declarative Command Registry:** A new file, `config/commands.yml`, will become the single source of truth for all Control Plane commands. It will define each command's name, help text, arguments, and the Python entry point that implements its logic.

2.  **Dynamic Command Loader:** `control_plane.py` will be refactored. Its sole purpose will be to:
    *   Read `config/commands.yml` on startup.
    *   Programmatically build its `argparse` interface based on the definitions in the YAML file.
    *   Dynamically import and execute the specified Python entry point for the invoked command.

3.  **Decoupled Command Implementation:** The logic for each command (e.g., `observe`, `validate`) will be moved out of `control_plane.py` and into its own dedicated module within a new `assemblage/commands/` directory (e.g., `assemblage/commands/observe.py`, `assemblage/commands/validate.py`).

4.  **Meta-Commands for Self-Management:** The Control Plane will be given two new, built-in "meta-commands":
    *   `control_plane list`: To display all available, registered commands.
    *   `control_plane register`: An interactive command to programmatically add a new command definition to `config/commands.yml`.

## 3. Rationale

This architecture directly serves our highest imperatives.

*   **Extensibility:** This is the core driver. New tools can be created and "registered" without ever touching the `control_plane.py` code, making the system infinitely extensible in a safe and scalable manner.
*   **AI-First:** The `register` and `list` commands empower the AI System Owner to understand and extend its own capabilities programmatically. This is a foundational skill for a truly autonomous agent.
*   **Holistic System Thinking:** This design enforces a clean separation of concerns between the command *interface* (Control Plane), the command *definition* (`commands.yml`), and the command *implementation* (`assemblage/commands/`).

## 4. Example Usage

**`config/commands.yml`:**
```yaml
commands:
  observe:
    entry_point: "assemblage.commands.observe.run"
    help: "Observe the state of the Assemblage and generate a status dashboard."
  validate:
    entry_point: "assemblage.commands.validate.run"
    help: "Run a full integrity check of the Assemblage."
    arguments:
      - name: "--silent"
        action: "store_true"
        help: "Run validation without verbose output."
```

**Registering a new command:**
```
> python -m assemblage.control_plane register
[PROMPT] Enter the name of the new command: my_new_tool
[PROMPT] Enter the Python entry point (e.g., assemblage.commands.my_new_tool.run): ...
[PROMPT] Enter the help text: ...
INFO: Command 'my_new_tool' successfully registered in config/commands.yml.
```

## 5. Consequences

- This is a significant refactoring that will touch many parts of the system.
- It introduces a new layer of abstraction (the YAML file) that must be managed.
- It fully realizes the vision of a decoupled, extensible Control Plane, setting the stage for all future development and making the Assemblage far more robust and scalable.
