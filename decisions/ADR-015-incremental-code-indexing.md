# ADR-015: Incremental Code Indexing

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Code Query System (`ADR-009`) currently re-indexes the entire codebase on every commit. While functional, this is an inefficient MVP solution that will lead to significant performance degradation as the codebase grows. Each commit will trigger a time-consuming process that is redundant for unchanged files. This is a critical architectural weakness that must be addressed to ensure the long-term viability of the system.

## 2. Decision

We will refactor the Code Query System to support **Incremental Indexing**.

1.  **Index Manifest:** A new manifest file (e.g., `.assemblage_cache/index_manifest.json`) will be created to track the state of the index. This file will store a mapping of indexed file paths to a hash of their content.
2.  **Modified `index` Logic:** The `index` command (and by extension, the `post-commit` hook that calls it) will be updated:
    *   On run, it will first scan for all eligible code files.
    *   For each file, it will calculate a content hash.
    *   It will compare this hash to the one stored in the manifest.
    *   **Add/Update:** If a file is new or its hash has changed, its content will be chunked, embedded, and the corresponding vectors will be added or updated in the FAISS index. The manifest will be updated with the new hash.
    *   **Delete:** If a file is present in the manifest but no longer exists in the codebase, its corresponding vectors will be removed from the FAISS index (FAISS supports removal by ID). The file will be removed from the manifest.
    *   **No Change:** If the hash is unchanged, the file will be skipped.

## 3. Rationale

*   **Performance & Scalability:** This is the primary driver. Changing one file should be a near-instantaneous indexing operation, not a multi-minute full re-build. This ensures the system remains fast and responsive, even for very large codebases.
*   **Efficiency:** Drastically reduces redundant computation and I/O, saving CPU cycles and energy.
*   **Architectural Maturity:** Moves the Code Query System from a "proof-of-concept" to a robust, production-grade feature.

## 4. Consequences

- This is a significant refactoring of the `code_search.py` module.
- The logic for managing the FAISS index becomes more complex, as it now requires handling additions, updates, and deletions rather than just bulk loading.
- A new manifest file is introduced, which becomes a critical part of the system's state.
