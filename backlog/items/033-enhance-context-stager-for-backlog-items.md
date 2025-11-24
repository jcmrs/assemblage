# ITEM-033: Enhance Context Stager for Backlog Items

**Date Created:** 2025-11-22
**Status:** Not Started
**Priority:** High
**Owner:** Architect

## 1. Description

Enhance the `control_plane new --type item` command to create more self-contained and context-rich backlog items, as defined in `ADR-026`. This is a **Context Engineering** initiative, involving richer "Why" integration from the parent ADR and guided "What" generation for acceptance criteria.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-026-enhance-context-stager-for-backlog-items.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `control_plane new --type item` command is modified to extract a concise summary of the parent ADR's "Context" and "Decision" sections.
- [ ] This summary is embedded directly into the new backlog item's "Description" or a dedicated "Why" section.
- [ ] The command actively guides the user (or System Owner) in defining comprehensive and granular "Acceptance Criteria" for the backlog item.
- [ ] The `backlog/items/TEMPLATE.md` is updated to reflect this richer structure.
- [ ] Comprehensive unit tests are created for the enhanced `control_plane new` command, verifying context extraction and integration.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/enhance-context-stager-for-backlog-items/spec.md`
