# Idea: System-Wide Code Query Capability

## 1. Concept

To provide the System Owner (AI) with a powerful, semantic search capability that goes beyond simple text matching, in alignment with the Holistic System Thinking imperative.

## 2. Problem

Currently, answering broad questions about the codebase (e.g., "Where is versioning handled?") requires multiple, slow, and often incomplete `grep` or `search_file_content` commands. This forces a file-by-file analysis rather than a true system-level understanding.

## 3. Proposed Solution

Create a new Control Plane command, `control_plane query <natural_language_query>`.

1.  **Indexing:** Implement a background or on-demand process that reads the entire codebase (respecting `.gitignore`).
2.  For each file, it would generate vector embeddings of its content (e.g., on a per-function or per-class basis).
3.  These embeddings would be stored in a local vector database (e.g., using `faiss` or `chromadb`).
4.  **Querying:** When the `query` command is run:
    *   It generates an embedding for the natural language query.
    *   It performs a similarity search against the vector database.
    *   It returns a ranked list of the most relevant code snippets and their file paths.

## 4. Value Proposition

- **Enhances Holistic Thinking:** Allows the AI to reason about the codebase conceptually, not just textually.
- **Dramatically Speeds Up Analysis:** Reduces the time for system-wide analysis from minutes to seconds.
- **Improves Accuracy:** Uncovers connections and relevant code that simple text search would miss.
- **Unlocks New Capabilities:** Forms the foundation for more advanced code intelligence features in the future.
