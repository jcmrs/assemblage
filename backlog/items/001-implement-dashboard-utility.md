# ITEM-001: Implement Dashboard MVP Utility

**Date Created:** 2025-11-16
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Create a "Utility" script that generates a project status dashboard in both Markdown and JSON formats.

## 2. "Why" (The Source Material)

*This section **MUST** link to the "Anchors" (the "Source Material") that define this work. This is the "Nudge" for traceability.*

* **Decision (The "Why"):**
    * `decisions/ADR-002-dashboard-mvp.md`
* **Product Definition (The "What"):**
    * N/A (This is a "How" / Platform feature)
* **Originating Idea (The "Spark"):**
    * `ideas/001-ai-first-dashboard.md`

## 3. "What" (Acceptance Criteria)

*A simple checklist of what "Done" looks like for this item. This is what the "Architect" workbench must fulfill.*

- [ ] A new script is created at `tools/generate-dashboard.sh`.
- [ ] The script is executable (`chmod +x`).
- [ ] When run, the script generates a `STATUS.md` file in the project root with the agreed-upon format.
- [ ] When run, the script generates a `status.json` file in the project root with the agreed-upon format.
- [ ] The script's implementation follows the "Assemblage Change Protocol," which includes creating a corresponding BATS test in `tests/tools/`.
- [ ] The generated files (`STATUS.md`, `status.json`) are added to the `.gitignore` file.

## 4. "How" (Implementation Link)

*(This section is left blank by the "Explorer." The "Architect" fills this in.*)

* **Blueprint (The "How"):**
    * `specs/dashboard-utility/spec.md`
