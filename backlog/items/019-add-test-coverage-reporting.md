# ITEM-019: Add Test Coverage Reporting

**Date Created:** 2025-11-19
**Status:** Ready for Architect
**Priority:** Medium
**Owner:** Architect

## 1. Description

Integrate `pytest-cov` into the project to generate and display test coverage reports, as defined in `ADR-012`.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-012-test-coverage-reporting.md`

## 3. "What" (Acceptance Criteria)

- [ ] `pytest-cov` is added to `requirements.txt`.
- [ ] The `validate` command in `config/commands.yml` is updated to include a `--coverage` flag.
- [ ] The `assemblage/commands/validate.py` module is updated to run `pytest --cov` when the `--coverage` flag is present and display the results.
- [ ] The `run-assemblage-tests.sh` script is updated to generate a coverage report by default.
- [ ] A new test is added to `tests/commands/test_validate.py` to ensure the `--coverage` flag correctly triggers the coverage run.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/test-coverage-reporting/spec.md`
