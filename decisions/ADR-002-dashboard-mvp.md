# ADR-002: Project Dashboard MVP

**Date:** 2025-11-16
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
* **"Why" decisions** relate to strategic goals, purpose, and the definition of success.
* **"How" decisions** relate to technical implementation, architecture, tools, and processes.

**Vision Owner Concurrence (Human Partner):** Yes
* *Does this decision align with the strategic "Why" and purpose of the project?*

**System Owner Concurrence (AI Partner):** Yes
* *Is this decision a sound, efficient, and sustainable part of the technical "How" (the platform)?*

---

## Context

The project requires a dashboard to provide at-a-glance status for both the System Owner (AI) and the Vision Owner (Human). The System Owner needs to quickly assess the health and integrity of the Assemblage ("The House"). The Vision Owner needs high-level visibility into the progress of the Product ("The Furniture"). The solution must serve both needs while being efficient and extensible.

## Decision

We will create a new "Utility" script at `tools/generate-dashboard.sh`. When executed, this script will generate two files in the project's root directory:

1.  **`STATUS.md`**: A human-readable Markdown file presenting a formatted status report. It will include Assemblage health, version, project flow metrics (counts of ideas, backlog items, specs), and recent activity.
2.  **`status.json`**: A machine-readable JSON file containing the same data in a structured format.

These two generated files will be added to `.gitignore` to prevent them from being committed to version control.

## Rationale

This two-file approach effectively serves both owners and aligns with our core principles:

*   **Serves the Symbiotic Partnership:** `STATUS.md` provides a simple, accessible view for the Vision Owner. `status.json` provides a structured data source for the System Owner and enables future automation and more advanced UIs.
*   **Enables Future Extensibility:** The `status.json` file acts as a stable data source (an API). This allows us to easily build a more sophisticated, graphical web-based dashboard in the future without changing the data-gathering logic.
*   **Low Cost, High Value:** The cost of generating two small text files is negligible, but it provides maximum utility and future-proofs the solution.

## Consequences

### Positive
- Provides immediate, at-a-glance status for both partners.
- Reduces the System Owner's cognitive load during session startup.
- Creates a data source (`status.json`) for future, more advanced dashboard UIs.
- Formally establishes the key performance indicators (KPIs) for platform health and project progress.

### Negative
- None identified for this MVP.

### Neutral
- Adds two new files to the `.gitignore` list.

## Alternatives Considered

- **Markdown Only:** This was rejected because it would not provide a structured data source for future automation or a potential web UI. It would be less "AI-First."
- **JSON Only:** This was rejected because it would be less immediately readable for the non-technical Vision Owner.
- **A full web-based UI:** This was deferred as it is too complex for an MVP. The current approach allows us to deliver value immediately while paving the way for a web UI in a future iteration.

## Foundation Alignment

### Imperative 0: Symbiotic Partnership
- [X] Explicitly defines "Why" vs. "How" ownership by providing tailored outputs for each partner.
- [X] Both partners have given concurrence for their domain.

### Imperative 1: Holistic System Thinking
- [X] Considered "ripple effects" by planning for a future web UI, ensuring the current work is a foundation for it.

### Imperative 2: AI-First
- [X] Enables System Owner (AI) autonomy by automating status gathering.
- [X] Preserves context in Process Memory by creating this ADR.

### Imperative 3: The Five Cornerstones
- [X] **Modularity:** The dashboard utility is a distinct, single-responsibility component.
- [X] **Extensibility:** The JSON output is explicitly designed for future extensions (like a web UI).
- [X] **Automation:** The entire process is automated via the `tools/generate-dashboard.sh` Utility.

## Related Decisions

- None.

## Implementation Notes

- The script must gather data from `tools/validate-assemblage.sh`, `ASSEMBLAGE.version`, `git log`, and by counting files in `ideas/`, `backlog/items/`, and `specs/`.
- The script must have a corresponding BATS test as per the `utility-test-protocol.md`.

## Follow-up Actions

- [X] Create a backlog item for the implementation of `tools/generate-dashboard.sh`.
- [ ] Move to the Architect workbench to design the script.
