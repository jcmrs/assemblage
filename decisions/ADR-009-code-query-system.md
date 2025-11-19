# ADR-009: Code Query System

**Date:** 2025-11-18
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

Following the great architectural refactoring (`ADR-007`), our codebase is no longer a collection of disparate scripts but is highly consolidated within `assemblage/control_plane.py`. The challenge for the System Owner (AI) has shifted from *discovering* the location of logic to rapidly *comprehending* the correct section of logic within a large, critical file. The existing text-based search tools are insufficient for this task, as they lack semantic understanding. To enhance the AI's Holistic System Thinking imperative, a more advanced code intelligence tool is required.

## 2. Decision

We will implement a **Code Query System** as a new, core capability of the Assemblage Control Plane. This system will enable semantic, natural-language queries against the codebase.

The system will be built on the following principles:

1.  **Multi-Command Architecture:** The capability will be exposed via a suite of commands on the Control Plane, not a single command:
    *   `control_plane index`: Manually triggers a full or incremental build of the codebase index.
    *   `control_plane query "<natural_language_query>"`: Executes a semantic search against the index.
    *   `control_plane status --index`: Reports on the status, freshness, and size of the index.

2.  **Vector-Based Semantic Search:** The core technology will be vector embeddings. The system will parse the codebase into logical chunks (e.g., functions), generate embeddings for each chunk using a sentence-transformer model, and store them in a local vector database.

3.  **AI-First, Event-Driven Indexing:** To ensure the AI's understanding of the code is always current, the index will be updated automatically. The `pre-commit` hook, upon a successful commit, will be modified to trigger an incremental re-indexing of only the files that were changed in that commit.

4.  **Transparent, Human-Readable Output:** The `query` command's output will be a formatted, human-readable report (in Markdown) to ensure the AI's analytical process is transparent to the Vision Owner.

## 3. Rationale

*   **Holistic System Thinking:** This system allows the AI to reason about the codebase conceptually, asking "what does this do?" instead of "where is this text?".
*   **AI-First:** The automatic, event-driven indexing reduces the AI's cognitive load. The AI does not need to remember to maintain its own understanding; the system does it automatically.
*   **Extensibility:** The multi-command architecture is clean and allows for future enhancements (e.g., different indexing strategies) without altering the core query interface.
*   **Bifurcated Ownership:** The clear, report-style output of the `query` command makes the AI's internal processes visible and auditable by the human partner.

## 4. Example Usage

**Building the index for the first time:**
```
> python -m assemblage.control_plane index
INFO: No existing index found. Performing full codebase scan...
INFO: Indexed 5 files, 35 code chunks. Index created successfully.
```

**Asking a question:**
```
> python -m assemblage.control_plane query "where is the git commit logic?"

## Code Query Results for: "where is the git commit logic?"

**Top 3 Results:**

---
**1. File:** `assemblage/commit_wrapper.py`
**Lines:** 35-41
**Confidence:** 0.92

```python
def main():
    # ...
    commit_command = ["git", "commit", "-m", args.message]

    # --- First Attempt ---
    print(f"{YELLOW}--- Attempting commit... ---{NC}")
    result = run_command(commit_command)
```
---
**2. File:** `assemblage/control_plane.py`
**Lines:** 35-41
**Confidence:** 0.85

```python
def _get_recent_activity(limit=5):
    """Gets the most recent Git log entries."""
    print("INFO: Fetching recent activity from Git...")
    command = ["git", "log", f"-n{limit}", "--pretty=format:%h|%s"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
```
---
```

## 5. Consequences

### New Dependencies
This project will introduce new Python dependencies, which must be added to `requirements.txt`:
1.  **`sentence-transformers`**: For generating high-quality code embeddings.
2.  **`faiss-cpu`**: A high-performance, local vector database from Facebook AI. It is chosen over other options like ChromaDB for its simplicity and lack of a client/server architecture, making it a better fit for our local-first approach.

### Risks
- **Index Freshness:** If the automatic indexing fails, the AI's understanding could become stale. The `control_plane status --index` command is designed to mitigate this by making the index's status easily verifiable.
- **Query Performance:** For very large codebases, indexing and querying could be slow. We will start with a simple implementation and can optimize later if needed.
