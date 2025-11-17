# ITEM-001: Establish Python Project Environment

**Date Created:** 2025-11-16
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Establish the foundational directory structure, configuration files, and dependencies for the new Python-based automation layer.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new top-level directory `assemblage/` is created.
- [ ] An empty `assemblage/__init__.py` file is created.
- [ ] A `pyproject.toml` file is created in the root with basic project metadata and configurations for `black` and `ruff`.
- [ ] A `requirements.txt` file is created in the root, containing `pytest`, `pyyaml`, `black`, and `ruff`.
- [ ] The `.gitignore` file is updated to ignore `.venv/`, `__pycache__/`, and `*.pyc` files.
- [ ] The BATS-related Git submodules (`tests/libs/`) are properly decommissioned and removed from the repository.
- [ ] The `README.md` is updated with new, clear instructions for setting up the Python environment (e.g., "Create a virtual environment, then run `pip install -r requirements.txt`").

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/python-environment/spec.md`
