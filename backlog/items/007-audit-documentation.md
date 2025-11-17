# ITEM-007: Audit and Update All Documentation for Python Pivot

**Date Created:** 2025-11-16
**Status:** Pending
**Priority:** High
**Owner:** Architect

## 1. Description

Audit all documentation and configuration files within the Assemblage and update them to reflect the architectural pivot to a Python-based automation layer, ensuring consistency and accuracy.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-005-python-pivot.md`
* **Product Definition (The "What"):**
    * `product/python_migration_plan.md`

## 3. "What" (Acceptance Criteria)

- [ ] The `guides/SYSTEM/utility-test-protocol.md` is rewritten to describe the `Pytest` framework and best practices.
- [ ] The `guides/SYSTEM/assemblage-change-protocol.md` is updated to replace all references to Bash scripts (`.sh`) and BATS with their Python (`.py`) and Pytest equivalents.
- [ ] The `guides/SYSTEM/onboarding-protocol.md` is updated to reflect the Python-based environment in its practical exam.
- [ ] The `config/workbenches.yml` file is audited and updated to ensure all `utilities` listed reflect the new Python module paths.
- [ ] A general audit of all `.md` files is performed to find and replace any other outdated references to the old Bash framework.
- [ ] The changes are committed to the repository.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/documentation-update/spec.md`
