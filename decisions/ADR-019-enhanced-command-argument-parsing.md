# ADR-019: Enhanced Command Argument Parsing

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Control Plane's command definition in `config/commands.yml` currently supports a very basic subset of `argparse` features for command arguments (e.g., `name`, `help`, `action`, `required`, `choices`). This limitation restricts the complexity and flexibility of commands that can be dynamically registered. For instance, it's not possible to specify argument types (e.g., `type=int`), default values, or more advanced argument behaviors (`nargs`). This forces more complex argument parsing logic into the command's Python implementation rather than declarative configuration.

## 2. Decision

We will enhance the Control Plane's command argument parsing capabilities to support a richer set of `argparse` features declaratively within `config/commands.yml`.

This will involve:

1.  **Extending the `commands.yml` Schema:** Add support for additional `argparse` parameters for each argument, such as:
    *   `type`: (e.g., `str`, `int`, `float`, `bool`)
    *   `default`: A default value if the argument is not provided.
    *   `nargs`: (e.g., `?`, `*`, `+`, `int`)
    *   `const`: A value that should be stored if the argument is encountered.
    *   `metavar`: A name for the argument in usage messages.
2.  **Updating the Command Loader:** Modify the Control Plane's command loading logic to correctly interpret these new parameters and pass them to `argparse.ArgumentParser.add_argument()`.
3.  **Validation:** Implement validation to ensure that the new argument parameters are correctly specified in `commands.yml` (e.g., `type` refers to a valid Python type).

## 3. Rationale

*   **Increased Flexibility:** Allows for more sophisticated and user-friendly command-line interfaces to be defined declaratively.
*   **Reduced Boilerplate:** Moves argument parsing logic from Python code into configuration, reducing the amount of repetitive code in command modules.
*   **Improved Usability:** Enables better help messages and automatic type conversion for command arguments.
*   **Alignment with `argparse`:** Leverages the full power of Python's standard argument parsing library.

## 4. Consequences

- Requires modifications to the Control Plane's core command loading and argument parsing logic.
- The schema for `config/commands.yml` will become more complex.
- New validation logic will be needed to ensure correct usage of the extended argument parameters.
