# ITEM-011: Refactor Git Hooks to use the 'pre-commit' Framework

**Date Created:** 2025-11-18
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Replace our custom, hybrid shell/Python pre-commit hook with the industry-standard `pre-commit` Python framework. This will make our hook management declarative and fully Python-native.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * This work is a direct result of the Gap Analysis performed after the main Python Pivot, aimed at achieving full architectural consistency.
* **Product Definition (The "What"):**
    * N/A

## 3. "What" (Acceptance Criteria)

- [ ] The `pre-commit` package is added to `requirements.txt`.
- [ ] A new `.pre-commit-config.yaml` file is created in the project root.
- [ ] The configuration file is set up to run `ruff` and `black`.
- [ ] The old `.githooks/pre-commit` file is deleted.
- [ ] The old `assemblage/tools/pre_commit_hook.py` script and its test are deleted.
- [ ] The `README.md` is updated with instructions to run `pre-commit install`.
- [ ] The new hook successfully blocks a commit if linting errors are present.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/pre-commit-refactor/spec.md`
