# Product Plan: Control Plane Build-Out

**Date:** 2025-11-18
**Status:** Defined

---

## 1. Objective

This document defines the scope and plan for the full build-out of the Assemblage Control Plane. The goal is to migrate all remaining standalone utilities into sub-commands of the central `assemblage/control_plane.py` module, completing the architectural vision outlined in `ADR-006`.

---

## 2. Project Scope and Definition

This project will complete the decoupling of the agent from its tools by making the Control Plane the single, abstract entry point for all system-level actions.

### 2.1. Architectural Pattern

For each utility, the following pattern will be applied:
1.  The core logic of the utility will be contained in its own module within `assemblage/tools/`.
2.  The `assemblage/control_plane.py` module will be updated with a new sub-command (e.g., `validate`).
3.  The sub-command handler in the Control Plane will import and call the corresponding logic module.
4.  The old standalone script will be decommissioned.
5.  The `tests/test_control_plane.py` file will be updated with a new test for the new sub-command.

### 2.2. Scope of Work (Utilities to be Integrated)

The following utilities will be integrated as commands into the Control Plane:

*   **`validate`:** (from `validate_assemblage.py`) - To run the full system integrity check.
*   **`create_specialist`:** (from `create_new_specialist.py`) - To launch the interactive specialist creation wizard.
*   **`nudge`:** (from `nudge.py`) - To deliver a behavioral nudge.
*   **`pre_commit`:** (from `pre_commit_hook.py`) - To run the linter (this will be called by the git hook, but can also be made available as a manual command).

This list constitutes the full scope of the build-out project.
