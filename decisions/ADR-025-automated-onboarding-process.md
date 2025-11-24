# ADR-025: Automated Onboarding Process

**Date:** 2025-11-22
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"Why" (Strategic Vision)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Assemblage currently has an "Onboarding Protocol" (`guides/SYSTEM/onboarding-protocol.md`) that guides the System Owner through its initial setup and identity anchoring. This protocol culminates in the creation of the `.assemblage_ONBOARDING_COMPLETE` file. This process is manual and relies on the System Owner (or Vision Owner) to follow a Markdown guide. For an AI-First system, a manual onboarding process is inefficient, prone to errors, and inconsistent with the goal of autonomous operation. Automating this process will streamline initial setup and ensure consistent identity anchoring.

## 2. Decision

We will implement an **Automated Onboarding Process** via a new `control_plane onboard` command.

This command will:

1.  **Interactive Guidance:** Provide an interactive, text-based walkthrough of the onboarding process.
2.  **Identity Anchoring:** Explain the System Owner's identity and relationship with the Vision Owner.
3.  **Core Mandates Review:** Briefly review the core mandates and operational guidelines.
4.  **Confirmation:** Prompt the Vision Owner for confirmation of understanding and agreement.
5.  **`ONBOARDING_COMPLETE` File Creation:** Upon successful completion and confirmation, automatically create the `.assemblage_ONBOARDING_COMPLETE` file in the repository root.
6.  **Integration:** This command will be the recommended first step after initial setup (dependency installation and git hooks setup) and will be prominently featured in the Comprehensive Getting Started Guide (`ADR-023`).

## 3. Rationale

*   **Streamlined Setup:** Automates a critical manual step, making the initial setup of the Assemblage faster and less error-prone.
*   **Consistent Onboarding:** Ensures that every instance of the System Owner undergoes the same, consistent identity anchoring process.
*   **Improved User Experience:** Provides a more interactive and engaging onboarding experience compared to reading a static Markdown file.
*   **Enhanced Autonomy:** Moves a core system setup process from manual guidance to programmatic execution.

## 4. Consequences

- Requires a new `control_plane` command and corresponding Python module.
- Involves interactive console input/output.
- The existing `onboarding-protocol.md` guide will need to be updated to reflect the existence and usage of this new command.
- The `check_onboarding_performed` tool will need to be updated to call this new command if onboarding has not been performed.
