# ITEM-018: Implement Dynamic Tool Registration

**Date Created:** 2025-11-19
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Refactor the Control Plane into a Dynamic Command Loader, as defined in `ADR-011`. This is a major architectural refactoring to make the system truly extensible.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-011-dynamic-tool-registration.md`
* **Idea (The "Spark"):**
    * `ideas/004-dynamic-tool-registration.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new `config/commands.yml` file is created to define commands declaratively.
- [ ] The `control_plane.py` module is refactored to dynamically load commands from `config/commands.yml` at runtime.
- [ ] The logic for existing commands (`observe`, `validate`, `new`, etc.) is moved from `control_plane.py` into separate modules in a new `assemblage/commands/` directory.
- [ ] A new `control_plane list` command is implemented that displays all registered commands.
- [ ] A new `control_plane register` command is implemented that interactively adds a new command to `config/commands.yml`.
- [ ] All existing tests are refactored to work with the new decoupled architecture.
- [ ] New tests are created to validate the dynamic loading, `list`, and `register` functionalities.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/dynamic-tool-registration/spec.md`
