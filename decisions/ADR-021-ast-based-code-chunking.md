# ADR-021: AST-based Code Chunking

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Code Query System currently relies on a simple regex-based approach (`_split_code_into_chunks`) to divide Python files into semantic units (functions, classes). While functional, this method is brittle and can lead to suboptimal chunking, especially for complex code structures, decorators, or nested definitions. This can negatively impact the quality and relevance of search results, as embeddings are generated for potentially poorly defined code segments. Improving the semantic integrity of code chunks is crucial for enhancing the accuracy of code queries.

## 2. Decision

We will refactor the `_split_code_into_chunks` function in `assemblage/code_search.py` to utilize an **Abstract Syntax Tree (AST)**-based approach for chunking Python code.

This will involve:

1.  **Parsing with `ast` module:** Use Python's built-in `ast` module to parse the code content into an AST.
2.  **Traversing the AST:** Develop logic to traverse the AST and identify key semantic units (functions, classes, methods).
3.  **Extracting Code Segments:** For each identified unit, extract its exact source code segment, including decorators and docstrings, ensuring that each chunk represents a complete and semantically meaningful block.
4.  **Metadata Enhancement:** Potentially enhance the metadata stored for each chunk to include AST-derived information (e.g., parent class, function arguments).

## 3. Rationale

*   **Improved Semantic Accuracy:** AST-based chunking guarantees that each code segment is a syntactically and semantically valid unit, leading to more accurate embeddings.
*   **Robustness:** Less prone to breaking due to code formatting variations or complex syntax compared to regex.
*   **Higher Search Relevance:** Better quality embeddings for semantically coherent chunks will result in more relevant search results for code queries.
*   **Foundation for Advanced Analysis:** An AST-based approach lays the groundwork for more sophisticated code analysis features in the future (e.g., dependency graphing, refactoring suggestions).

## 4. Consequences

- Requires a deeper understanding and implementation of Python's `ast` module.
- The `_split_code_into_chunks` function will become more complex.
- Potential for minor performance impact during indexing due to AST parsing, but this is offset by improved search quality and the incremental indexing (`ADR-015`).
- The metadata structure might need slight adjustments to accommodate AST-derived information.
