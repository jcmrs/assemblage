# Specification: AST-based Code Chunking

This document provides the detailed technical blueprint for `ITEM-028`, refactoring the code chunking mechanism as defined in `ADR-021`.

## 1. Core Design: AST-based Chunking

The current regex-based `_split_code_into_chunks` function in `assemblage/code_search.py` will be completely replaced with a new implementation that leverages Python's built-in `ast` module. This ensures that chunks are semantically and syntactically correct.

### `_split_code_into_chunks` Refactoring

- **Module:** `assemblage/code_search.py`
- **Function:** `_split_code_into_chunks(file_path: Path, content: str)`

**New Implementation Logic:**

1.  **Initialization:** The function will initialize an empty list, `chunks`.
2.  **AST Parsing:** It will parse the input `content` into an Abstract Syntax Tree using `ast.parse(content, filename=str(file_path))`. This will be wrapped in a `try...except SyntaxError` block to gracefully handle files with syntax errors.
3.  **Node Iteration:** The function will iterate through the top-level nodes in the `tree.body`.
4.  **Chunk Identification:** For each `node` in the body, it will check if the node is an instance of `ast.FunctionDef` or `ast.ClassDef`.
5.  **Source Segment Extraction:** If a node is a function or class definition, the function will use `ast.get_source_segment(content, node)` to extract the full, original source code for that node. This function correctly includes decorators, the signature, and the entire body of the function or class.
6.  **Chunk Creation:** A dictionary representing the chunk will be created and appended to the `chunks` list. This dictionary will contain:
    *   `path`: The string representation of `file_path`.
    *   `line`: The starting line number of the node, available from `node.lineno`.
    *   `content`: The source code segment extracted in the previous step.
7.  **Return Value:** The function will return the `chunks` list.

**Example Implementation Snippet:**
```python
# In assemblage/code_search.py
import ast

def _split_code_into_chunks(file_path: Path, content: str):
    chunks = []
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        print(f"WARNING: Skipping {file_path} due to syntax error: {e}")
        return []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            source_segment = ast.get_source_segment(content, node)
            if source_segment:
                chunks.append({
                    "path": str(file_path),
                    "line": node.lineno,
                    "content": source_segment
                })
    return chunks
```

## 2. Dependencies

This implementation relies on:
- The `ast` module, which is part of the Python standard library.
- `ast.get_source_segment()`, which is available in Python 3.8 and later. Our environment (Python 3.11) fully supports this.
- No new external dependencies are required.

## 3. Test Plan

A new test file will be created to specifically validate the new chunking logic.

- **New File:** `tests/test_code_chunking.py`
- **Strategy:** The tests will provide various Python code snippets as strings to the `_split_code_into_chunks` function and assert that the returned chunks are correct in number, content, and line number.

### Test Cases:

- **`test_simple_function`**: A single function. Assert 1 chunk is returned with the correct content.
- **`test_function_with_decorator`**: A function with one or more decorators. Assert the decorator is included in the chunk content.
- **`test_class_with_method`**: A class containing a method. Assert 1 top-level chunk is returned for the class, and its content includes the method.
- **`test_multiple_top_level_nodes`**: A file with two functions and one class. Assert 3 chunks are returned.
- **`test_file_with_imports_and_globals`**: A file with imports and global variables at the top. Assert that this non-chunkable code is ignored and only the functions/classes are chunked.
- **`test_syntax_error_file`**: A file with a syntax error. Assert that the function returns an empty list and does not crash.
- **`test_correct_line_numbers`**: Assert that the `line` number in the returned chunk metadata correctly corresponds to the `def` or `class` line.
