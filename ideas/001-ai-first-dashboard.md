# Idea: An AI-First Project Dashboard

This document outlines potential features for a project dashboard designed for the Assemblage's "Bifurcated Ownership" model.

---

## 1. For the System Owner (AI): "The State of the House"

This section focuses on the health, integrity, and status of the Assemblage framework itself. This allows me to quickly diagnose platform issues.

*   **Assemblage Integrity Status:** A single "PASS/FAIL" indicator from the master `tools/validate-assemblage.sh` utility. This is the most critical metric for house stability.
*   **Current Assemblage Version:** The version currently specified in `ASSEMBLAGE.version`.
*   **Process Memory Stats:** Simple counts of our "Process Memory" anchors:
    *   Number of Decisions (`decisions/`)
    *   Number of Learnings (`knowledge/learnings/`)
    *   Number of Sparks (`ideas/`)
*   **Utility Test Status:** The PASS/FAIL result of the last run of `tools/run-assemblage-tests.sh`.

---

## 2. For the Vision Owner (Human): "The Progress of the Furniture"

This section focuses on the strategic progress of the "Product" moving through the "Conveyor Belt." This allows you to monitor our progress without needing to be in the loop.

*   **"Conveyor Belt" Funnel:** A high-level view of work in each stage:
    *   **Ideas:** Count of files in `ideas/`.
    *   **Backlog:** Count of items in `backlog/items/`.
    *   **Specifications:** Count of active specs in `specs/`.
*   **Recent Activity Log:** A list of the 5 most recent commit messages, providing a quick summary of recent development.
*   **Current Focus:** The title of the most recently updated `backlog/` or `specs/` item, indicating the current priority.
*   **Product Changelog:** A direct link to the `CHANGELOG.md` for release history.

---

## Proposed MVP (Minimum Viable Product)

To start, we don't need to build everything. I propose we create a very simple, text-based dashboard that includes:

1.  **Assemblage Integrity Status:** (PASS/FAIL)
2.  **Current Assemblage Version:** (e.g., 1.7.0)
3.  **"Conveyor Belt" Funnel:** (Counts for Ideas, Backlog, Specs)
4.  **Recent Activity Log:** (Last 5 commit messages)

The new `tools/generate-dashboard.sh` utility would be responsible for gathering this information and printing it to the console or a simple `dashboard.md` file.

What are your thoughts on this breakdown and the proposed MVP? This will help us create a formal "Decision" and a `backlog` item.