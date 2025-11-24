# ADR-024: Automated Git Hooks Setup

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Assemblage relies heavily on `pre-commit` hooks (defined in `.pre-commit-config.yaml`) for maintaining code quality, running linters, and automatically rebuilding the code intelligence index. Currently, users must manually run `pre-commit install` after cloning the repository to activate these hooks. This manual step is easily overlooked, leading to inconsistencies in development environments and potential failures in automated processes (like index rebuilding). Automating this setup is crucial for a seamless developer experience and ensuring the integrity of the Assemblage.

## 2. Decision

We will implement an **Automated Git Hooks Setup** mechanism.

This will involve:

1.  **New Command:** A new `control_plane setup_hooks` command will be created.
2.  **Command Logic:** This command will:
    *   Check if `pre-commit` is installed (and if not, guide the user to install it).
    *   Execute `pre-commit install` to set up the git hooks in the current repository.
    *   Provide clear feedback on the success or failure of the installation.
3.  **Integration:** This command will be prominently featured in the Comprehensive Getting Started Guide (`ADR-023`) and potentially integrated into an automated onboarding process (`ADR-025`).

## 3. Rationale

*   **Ensured Code Quality:** Guarantees that essential code quality checks and automated processes (like index rebuilding) are active in every developer's environment.
*   **Improved Developer Experience:** Eliminates a manual, easily forgotten step, streamlining the setup process.
*   **Consistency:** Ensures all developers are using the same set of pre-commit hooks.
*   **Reduced Errors:** Prevents issues arising from missing or incorrectly installed hooks.

## 4. Consequences

- Requires a new `control_plane` command and corresponding Python module.
- Involves interacting with the `pre-commit` tool via `subprocess`.
- The `Comprehensive Getting Started Guide` will need to reference this new command.
