# ITEM-020: Implement Structured Feedback Channel

**Date Created:** 2025-11-19
**Status:** Ready for Architect
**Priority:** High
**Owner:** Architect

## 1. Description

Implement the "Structured Feedback Channel" as the `feedback` command on the Control Plane, following the detailed specification in `ADR-013`.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-013-structured-feedback-channel.md`
* **Idea (The "Spark"):**
    * `ideas/005-structured-feedback-channel.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new `feedback/` directory is created.
- [ ] A new `control_plane feedback` command is implemented and registered in `config/commands.yml`.
- [ ] The command takes a `--commit` hash as a required argument.
- [ ] **Phase 1:** The command first generates and saves an `ai_self_report` section to a new YAML file in `feedback/`. This report must contain objective data about the specified commit (e.g., files changed, lines added/deleted).
- [ ] **Phase 2:** The command then interactively prompts the Vision Owner for the subjective review fields (`clarity_rating`, `positive_notes`, etc.).
- [ ] The final YAML file in `feedback/` is updated to contain both the `ai_self_report` and `vision_owner_review` sections.
- [ ] A new test file is created to validate the entire two-phase process, including the self-reporting logic and the interactive prompting.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/structured-feedback-channel/spec.md`
