# ITEM-017: Implement Context Staging System

**Date Created:** 2025-11-19
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Implement the "Context Staging System" as the `new` command on the Control Plane, following the detailed specification in `ADR-010`. This system will automate the creation of new process documents by assembling context from parent documents and generating a "Task Briefing" for the AI.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-010-context-staging-system.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new `control_plane new` command is implemented with arguments like `--type` and `--from-<type>`.
- [ ] A new, dedicated module (e.g., `assemblage/stager.py`) is created to house the logic for context assembly.
- [ ] The system can correctly parse parent documents (e.g., an ADR) to extract key information.
- [ ] The system correctly provisions a new, sequentially-numbered file in the correct directory.
- [ ] The system's primary output is a formatted "Task Briefing" printed to the console, containing synthesized context and a clear directive for the next task.
- [ ] A new test file is created to validate the entire end-to-end process for at least one document type (e.g., creating an `item` from an `adr`).

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/context-staging-system/spec.md`
