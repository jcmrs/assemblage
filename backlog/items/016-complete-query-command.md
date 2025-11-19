# ITEM-016: Complete 'query' Command Content Retrieval

**Date Created:** 2025-11-19
**Status:** Ready for Architect
**Priority:** Critical

## 1. Description

This is a high-priority bug fix to complete the functionality of the `control_plane query` command. Currently, the command identifies the correct code chunk but returns a placeholder string instead of the actual code content. This item will implement the necessary changes to retrieve and display the code content.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * This work is a direct result of the Gap Analysis performed after the `ITEM-015` implementation. It addresses a functional deficit in the existing Code Query System.
* **Product Definition (The "What"):**
    * `decisions/ADR-009-code-query-system.md` (specifically, fulfilling the "Example Usage" section).

## 3. "What" (Acceptance Criteria)

- [ ] The `code_search.py` module is modified to store the raw text of each code chunk in the `code_index_meta.json` file during indexing.
- [ ] The `search_index` function is updated to retrieve and return this content in its results.
- [ ] The `query_command` in `control_plane.py` is updated to print the code content in a formatted code block, as originally envisioned in `ADR-009`.
- [ ] The existing tests in `tests/test_code_search.py` are updated to assert that the correct code content is returned by the `search_index` function.
- [ ] A full re-index is triggered after the code is committed to populate the metadata file with the new content.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/query-command-completion/spec.md`
