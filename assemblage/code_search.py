"""
code_search.py

Core logic for incrementally indexing the codebase and performing semantic searches.
"""

import ast
import hashlib
import json
import subprocess
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Constants ---
INDEX_DIR = Path(".assemblage_cache")
INDEX_PATH = INDEX_DIR / "code_index.faiss"
METADATA_PATH = INDEX_DIR / "code_index_meta.json"
MANIFEST_PATH = INDEX_DIR / "index_manifest.json"
MODEL_NAME = "all-MiniLM-L6-v2"


def _get_content_hash(content: str) -> str:
    """Returns the SHA256 hash of a string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _load_state():
    """Loads the index, metadata, and manifest from disk."""
    print("INFO: Loading existing index state...")
    if (
        not INDEX_PATH.exists()
        or not METADATA_PATH.exists()
        or not MANIFEST_PATH.exists()
    ):
        print("INFO: No existing index found. Initializing new index.")
        # Get model dimension
        model = SentenceTransformer(MODEL_NAME)
        dimension = model.get_sentence_embedding_dimension()
        # Create a new FAISS index that supports ID mapping
        index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
        metadata = {}
        manifest = {"files": {}, "next_faiss_id": 0}
        return index, metadata, manifest

    index = faiss.read_index(str(INDEX_PATH))
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    return index, metadata, manifest


def _save_state(index, metadata, manifest):
    """Saves the index, metadata, and manifest to disk."""
    print("INFO: Saving new index state...")
    INDEX_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def _get_all_code_files():
    """Gets all .py files in the repo, respecting .gitignore."""
    cmd = ["git", "ls-files", "*.py"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return {Path(p) for p in result.stdout.strip().split("\n") if p}


def _split_code_into_chunks(file_path: Path, content: str):
    """
    Splits code into chunks using an Abstract Syntax Tree (AST).
    Each top-level function and class is considered a chunk.
    """
    chunks = []
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        print(f"WARNING: Skipping {file_path} due to syntax error: {e}")
        return []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            # ast.get_source_segment might not exist in all versions or might fail
            try:
                source_segment = ast.get_source_segment(content, node)
            except (TypeError, ValueError):
                # Fallback for older versions or edge cases
                source_segment = None

            if source_segment:
                chunks.append(
                    {
                        "path": str(file_path),
                        "line": node.lineno,
                        "content": source_segment,
                    }
                )
    return chunks


def build_index():
    """Builds or updates the FAISS index incrementally."""
    print("INFO: Starting incremental index build...")
    index, metadata, manifest = _load_state()
    model = SentenceTransformer(MODEL_NAME)

    current_files = _get_all_code_files()
    manifest_files = set(Path(p) for p in manifest["files"].keys())

    # --- Identify Changes ---
    files_to_add = []
    ids_to_remove = []

    deleted_files = manifest_files - current_files
    for file_path in deleted_files:
        file_str = str(file_path)
        if file_str in manifest["files"]:
            ids_to_remove.extend(manifest["files"][file_str]["faiss_ids"])
            del manifest["files"][file_str]
            print(f"INFO: File deleted: {file_str}")

    files_to_check = current_files - deleted_files
    for file_path in files_to_check:
        file_str = str(file_path)
        try:
            content = file_path.read_text(encoding="utf-8")
            content_hash = _get_content_hash(content)
            if (
                file_str not in manifest["files"]
                or manifest["files"][file_str]["hash"] != content_hash
            ):
                files_to_add.append((file_path, content, content_hash))
                if file_str in manifest["files"]:
                    ids_to_remove.extend(manifest["files"][file_str]["faiss_ids"])
                    print(f"INFO: File modified: {file_str}")
                else:
                    print(f"INFO: New file found: {file_str}")
        except Exception as e:
            print(f"WARNING: Could not process file {file_path}: {e}")

    # --- Process Changes ---
    if not files_to_add and not ids_to_remove:
        print("INFO: Index is up to date.")
        return

    if ids_to_remove:
        print(f"INFO: Removing {len(ids_to_remove)} old vectors from index...")
        index.remove_ids(np.array(ids_to_remove, dtype=np.int64))
        # Also remove from metadata
        ids_to_remove_set = set(ids_to_remove)
        for key in list(metadata.keys()):
            if int(key) in ids_to_remove_set:
                del metadata[key]

    if files_to_add:
        next_id = manifest["next_faiss_id"]

        for file_path, content, content_hash in files_to_add:
            chunks = _split_code_into_chunks(file_path, content)
            if not chunks:
                continue

            print(
                "INFO: Generating embeddings for "
                f"{len(chunks)} chunks in {file_path}..."
            )
            embeddings = np.array(model.encode([c["content"] for c in chunks]))

            if embeddings.ndim == 1:  # Handle case of single chunk
                embeddings = np.atleast_2d(embeddings)

            faiss_ids = list(range(next_id, next_id + len(chunks)))

            print(f"INFO: Adding {len(chunks)} new vectors to index...")
            index.add_with_ids(embeddings, np.array(faiss_ids, dtype=np.int64))

            for i, chunk in enumerate(chunks):
                chunk_id = faiss_ids[i]
                metadata[str(chunk_id)] = chunk

            manifest["files"][str(file_path)] = {
                "hash": content_hash,
                "faiss_ids": faiss_ids,
            }
            next_id += len(chunks)

        manifest["next_faiss_id"] = next_id

    _save_state(index, metadata, manifest)
    print("INFO: Index build complete.")


def search_index(query_text: str, top_k: int = 5):
    """Searches the index for a given query."""
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Index not found. Please run 'control_plane index' first."
        )

    print("INFO: Loading code intelligence index...")
    index = faiss.read_index(str(INDEX_PATH))
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    model = SentenceTransformer(MODEL_NAME)
    query_vector = model.encode([query_text])
    distances, indices = index.search(query_vector, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        # The indices returned by search are the FAISS IDs
        meta_key = str(idx)
        if meta_key in metadata:
            meta = metadata[meta_key]
            results.append(
                {
                    "score": float(distances[0][i]),
                    "path": meta["path"],
                    "line": meta["line"],
                    "content": meta["content"],
                }
            )
    return results
