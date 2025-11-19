# Specification: Code Query System

This document provides the detailed technical blueprint for `ITEM-015`, implementing the Code Query System as defined in `ADR-009`.

## 1. New Dependencies

The `requirements.txt` file must be updated to include the new libraries:
```
# Code Intelligence
sentence-transformers
faiss-cpu
```

## 2. New Module: `assemblage/code_search.py`

A new module will be created to encapsulate all logic for indexing and searching. This separates the core logic from the command-line interface in the Control Plane.

### 2.1. Constants
- `INDEX_DIR = Path(".assemblage_cache")`
- `INDEX_PATH = INDEX_DIR / "code_index.faiss"`
- `METADATA_PATH = INDEX_DIR / "code_index_meta.json"`
- `MODEL_NAME = 'all-MiniLM-L6-v2'`

### 2.2. Core Functions

- **`_get_all_code_files()`**:
    - Uses `pathlib.Path.glob` to find all `*.py` files in the repository.
    - Must implement logic to read and respect patterns from the `.gitignore` file to exclude ignored files and directories (like `.venv`).

- **`_split_code_into_chunks(file_path: Path, content: str)`**:
    - Takes file content as a string.
    - Uses a regular expression (`re.split`) to split the content by function or class definition lines (`^\s*def |^\s*class `). This is a simple but effective strategy for creating logical chunks.
    - For each chunk, it must store the text content, the file path, and the starting line number.
    - It will return a list of dictionaries: `[{"path": str, "line": int, "content": str}]`.

- **`build_index()`**:
    1.  Ensures the `INDEX_DIR` exists using `INDEX_DIR.mkdir(exist_ok=True)`.
    2.  Initializes the sentence transformer model: `SentenceTransformer(MODEL_NAME)`.
    3.  Calls `_get_all_code_files()` to get a list of files to index.
    4.  Iterates through each file, reads its content, and uses `_split_code_into_chunks()` to get all code chunks.
    5.  Aggregates all chunks into two lists: one with the raw text content (`chunks_content`) and one with the metadata dictionaries (`chunks_metadata`).
    6.  Generates embeddings for all `chunks_content` in a single batch: `model.encode(chunks_content)`.
    7.  Creates a new FAISS index (`faiss.IndexFlatL2`) and adds the embeddings.
    8.  Saves the index to `INDEX_PATH` using `faiss.write_index()`.
    9.  Saves the `chunks_metadata` list to `METADATA_PATH` as a JSON file.
    10. Prints clear logging messages for each major step.

- **`search_index(query_text: str, top_k: int = 5)`**:
    1.  Checks if `INDEX_PATH` and `METADATA_PATH` exist. If not, raises an error instructing the user to run `control_plane index`.
    2.  Loads the FAISS index using `faiss.read_index()`.
    3.  Loads the metadata from the JSON file.
    4.  Initializes the sentence transformer model.
    5.  Encodes the `query_text` into a vector.
    6.  Searches the index for the `top_k` nearest neighbors, which returns distances and indices.
    7.  Maps the returned indices back to the loaded metadata and the original code chunks to build a list of results.
    8.  Returns a list of result dictionaries, each containing: `{"score": float, "path": str, "line": int, "content": str}`.

## 3. Control Plane Modifications (`assemblage/control_plane.py`)

- **Imports:** Add `from assemblage import code_search`.
- **New Handlers:**
    - `index_command(args)`: Prints a status message and calls `code_search.build_index()`.
    - `query_command(args)`: Calls `code_search.search_index(args.query)`. It then iterates through the results and formats them into the human-readable Markdown report specified in `ADR-009`, including confidence scores, file paths, line numbers, and formatted code snippets.
    - `status_command(args)`: If `args.index` is True, it will check for the existence of `INDEX_PATH`, report its last modification time, and the number of items in the corresponding metadata file.
- **`argparse` Setup:**
    - Add the `index` sub-parser.
    - Add the `query` sub-parser with a required `query` argument.
    - Add the `status` sub-parser with an optional `--index` flag.

## 4. Post-Commit Hook (`.pre-commit-config.yaml`)

- A new `post-commit` hook will be added.
- **For simplicity and safety (as per `ADR-009`), the MVP of this hook will trigger a full re-index.** Incremental updates are a future optimization.
- The hook will run the command: `python -m assemblage.control_plane index`.

```yaml
# Add to .pre-commit-config.yaml
-   repo: local
    hooks:
    -   id: reindex-codebase
        name: Re-index Codebase
        stages: [post-commit]
        language: system
        entry: python -m assemblage.control_plane index
        verbose: true
```

## 5. Test Design (`tests/test_code_search.py`)

- A new test file is required.
- It will use `pytest.fixture` to create a temporary directory with two mock `.py` files containing known functions.
- **`test_build_index`**: Calls `build_index()` within the temporary directory. Asserts that `INDEX_PATH` and `METADATA_PATH` are created.
- **`test_search_index`**: Builds the index, then calls `search_index()` with a query like "logic for adding numbers". Asserts that the top result correctly identifies the `def add(a, b):` function from the mock files.

This blueprint provides an exact and complete plan for the Builder.
