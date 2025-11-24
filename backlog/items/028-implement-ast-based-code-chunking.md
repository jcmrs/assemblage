# ITEM-028: Implement AST-based Code Chunking

**Date Created:** 2025-11-22
**Status:** Not Started
**Priority:** High
**Owner:** Architect

## 1. Description

Refactor the `_split_code_into_chunks` function in `assemblage/code_search.py` to utilize an Abstract Syntax Tree (AST)-based approach for chunking Python code, as defined in `ADR-021`.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-021-ast-based-code-chunking.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `_split_code_into_chunks` function is refactored to use Python's `ast` module.
- [ ] The function correctly identifies and extracts full code segments for classes, functions, and methods, including decorators and docstrings.
- [ ] Each extracted chunk represents a semantically coherent unit of code.
- [ ] The existing `build_index` and `search_index` functions continue to operate correctly with the new chunking mechanism.
- [ ] Comprehensive unit tests are created for the new AST-based chunking logic, covering various Python code structures.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/ast-based-code-chunking/spec.md`
