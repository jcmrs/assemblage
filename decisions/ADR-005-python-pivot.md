# ADR-005: Architectural Pivot to Python for Assemblage Utilities

**Date:** 2025-11-16
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## Context

The Assemblage has been suffering from a hard blocker (`ADR-004`) related to an irreconcilable conflict between the Windows host environment (which creates CRLF line endings) and the Bash-based execution environment for utilities (which requires LF line endings). This has made the creation and testing of any new automation impossible, violating our core imperatives of "Automation" and "AI-First." Expert consultations have confirmed that this friction is inherent to the architectural choice of using a non-native scripting language (Bash) on Windows.

## Decision

The Assemblage will undertake a full, high-priority architectural pivot away from Bash scripting for its automation and utility layer.

1.  **The new official language for all utilities will be Python 3.x.**
2.  All existing Bash scripts in `tools/` will be migrated to Python modules within a new `assemblage/` source directory.
3.  The BATS testing framework will be decommissioned and replaced with **Pytest**.
4.  Project dependencies and configuration will be managed via `pip`, `requirements.txt`, and `pyproject.toml`.

This decision is based on the comprehensive research and planning documented in:
*   `knowledge/research/python_best_practices.md`
*   `knowledge/research/bash_to_python_migration_plan.md`
*   `product/python_migration_plan.md`

## Rationale

This decision addresses the root cause of our platform instability, rather than attempting further brittle, symptomatic fixes.

*   **Robustness & Stability:** Python provides a true cross-platform runtime, abstracting away OS-level details like line endings and path separators. This permanently solves the blocker and makes the "house" stable for the AI to work in.
*   **AI-First:** Python is the lingua franca of AI and automation. Adopting it makes the Assemblage more powerful and reduces the cognitive load on the System Owner, as it provides a richer, more predictable toolset than Bash.
*   **Maintainability & Extensibility:** A single, modern, high-level language is easier to maintain and extend than a collection of shell scripts. The Python ecosystem provides vast libraries for any future needs.
*   **Constitutional Alignment:** This pivot reinforces all our imperatives by replacing a flawed, brittle system with one that is modular, automated, and designed for a predictable, AI-First environment.

## Consequences

### Positive
- Permanently resolves the line-ending blocker.
- Makes the Assemblage platform-agnostic and more robust.
- Upgrades our automation capabilities with a more powerful language.
- Creates a more maintainable and extensible codebase for utilities.

### Negative
- Requires a significant, one-time effort to migrate existing scripts and testing infrastructure. This is accepted as a necessary cost to fix a foundational flaw.
- Introduces a dependency on a Python 3.x interpreter being available in the environment. This is deemed an acceptable and standard prerequisite.

## Alternatives Considered

- **Retaining Bash with WSL:** This was rejected as it imposes a more significant environmental requirement on the host machine and does not address the inherent brittleness of complex shell scripting compared to a high-level language.
- **Retaining Bash with more workarounds:** This was rejected as it has been proven to be an unproductive loop that violates our core principles.

## Related Decisions

- This ADR **supersedes** the testing framework decision in `ADR-003`. The BATS framework and its submodules will be decommissioned.
- This ADR **resolves** the blocker documented in `ADR-004`.

## Follow-up Actions

- [X] Create a full set of high-priority backlog items to execute the migration plan defined in `product/python_migration_plan.md`.
