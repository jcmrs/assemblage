# ADR-006: Control Plane Architecture

**Date:** 2025-11-18
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## Context

Our initial Assemblage design tightly coupled the System Owner (AI) to its tools. The AI was directly responsible for knowing the specific commands and paths for each utility. This led to a system-wide failure when an environmental issue (line endings) consumed the agent's reasoning loop. A more robust, scalable, and abstract architecture is needed to prevent this and to support more advanced agentic patterns in the future.

## Decision

The Assemblage will adopt a **"Control Plane as a Tool"** design pattern. This is a formal architectural decision to decouple the agent's reasoning from the tool's implementation.

1.  **A Central Control Plane Module:** A new, central Python module will be created at `assemblage/control_plane.py`.
2.  **Abstracted Interaction:** The System Owner (AI) will no longer call individual tool scripts directly. Instead, it will make abstract, capability-based requests to the Control Plane module.
    *   *Example:* Instead of `python -m assemblage.tools.validate_assemblage`, the AI will execute `python -m assemblage.control_plane validate`.
3.  **Control Plane as Orchestrator:** The Control Plane module will be responsible for receiving these abstract requests, mapping them to the correct underlying tool implementation, executing the tool, and returning a structured result.

## Rationale

This architectural pattern is a direct solution to the challenges of building a scalable and resilient Agentic AI System.

*   **Decoupling:** It separates the "what" (the agent's intent, e.g., "validate the system") from the "how" (the specific script and command to run). This is a fundamental principle of good software architecture.
*   **Extensibility & Maintainability:** Tools can be changed, refactored, or rewritten in different languages without ever affecting the agent's core logic. To add a new capability, we simply register it with the Control Plane.
*   **Governance & Observability:** The Control Plane becomes a single point of entry for all tool use, making it the perfect place to implement logging, auditing, and security checks.
*   **Reduced Cognitive Load (AI-First):** The AI no longer needs to manage a complex mental map of tool paths and commands. It only needs to know what capabilities the Control Plane offers. This frees up its reasoning capacity for higher-level strategic tasks.

## Consequences

### Positive
- Dramatically increases the robustness and resilience of the Assemblage.
- Creates a scalable architecture prepared for more advanced, multi-tool, and multi-agent workflows.
- Simplifies the agent's decision-making process.
- Centralizes tool orchestration and governance.

### Negative
- Introduces a layer of indirection, which adds a small amount of complexity to the initial creation of a new tool (as it must be registered with the Control Plane). This is a worthwhile trade-off for the immense gain in stability and scalability.

## Alternatives Considered

- **Direct Tool Use (The Status Quo):** This was rejected as it has already been proven to be brittle and prone to failure, as documented in `ADR-004`.

## Related Decisions

- This ADR is the strategic foundation for the Python Pivot described in `ADR-005`. It provides the core "Why" for that migration.

## Implementation Notes

- The `control_plane.py` module will use Python's `argparse` to create a command-line interface with sub-commands for each capability (e.g., `observe`, `validate`).
- The initial implementation will focus on wiring up the `observe` command to the dashboard generation logic.
