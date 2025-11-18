# ADR-007: Control Plane Build-Out

**Date:** 2025-11-18
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## Context

With the successful implementation of the `observe` command, the foundation of the Control Plane architecture is in place (`ADR-006`). However, several other utilities (`validate_assemblage`, `create_new_specialist`, etc.) still exist as standalone, directly-executable Python modules. To complete the architectural vision and fully realize the benefits of decoupling, these remaining utilities must be integrated into the Control Plane.

## Decision

All remaining Python utilities in `assemblage/tools/` will be refactored to be capabilities accessible only through the central `assemblage/control_plane.py` module. Each utility will become a sub-command of the Control Plane's command-line interface.

*   `python -m assemblage.tools.validate_assemblage` will become `python -m assemblage.control_plane validate`
*   `python -m assemblage.tools.create_new_specialist` will become `python -m assemblage.control_plane create_specialist`
*   ...and so on.

The standalone modules will be refactored into libraries, and their `if __name__ == "__main__"` blocks will be removed.

## Rationale

This decision is the logical conclusion of `ADR-006`. It fully commits us to the "Control Plane as a Tool" pattern.

*   **Consistency:** It creates a single, consistent, and predictable way for the agent to interact with all system capabilities.
*   **Centralized Governance:** It reinforces the Control Plane as the single point for logging, auditing, and managing all tool use.
*   **Reduced Cognitive Load:** The agent no longer needs to remember the individual paths to a dozen different tools, only the abstract capabilities offered by the single Control Plane.
*   **Completes the Architecture:** This work completes the foundational layer of our agentic architecture, providing a stable base for all future development.

## Consequences

### Positive
- A fully unified and consistent interface for all system tools.
- The agent's interaction model is greatly simplified.
- The architecture is now fully aligned with the "decoupled" vision.

### Negative
- None. This is the completion of an in-progress architectural refactor.

## Alternatives Considered

- **Leaving utilities as standalone scripts:** This was rejected as it would leave the architecture in an inconsistent, hybrid state, undermining the purpose of the Control Plane.

## Related Decisions

- This ADR is the direct implementation plan for the vision laid out in `ADR-006`.
