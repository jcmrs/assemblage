"""
code_search.py

Core logic for indexing the codebase and performing semantic searches.
"""

import json
import re
import subprocess
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

# --- Constants ---
INDEX_DIR = Path(".assemblage_cache")
INDEX_PATH = INDEX_DIR / "code_index.faiss"
METADATA_PATH = INDEX_DIR / "code_index_meta.json"
MODEL_NAME = "all-MiniLM-L6-v2"


def _get_all_code_files():
    """
    Gets all .py files in the repo, respecting .gitignore.
    """
    print("INFO: Finding all Python files in the repository...")
    # Use git to list all tracked python files, which respects .gitignore
    cmd = ["git", "ls-files", "*.py"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    files = [Path(p) for p in result.stdout.strip().split("\n") if p]
    print(f"INFO: Found {len(files)} Python files to index.")
    return files


def _split_code_into_chunks(file_path: Path, content: str):
    """
    Splits code into chunks based on class/function definitions.
    """
    chunks = []
    # Split by class/def, but keep the delimiter
    split_points = re.split(r"(^\s*(?:def|class)\s)", content, flags=re.MULTILINE)

    # The first element is the content before the first class/def (imports etc.)
    # We can choose to index this or not. For now, we'll skip it.

    # Re-combine the delimiter with the following code block
    for i in range(1, len(split_points), 2):
        chunk_header = split_points[i]
        chunk_body = split_points[i + 1]
        full_chunk = chunk_header + chunk_body

        # Find line number of the chunk
        # This is an approximation but good enough for this purpose
        lines = content.splitlines()
        line_num = -1
        for idx, line in enumerate(lines):
            if line.strip().startswith(chunk_header.strip()):
                line_num = idx + 1
                break

        chunks.append({"path": str(file_path), "line": line_num, "content": full_chunk})

    return chunks


def build_index():
    """
    Builds the FAISS index and metadata for the entire codebase.
    """
    print("INFO: Building code intelligence index...")
    INDEX_DIR.mkdir(exist_ok=True)

    print(f"INFO: Initializing sentence transformer model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    all_files = _get_all_code_files()

    all_chunks_content = []
    all_chunks_metadata = []

    print("INFO: Parsing files and splitting into code chunks...")
    for file_path in all_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            chunks = _split_code_into_chunks(file_path, content)
            for chunk in chunks:
                all_chunks_content.append(chunk["content"])
                all_chunks_metadata.append(
                    {
                        "path": chunk["path"],
                        "line": chunk["line"],
                        "content": chunk["content"],
                    }
                )
        except Exception as e:
            print(f"WARNING: Could not process file {file_path}: {e}")

    if not all_chunks_content:
        print("WARNING: No code chunks found to index.")
        return

    print(f"INFO: Generating embeddings for {len(all_chunks_content)} code chunks...")
    embeddings = model.encode(all_chunks_content, show_progress_bar=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print(f"INFO: Saving FAISS index to {INDEX_PATH}...")
    faiss.write_index(index, str(INDEX_PATH))

    print(f"INFO: Saving metadata to {METADATA_PATH}...")
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks_metadata, f)

    print("INFO: Index build complete.")


def search_index(query_text: str, top_k: int = 5):
    """
    Searches the index for a given query.
    """
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Index not found. Please run 'control_plane index' first."
        )

    print("INFO: Loading code intelligence index...")
    index = faiss.read_index(str(INDEX_PATH))
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"INFO: Initializing sentence transformer model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    print(f"INFO: Encoding query: '{query_text}'")
    query_vector = model.encode([query_text])

    print(f"INFO: Performing search for top {top_k} results...")
    distances, indices = index.search(query_vector, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            meta = metadata[idx]
            results.append(
                {
                    "score": float(distances[0][i]),
                    "path": meta["path"],
                    "line": meta["line"],
                    "content": meta["content"],
                }
            )

    return results
