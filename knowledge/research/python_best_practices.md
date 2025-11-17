# Research Report: Python Best Practices for the Assemblage

**Author:** `python_best_practices_specialist`
**Date:** 2025-11-16
**Status:** Completed

---

## 1. Executive Summary

To ensure the Python-based automation layer for the Assemblage is robust, maintainable, and aligns with our "AI-First" and "Project = Repository" principles, this report recommends a specific set of tools and conventions. We will use **pip with a `requirements.txt` file** for dependency management, **Pytest** for testing, and a standardized directory structure. This combination provides simplicity, power, and aligns with industry best practices.

---

## 2. Dependency Management

The goal is to have a dependency management system that is simple, declarative, and self-contained.

*   **Option A: Pip + `requirements.txt`**
    *   **Description:** This is the most standard, built-in method for managing Python dependencies. A `requirements.txt` file explicitly lists all required packages.
    *   **Pros:** Ubiquitous, simple, no extra tools needed. Aligns with "simplicity."
    *   **Cons:** Does not have robust dependency locking out-of-the-box.
*   **Option B: Poetry or Pipenv**
    *   **Description:** These are more advanced tools that manage dependencies, virtual environments, and packaging in one tool, with sophisticated dependency resolution and locking.
    *   **Pros:** Powerful, reproducible builds.
    *   **Cons:** Introduces a new, complex tool to the Assemblage, which slightly violates the "simplicity" goal.

**Recommendation:** Start with **Pip + `requirements.txt`**. The simplicity and universality make it the best choice for our current needs. We can create a virtual environment and "freeze" the dependencies to the `requirements.txt` file to ensure reproducibility.

---

## 3. Testing Framework

The testing framework must be powerful enough to validate our utilities and easy for an AI to write tests for.

*   **Option A: `unittest`**
    *   **Description:** Python's built-in, xUnit-style testing library.
    *   **Pros:** Part of the standard library, no extra dependencies.
    *   **Cons:** Boilerplate-heavy, syntax is verbose compared to modern alternatives.
*   **Option B: `pytest`**
    *   **Description:** The de facto industry standard for testing in Python.
    *   **Pros:** Simple, clean syntax; powerful features like fixtures and plugins; excellent assertion introspection. It is more "AI-First" due to its low-boilerplate nature.
    *   **Cons:** Is an external dependency.

**Recommendation:** Adopt **Pytest**. Its clean syntax and powerful features will reduce the cognitive load for the System Owner (AI) when writing tests, making it a superior choice for an "AI-First" environment.

---

## 4. Directory Structure and Conventions

A standardized structure is critical for a predictable environment.

**Recommendation:**

*   **`.venv/`:** A directory in the root to contain the Python virtual environment. This should be added to `.gitignore`.
*   **`assemblage/`:** A new top-level directory to hold all our Python source code. This will be our main Python package.
    *   **`assemblage/tools/`:** Python modules corresponding to our utilities will live here.
    *   **`assemblage/__init__.py`:** Makes the `assemblage` directory a Python package.
*   **`tests/`:** The existing top-level directory will be used for Pytest tests. Pytest will automatically discover tests here.
*   **`requirements.txt`:** A file in the root listing our Python dependencies (e.g., `pytest`).
*   **`pyproject.toml`:** A standard Python configuration file to define project metadata and tool configurations (like for `pytest` or formatters).

---

## 5. Linting and Formatting

To ensure code quality and consistency, we should use standard Python tools.

*   **Formatter: `black`**: An opinionated, deterministic code formatter. Using it removes all debate about style and ensures consistency.
*   **Linter: `flake8` or `ruff`**: A tool to check for logical errors, unused imports, and style guide violations. `ruff` is a modern, extremely fast alternative written in Rust.

**Recommendation:** Use **`black`** for formatting and **`ruff`** for linting. They can be configured in `pyproject.toml` and run as a pre-commit hook.
