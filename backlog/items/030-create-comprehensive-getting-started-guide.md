# ITEM-030: Create Comprehensive Getting Started Guide

**Date Created:** 2025-11-22
**Status:** Not Started
**Priority:** High
**Owner:** Architect

## 1. Description

Create a Comprehensive Getting Started Guide document that consolidates all necessary information for installing, configuring, and initially using the Assemblage, as defined in `ADR-023`.

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-023-comprehensive-getting-started-guide.md`

## 3. "What" (Acceptance Criteria)

- [ ] A new Markdown document (e.g., `docs/GETTING_STARTED.md`) is created.
- [ ] The guide clearly lists all prerequisites (Git, Python, pip).
- [ ] It provides step-by-step instructions for cloning the repo, initial dependency installation, and git hook setup.
- [ ] It includes instructions for running the onboarding protocol (or automated onboarding command).
- [ ] It introduces core Assemblage concepts (Control Plane, Conveyor Belt, ADRs, Backlog Items, Specs, Nudges, Feedback).
- [ ] It demonstrates basic `control_plane` commands (`index`, `query`, `status`).
- [ ] It explains the purpose of main configuration files (`config/*.yml`).
- [ ] It includes a basic troubleshooting section.
- [ ] It informs users about the automatic SentenceTransformer model download.

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/comprehensive-getting-started-guide/spec.md`
