# Specification: Incremental Code Indexing

This document provides the detailed technical blueprint for `ITEM-022`, implementing incremental indexing for the Code Query System as defined in `ADR-015`.

## 1. State Management File

- **New File:** `.assemblage_cache/index_manifest.json`
- **Purpose:** To maintain the state of the index between runs.
- **Schema:** A JSON object mapping file paths to their metadata.
    ```json
    {
      "files": {
        "path/to/file1.py": {
          "hash": "sha256_hash_of_content",
          "faiss_ids": [0, 1, 2]
        }
      },
      "next_faiss_id": 3
    }
    ```

## 2. `code_search.py` Module Refactoring

The `build_index` function will be completely refactored. The `search_index` function will remain largely unchanged but will need to load the new `IndexIDMap` correctly.

### 2.1. New Helper Functions
- `_get_content_hash(content: str) -> str`: Takes a string, encodes it to UTF-8, and returns its SHA256 hash as a hex digest.
- `_load_state()`: Loads `index.faiss` and `index_manifest.json`. If they don't exist, it initializes a new FAISS `IndexIDMap`, an empty manifest dictionary, and sets `next_faiss_id` to 0.
- `_save_state(index, manifest)`: Saves the FAISS index and the manifest file.

### 2.2. Refactored `build_index()` Logic
The new orchestration will be:
1.  **Load State:** Call `_load_state()` to get the current index and manifest.
2.  **Scan Filesystem:** Get a `current_files_map` of all `.py` files in the repo, with file paths as keys and their new content hashes as values.
3.  **Identify Changes:**
    -   Initialize three lists: `files_to_add`, `files_to_remove`, `ids_to_remove`.
    -   **Find Deletions:** Iterate through the files in the manifest. If a file is not in `current_files_map`, add its path to `files_to_remove` and extend `ids_to_remove` with its `faiss_ids`.
    -   **Find Additions/Modifications:** Iterate through `current_files_map`. If a file is not in the manifest, or if its hash has changed, add its path to `files_to_add`. If it was a modification, also add its old `faiss_ids` to `ids_to_remove`.
4.  **Process Changes:**
    -   **Remove:** If `ids_to_remove` is not empty, call `index.remove_ids()` with the collected IDs. Then, remove the corresponding `files_to_remove` from the manifest's `files` dictionary.
    -   **Add:** For each file in `files_to_add`:
        -   Read the file, split it into chunks, and generate embeddings.
        -   Generate a new, unique range of FAISS IDs for the chunks using the `next_faiss_id` counter from the manifest.
        -   Call `index.add_with_ids()` to add the new vectors and their IDs.
        -   Update the manifest with the new file's hash and its allocated `faiss_ids`. Update the `next_faiss_id` counter.
5.  **Save State:** If any changes were made, call `_save_state()` to persist the updated index and manifest. Otherwise, print "Index is up to date."

### 2.3. FAISS Index Type Change
- The index will be changed from `IndexFlatL2` to `IndexIDMap(IndexFlatL2(...))`. This is a wrapper that maps our custom integer IDs to the internal FAISS index, which is required for the `remove_ids` operation.

## 3. Test Plan (`tests/test_code_search.py`)

The existing test file will be completely rewritten to test the new incremental logic.

- **Fixture:** A `pytest` fixture will provide a temporary directory and helper functions to create/modify/delete mock code files.
- **`test_initial_build`**: Asserts that running `build_index` for the first time correctly creates the index and a complete manifest.
- **`test_no_change_run`**: Asserts that running `build_index` a second time with no file changes results in no calls to `index.add_with_ids` or `index.remove_ids`.
- **`test_file_addition`**: Asserts that adding a new file and running `build_index` results in a call to `index.add_with_ids` and updates the manifest correctly.
- **`test_file_deletion`**: Asserts that deleting a file and running `build_index` results in a call to `index.remove_ids` and removes the file from the manifest.
- **`test_file_modification`**: Asserts that changing a file and running `build_index` results in calls to both `index.remove_ids` (for the old vectors) and `index.add_with_ids` (for the new ones), and updates the hash in the manifest.

This blueprint provides a complete and actionable plan for the Builder.
