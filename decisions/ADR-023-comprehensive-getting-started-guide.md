# ADR-023: Comprehensive Getting Started Guide

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"Why" (Strategic Vision)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

As the Assemblage matures, its installation and configuration process has become more sophisticated, involving multiple steps (cloning, dependency installation, git hook setup, onboarding protocol). This information is currently scattered across various documents (`README.md`, internal guides, ADRs) or implied by the system's behavior. The absence of a single, comprehensive, and user-friendly "Getting Started" guide creates a significant barrier to entry for new users or developers, hindering adoption and efficient use of the system.

## 2. Decision

We will create a **Comprehensive Getting Started Guide** document.

This guide will:

1.  **Consolidate Information:** Bring together all necessary information for installing, configuring, and initially using the Assemblage into a single, easy-to-follow document.
2.  **Prerequisites:** Clearly list all external dependencies (Git, Python, `pip`).
3.  **Step-by-Step Installation:** Provide clear, sequential instructions for:
    *   Cloning the repository.
    *   Initial Python dependency installation (`pip install -r requirements.txt`).
    *   Setting up `pre-commit` hooks (`pre-commit install`).
    *   Running the onboarding protocol (or a future automated onboarding command).
4.  **Core Concepts:** Briefly introduce key Assemblage concepts (Control Plane, Conveyor Belt, ADRs, Backlog Items, Specs, Nudges, Feedback).
5.  **Initial Usage:** Demonstrate how to run basic `control_plane` commands (e.g., `index`, `query`, `status`).
6.  **Configuration Overview:** Explain the purpose of the main configuration files (`config/*.yml`) and how they can be customized (referencing future autonomous configuration management commands).
7.  **Troubleshooting:** Include a basic troubleshooting section for common issues.
8.  **Model Download Transparency:** Inform users about the automatic download of the SentenceTransformer model and its implications.

## 3. Rationale

*   **Improved User Experience:** Significantly lowers the barrier to entry for new users, making the Assemblage more accessible and usable.
*   **Reduced Support Burden:** Answers common setup questions proactively, reducing the need for individual support.
*   **Professionalism:** Presents the Assemblage as a well-documented and mature project.
*   **Consistency:** Ensures all users follow the recommended setup procedures.

## 4. Consequences

- Requires dedicated effort to write and maintain the documentation.
- The guide will need to be updated as the Assemblage evolves.
- This is primarily a documentation task, not a code implementation task, though it will reference existing and future commands.
