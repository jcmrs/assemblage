# ADR-020: Full Context Staging Pipeline

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Context Staging System (`control_plane new` command) was designed to streamline the creation of process documents by assembling relevant context. Currently, it supports the creation of ADRs and backlog items, with the `item` type being able to pull context from an `adr`. However, the pipeline is incomplete; there is no direct mechanism to generate a `spec` document from a `backlog item`, pre-populated with the item's acceptance criteria and linked to its parent ADR. This forces manual copying and pasting of information, breaking the intended seamless flow of the "Conveyor Belt."

## 2. Decision

We will extend the Context Staging System to implement a **Full Context Staging Pipeline**, specifically enabling the generation of a `spec` document from an existing `backlog item`.

This will involve:

1.  **Enhancing `control_plane new --type spec`:**
    *   The command will accept an argument referencing an existing `backlog item` (e.g., `--item ITEM-XXX`).
    *   It will read the specified `backlog item` Markdown file.
    *   It will extract the "What" (Acceptance Criteria) and the link to the parent ADR from the backlog item.
    *   It will generate a new `spec.md` file within a new directory (e.g., `specs/item-xxx-title/spec.md`), pre-populating it with the extracted acceptance criteria and the ADR link.
    *   The generated spec will include a clear structure for the "How" (module design, function signatures, test plan) for the Builder to fill.
2.  **Updating `backlog item` Status:** The `control_plane new --type spec` command will optionally update the status of the parent `backlog item` to "In Progress" or "Ready for Build" (or similar, to be defined).

## 3. Rationale

*   **Seamless Workflow:** Completes the intended "Conveyor Belt" flow, reducing manual steps and potential for errors.
*   **Improved Traceability:** Ensures that the "How" (spec) is directly linked to the "What" (backlog item) and "Why" (ADR).
*   **Increased Efficiency:** Automates the tedious process of copying and pasting information between document types.
*   **Consistency:** Promotes a consistent structure and content for `spec` documents.

## 4. Consequences

- Requires modifications to the `assemblage/commands/new.py` module.
- New parsing logic will be needed to extract acceptance criteria from backlog item Markdown files.
- The generated `spec` template will need to be carefully designed.
- The `control_plane new` command will become more powerful and central to the workflow.
