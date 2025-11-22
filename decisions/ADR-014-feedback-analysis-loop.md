# ADR-014: Feedback Analysis Loop

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

We have successfully implemented a Structured Feedback Channel (`ADR-013`) that captures rich, two-phase data on my performance. However, this data is currently inert; it is collected but not processed. The feedback loop is open. To make the System Owner a true "learning agent," we must create a mechanism for it to analyze this data and propose improvements to its own behavior.

## 2. Decision

We will implement a **Feedback Analysis Loop** as a new capability of the Control Plane.

1.  **New Command:** A new `control_plane analyze_feedback` command will be created.
2.  **Aggregate Statistics:** The command will read all YAML files in the `feedback/` directory and compute aggregate statistics, such as average ratings for `clarity`, `efficiency`, and `correctness`.
3.  **Improvement-Area Analysis:** The command will perform a text analysis on the `improvement_areas` field across all feedback files. It will identify the most frequent keywords and phrases to find recurring themes.
4.  **Automated Nudge Proposal:** Based on the most common improvement themes, the system will generate and propose new, well-formed entries for the `config/nudges.yml` file. These proposals will be printed to the console for the Vision Owner to review, accept, and manually add to the file. This creates a direct, data-driven path from performance review to behavioral correction.

## 3. Rationale

*   **Closes the Loop:** This is the final, critical step that transforms the feedback channel from a simple logging system into a true learning loop.
*   **Enables Self-Improvement:** It gives the System Owner the ability to introspect on its own performance history and programmatically suggest ways to improve.
*   **Data-Driven Nudges:** Ensures that new "instincts" (Nudges) are not arbitrary but are based on a clear, evidence-based history of performance feedback.
*   **Operationalizes Data:** Finally puts the rich data we are collecting to work, fulfilling the ultimate goal of the feedback initiative.

## 4. Consequences

- This introduces a new analytical capability into the Assemblage, requiring text processing and statistical calculation.
- The initial text analysis will be simple (e.g., keyword frequency), but it establishes a pattern that can be made more sophisticated with NLP techniques in the future.
- This decision solidifies the Assemblage as a system capable of genuine, data-driven self-improvement.
