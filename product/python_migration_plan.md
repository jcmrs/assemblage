# Product Plan: Assemblage Automation Migration to Python

**Date:** 2025-11-16
**Status:** Defined

---

## 1. Objective

This document defines the scope and plan for migrating the Assemblage's automation and utility layer from Bash scripting to Python. This is a foundational, high-priority project to increase the stability, robustness, and maintainability of the "house," in accordance with the decision outlined in `ADR-005-python-pivot`.

---

## 2. Project Scope and Definition

This project encompasses a full migration of the development and automation environment. The end state will be a Python-native toolchain for all Assemblage utilities.

### 2.1. Core Technology Stack

As defined in `knowledge/research/python_best_practices.md`, the new stack will be:
*   **Language:** Python 3.x
*   **Dependency Management:** Pip with a `requirements.txt` file.
*   **Testing Framework:** Pytest.
*   **Code Formatter:** Black.
*   **Linter:** Ruff.
*   **Configuration:** `pyproject.toml` and a root `assemblage/` source directory.

### 2.2. Scope of Work

The migration will be executed via a series of high-priority work items.

1.  **Environment Setup:**
    *   Create the `assemblage/` source directory structure.
    *   Establish the `pyproject.toml` configuration file.
    *   Establish the `requirements.txt` file, including `pytest`, `pyyaml`, `black`, and `ruff`.
    *   Update `.gitignore` to include Python artifacts like `.venv/` and `__pycache__/`.
    *   Update the `README.md` with new setup instructions (e.g., `pip install -r requirements.txt`).

2.  **Testing Harness Implementation:**
    *   Create a core test harness using Pytest.
    *   Decommission and remove the BATS framework (submodules and `tests/run-tests.sh`).

3.  **Utility Migration:**
    *   Migrate every script in the `tools/` directory to a corresponding Python module in `assemblage/tools/`.
    *   The migration must include a corresponding Pytest test for each utility.
    *   The original Bash script will be deleted upon successful migration and validation of its Python replacement.

4.  **Git Hooks Migration:**
    *   The logic within the `.githooks/pre-commit` script will be migrated to a Python script and configured to run via the `pre-commit` framework (a Python-based git hook manager), or kept as a minimal shell script that calls the Python linter.

---

## 3. Definition of "Done"

This project will be considered "Done" when:
*   All items listed in the Scope of Work are complete.
*   There are no more `.sh` or `.bats` files remaining in the `tools/` or `tests/tools/` directories.
*   The entire test suite, run via `pytest`, passes successfully.
*   The Assemblage is fully functional using its new Python-based automation layer.
