# ADR-010: Context Staging System

**Date:** 2025-11-19
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

Our "Conveyor Belt" workflow requires the creation of several standardized documents (ADRs, Items, Specs). This is currently a manual, error-prone process. A previous proposal to use simple templating (`ADR-010-intelligent-boilerplate-generation.md`, now deleted) was rejected as too rigid and insufficient. It failed to address the core challenge, which is not file creation, but the management of *cognitive context* for the AI System Owner as it moves between workbenches. A truly AI-First system must not just create a file; it must "set the stage" for the subsequent task.

## 2. Decision

We will implement a **"Context Staging System"** as a new core capability of the Control Plane. This system replaces the naive "boilerplate generation" idea with a more sophisticated, workflow-aware process.

The system will be exposed via a `control_plane new` command and will be governed by these principles:

1.  **It is a Context Assembler:** Its primary role is to gather and synthesize information from parent documents in the workflow chain (e.g., reading an ADR and Product Definition to create a Backlog Item).
2.  **It is a Dynamic Prompt Generator:** Its primary output is not a file, but a **"Task Briefing"** presented directly to the AI. This briefing will contain the synthesized context and a clear directive for the upcoming task, effectively acting as a master prompt.
3.  **It is a File Provisioner:** As a secondary effect of this process, it will create the necessary file (`.md`) in the correct directory, with the correct name, and containing the relevant boilerplate and synthesized context.
4.  **It is Extensible:** The templates and logic for assembling context for each document type will be managed in a clear and extensible way (e.g., in a dedicated `assemblage/stages/` module or similar).

## 3. Rationale

This decision represents a significant leap in the maturity of our Assemblage.

*   **True AI-First Design:** This system is designed explicitly to manage and optimize the AI's cognitive state, reducing context-switching costs and preparation time.
*   **Holistic System Thinking:** The system is aware of the entire "Conveyor Belt" workflow and the relationships between its stages, rather than treating each file as an isolated artifact.
*   **Enhanced Workflow Integrity:** By automating the synthesis of information, it ensures no critical context is lost as a project moves from "Why" to "What" to "How."
*   **Adaptability:** By focusing on the *process* of context assembly rather than static templates, the system is inherently more flexible and adaptable to future changes in our workflow.

## 4. Example Workflow

1.  **Command:** `> python -m assemblage.control_plane new --type spec --from-item 017`
2.  **Internal Action (Context Assembly):**
    *   The system reads `backlog/items/017...md`.
    *   It finds the link to `decisions/ADR-010...md` within that file and reads it.
3.  **Internal Action (File Provisioning):**
    *   The system creates a new file at `specs/017-some-title/spec.md`.
4.  **Output (Dynamic Prompt Generation / "Task Briefing"):**
    *   The system presents a formatted summary to the AI, including synthesized context from the ADR and the Item, and a clear directive to begin the Architect's work.

## 5. Consequences

- This is a more complex and ambitious feature than the original templating idea, but it provides exponentially more value.
- It will require a dedicated module for managing the logic of each "Stage" in our workflow.
- It solidifies the Control Plane's role as the central orchestrator of all high-level workflows in the Assemblage.
