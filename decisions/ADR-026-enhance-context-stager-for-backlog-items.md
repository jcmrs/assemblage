# ADR-026: Enhance Context Stager for Backlog Items

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The current implementation of the Context Staging System, specifically the `control_plane new --type item` command, generates backlog items that often have a high context window dependency. While these items link to their parent Architecture Decision Records (ADRs), they do not sufficiently extract and embed the "Why" (context, decision, rationale) and detailed "What" (acceptance criteria) directly into the backlog item itself. This forces users (including the System Owner) to constantly refer back to the ADR or rely on implicit knowledge, hindering clarity, efficiency, and the self-contained nature of process artifacts.

## 2. Decision

We will enhance the `control_plane new --type item` command to create **more self-contained and context-rich backlog items**.

This enhancement will involve:

1.  **Richer "Why" Integration:** When a backlog item is created from an ADR, the `new --type item` command will:
    *   Extract a concise summary of the ADR's "Context" and "Decision" sections.
    *   Embed this summary directly into the backlog item's "Description" or a dedicated "Why" section, ensuring the item's purpose is immediately clear.
2.  **Guided "What" Generation:** The command will:
    *   More actively guide the user (or System Owner) in defining comprehensive and granular "Acceptance Criteria" for the backlog item.
    *   Potentially extract key outcomes or requirements from the ADR's "Decision" and "Consequences" sections to pre-populate or suggest acceptance criteria.
3.  **Template Update:** The `backlog/items/TEMPLATE.md` will be updated to reflect this richer structure.

## 3. Rationale

*   **Reduced Context Window Dependency:** Makes each backlog item more self-contained, reducing the need to constantly refer to parent documents.
*   **Improved Clarity and Efficiency:** Enhances understanding of the item's purpose and scope, streamlining the Architect and Builder phases.
*   **Enhanced AI-First Principles:** Aligns with the goal of creating autonomous, self-documenting, and easily understandable process artifacts.
*   **Better Planning Artifacts:** Leads to higher quality backlog items that are more actionable and less ambiguous.

## 4. Consequences

- Requires modifications to the `assemblage/commands/new.py` module.
- Involves more sophisticated Markdown parsing and text summarization/extraction logic within the `new` command.
- The `backlog/items/TEMPLATE.md` will need to be updated.
- Existing backlog items will not be retroactively updated by this change, but future ones will benefit.
