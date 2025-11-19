# ADR-008: Self-Correction Loop for Pre-Commit Hooks

**Date:** 2025-11-18
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## Context

The current `pre-commit` framework, while effective, halts the AI's workflow on any failure, even easily correctable ones (e.g., formatting issues fixed by `ruff --fix`). This requires manual intervention and is not fully aligned with our AI-First imperative. We need a mechanism that allows the system to solve its own simple problems.

## Decision

We will implement a "Self-Correction Loop" for our pre-commit workflow. The implementation will be a wrapper script that orchestrates the `git commit` process and will adhere to the following safety-critical principles:

1.  **One-Retry-Only Rule:** The loop will re-attempt a commit **at most one time**. If the commit fails a second time for any reason, the process must halt and report the failure. This is the primary safeguard against infinite loops.
2.  **Explicit "Fix" Detection:** The loop will only trigger if a pre-commit hook both fails (non-zero exit code) and explicitly reports that it has modified files on disk.
3.  **Clear and Verbose Logging:** The wrapper script must provide crystal-clear log output indicating that a hook failed, a fix was applied, and a re-commit is being attempted. This ensures the process is never a "black box."
4.  **Phased Rollout:** The implementation will be delivered in two phases: an "observe-only" phase to validate the detection logic, followed by an "activation" phase.

## Rationale

This decision moves the Assemblage towards a more truly AI-First architecture, where the system can handle low-level, predictable failures autonomously.

*   **Increased Autonomy:** Frees up both the System Owner and Vision Owner from intervening in trivial, automatable fixes.
*   **Improved Workflow Velocity:** Prevents the development cycle from being unnecessarily halted.
*   **Risk Mitigation:** The strict design principles (one-retry, explicit detection, logging) are designed to mitigate the risks of unintended consequences, such as hiding deeper bugs or entering infinite loops.

## Consequences

### Positive
- The system becomes more resilient and autonomous.
- A significant source of friction is removed from the development workflow.

### Negative
- Introduces a small amount of complexity into the commit process via the wrapper script. This is a necessary trade-off for the gain in autonomy.
- If not implemented carefully, it could mask underlying issues. The "one-retry-only" rule is designed to prevent this.

## Alternatives Considered

- **Status Quo:** Leaving the pre-commit process as-is. Rejected as it does not meet our AI-First goals.
- **Directly Modifying `pre-commit`:** Attempting to alter the behavior of the `pre-commit` framework itself. Rejected as overly complex and brittle; a wrapper script is a cleaner, more maintainable solution.
