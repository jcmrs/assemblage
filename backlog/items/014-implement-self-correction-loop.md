# ITEM-014: Implement Self-Correction Loop

**Date Created:** 2025-11-18
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Implement a "Self-Correction Loop" for the pre-commit process, as defined in `ADR-008`. This will involve creating a wrapper script that can detect fixable hook failures, stage the fixes, and re-attempt a commit once.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-008-self-correction-loop.md`
* **Idea (The "Spark"):**
    * `ideas/002-self-correction-loop.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new Python script is created (e.g., `assemblage/git_wrapper.py`) that can take a commit message and execute `git commit`.
- [ ] The script successfully detects when a `pre-commit` hook fails but fixes files.
- [ ] Upon detection, the script automatically stages the changes using `git add`.
- [ ] The script re-attempts the commit exactly one more time.
- [ ] The script provides clear, verbose logging for every step of the process.
- [ ] **Negative Test Case:** The script does NOT enter a loop if a hook fails without fixing any files.
- [ ] The `README.md` or a new guide is updated to explain how to use the new commit wrapper.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/self-correction-spec/spec.md`
