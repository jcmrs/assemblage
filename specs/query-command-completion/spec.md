# Specification: Query Command Content Retrieval

This document provides the detailed technical blueprint for `ITEM-016`, which is a bug fix to complete the `control_plane query` command.

## 1. Objective

To modify the Code Query System to store, retrieve, and display the actual code content for each search result, fulfilling the original design goal in `ADR-009`.

## 2. Component Design & Implementation Steps

### Step 1: Modify `assemblage/code_search.py`

The core logic module needs to be updated to handle the content.

1.  **`build_index()` function:**
    *   **Change:** When iterating through code chunks, the metadata dictionary appended to `all_chunks_metadata` must now include the content.
    *   **From:** `{"path": chunk["path"], "line": chunk["line"]}`
    *   **To:** `{"path": chunk["path"], "line": chunk["line"], "content": chunk["content"]}`

2.  **`search_index()` function:**
    *   **Change:** When building the `results` list, the function must now retrieve the "content" field from the loaded metadata and place it in the result dictionary.
    *   **From:** `"content": "Content not retrieved in this version."`
    *   **To:** `"content": meta["content"]`

### Step 2: Modify `assemblage/control_plane.py`

The command handler needs to be updated to display the content.

1.  **`query_command()` function:**
    *   **Change:** The loop that prints results must be updated to include the formatted code block.
    *   **Action:** Uncomment and activate the line that prints the content:
        ```python
        print(f"```python\n{res['content']}\n```")
        ```

### Step 3: Update `tests/test_code_search.py`

The tests must be updated to assert the new behavior.

1.  **`test_search_index()` function:**
    *   **Change:** The final assertion must be updated to check for the actual code content.
    *   **From:** `assert top_result["content"] == "Content not retrieved in this version."`
    *   **To:** A new assertion that checks if a key part of the expected function's code is in the result, for example: `assert "return a - b" in top_result["content"]`.

### Step 4: Validation

1.  Run the updated test suite in `tests/test_code_search.py` to confirm the logic is correct.
2.  After committing the code, the `post-commit` hook will automatically trigger a full re-index, which will populate the metadata file with the new content field.
3.  Manually run a `control_plane query` command to visually confirm the output matches the format specified in `ADR-009`.

This blueprint provides a precise and complete plan for the Builder to execute the fix.
