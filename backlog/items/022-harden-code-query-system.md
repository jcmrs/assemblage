# ITEM-022: Harden Code Query System

**Date Created:** 2025-11-22
**Status:** Not Started
**Priority:** High
**Owner:** Architect

## 1. Description

Refactor the Code Query System to support Incremental Indexing, as defined in `ADR-015`. This will improve the performance and scalability of the `index` command.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-015-incremental-code-indexing.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new `.assemblage_cache/index_manifest.json` file is used to track indexed files and their content hashes.
- [ ] The `code_search.build_index()` function is refactored to perform incremental updates.
- [ ] When a file is changed, only that file is re-indexed.
- [ ] When a file is deleted, it is removed from the index.
- [ ] When a file is unchanged, it is skipped during the indexing process.
- [ ] The `post-commit` hook now runs significantly faster for small changes.
- [ ] Tests for `code_search.py` are updated to validate the new add, update, and delete logic.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/incremental-code-indexing/spec.md`
