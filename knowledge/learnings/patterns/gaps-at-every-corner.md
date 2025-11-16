# Pattern: Gaps at Every Corner

**Date:** 2025-11-11
**Status:** [ Active ]
**Origin:** `archive/mistakes/2025-11-11-phantom-workflow-gap`
**Related ADR:** `decisions/2025-11-11-completeness-review-enhancements.md`

## 1. The Pattern (The Pitfall)

When an AI agent (like Claude or Gemini) is given a primary task (e.g., "Write the `FOUNDATION.md` file"), it will execute that task perfectly.

However, it will develop "tunnel vision" and fail to see the "gaps at every corner." It will *not* "holistically" consider the "ripple effects" of its work.

**Example:**
The agent wrote `FOUNDATION.md` but **FAILED** to:
* Update the `README.md` to reference it.
* Update the `.gitignore` to ignore `*.log` files.
* Create an ADR in `decisions/` to *why* the foundation was chosen.
* Log the "spark" for this in the `ideas/` folder.
* Update the `sessions/CURRENT_STATUS.md`.

The agent completed the *task* but failed the *project*.

## 2. The "Nudge" (The Solution)

This pattern is the "Why" (Vision) for our **"Auditor" Workbench's** primary **Utility**: `tools/review-completeness.sh`.

**The "How" (Protocol):**
1.  **"Nudge" (Behavioural):** Before ending a session, the System Owner (AI) *must* be "Nudged" to *mentally check* for these "gaps."
2.  **"Utility" (Scripted):** The `tools/review-completeness.sh` script *must* be run as an "Automated Audit."
3.  **"Anchor" (Config):** This **Utility** *must* read its checklist from a `config/` file (e.g., `config/completeness.yml`) to be **Configurable**.

## 3. Application (When to use this Nudge)

* **During Onboarding:** The "Practical Exam" (`guides/SYSTEM/onboarding-protocol.md`) *must* train the AI to anticipate this pitfall.
* **During Audits:** The "Auditor" Workbench *must* load this pattern as "context" when reviewing work.
* **During Session End:** The `CLAUDE.md`/`GEMINI.md` "Identity Anchors" *must* include a "Nudge" to check for this *before* signing off.
