# ITEM-015: Implement Code Query System

**Date Created:** 2025-11-18
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Implement the Code Query System as a new core capability of the Control Plane, following the detailed specification in `ADR-009`. This involves creating the `index`, `query`, and `status` commands, and integrating the indexing process into our `pre-commit` workflow.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-009-code-query-system.md`
* **Idea (The "Spark"):**
    * `ideas/003-system-wide-query.md`

## 3. "What" (Acceptance Criteria)

- [ ] New dependencies (`sentence-transformers`, `faiss-cpu`) are added to `requirements.txt`.
- [ ] The Control Plane is extended with the `index`, `query`, and `status --index` commands.
- [ ] The `index` command successfully scans the codebase, generates embeddings, and saves a FAISS index file to disk (e.g., in a `.assemblage_cache/` directory).
- [ ] The `query` command takes a string, performs a semantic search, and prints a formatted, human-readable report of the top results, as shown in the `ADR-009` example.
- [ ] The `status --index` command correctly reports on the existence, date, and size of the index file.
- [ ] The `.pre-commit-config.yaml` is updated with a new `post-commit` hook that triggers an incremental re-indexing of changed files.
- [ ] A new test file (`tests/test_code_query.py` or similar) is created with unit tests for the indexing and querying logic, using a small, controlled set of mock code files.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/code-query-system/spec.md`
