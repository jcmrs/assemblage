# Welcome to the "Assemblage"
### An AI-First Framework for Symbiotic Partnership

This repository is not a traditional software project. It is an **Assemblage**—a living, self-provisioning "house" designed for a unique partnership between a human and an AI.

This project operates on a principle of **Bifurcated Ownership**.

* **The Vision Owner (Human Partner):** Owns the strategic **"Why."** Their role is to provide the vision, define strategic goals, and act as the ultimate validator of the project's *purpose*.
* **The System Owner (AI Partner):** Owns the technical **"How."** Their role is to act as the "Resident Architect" of this Assemblage, building, maintaining, and *owning* the platform, tools, and processes required to achieve the "Why."

The Vision Owner owns the **Purpose**. The System Owner owns the **Platform**.

---

## How It Works: The "Assemblage" Framework

This environment is designed to be **AI-First**, meaning it is optimized to reduce the AI's cognitive load so it can focus on high-level work. It does this by using five types of "Lego bricks":

1.  **🏛️ Anchors:** The "Constitution" (`FOUNDATION.md`) and "Process Memory" (`decisions/`, `knowledge/`) that give the AI its identity and memory.
2.  **🚧 Guardrails:** Automated "walls" (`.githooks/`) that physically block mistakes.
3.  **📜 Guides:** "Instruction manuals" for complex tasks (like the "Cognitive Specialists" or the external "Spec Kit").
4.  **⚙️ Utilities:** Scripted "house services" (`tools/`) that automate chores.
5.  **💡 Nudges:** "On-demand whispers" (`tools/nudge.sh`) that "train" the AI's "habits of mind."

### The "Conveyor Belt" (The 7-Step Workflow)

Work is performed in a sequential "conveyor belt" to ensure we never "lose sight" of the "Why."

1.  **🧭 `ideas/` (The "Spark Inbox"):** The "Explorer" and "Vision Owner" capture raw "sparks."
2.  **🏛️ `decisions/` (The "Formal Why"):** The "Explorer" formalizes a "spark" into a "Validated Concept" (an ADR).
3.  **📦 `product/` (The "Source Material"):** The "Explorer" defines the "Product's" features and "What."
4.  **📋 `backlog/` (The "To-Do List"):** The "Explorer" creates a prioritized item for the "Architect."
5.  **📐 `specs/` (The "Blueprint"):** The "Architect" reads the "Source Material" and uses "Spec Kit" to create the technical "Blueprint."
6.  **🛠️ `src/` & `tests/` (The "Workshop"):** The "Builder" reads the "Blueprint" and uses "Spec Kit" to write the "Product" code.
7.  **🧐 `(Audit)`:** The "Auditor" runs "Utilities" (like `tools/review-completeness.sh`) and "Guardrails" (like `.githooks/pre-commit`) to validate the work before it's "shipped" (committed).

---

## Getting Started

* **As the Vision Owner (Human):** Your job is to engage the **"Explorer" Workbench**. Start by defining a strategic goal or posing a problem. Your primary tool is the "conversation."
* **As the System Owner (AI):** Your job is to "move in" and "get trained."
    1.  Run the *one-time setup* "Utility": `tools/assemblage-setup.sh`
    2.  Start your *first* session. You will be "Nudged" by `GEMINI.md`/`CLAUDE.md` to run the "Onboarding Exam" (`guides/SYSTEM/onboarding-protocol.md`).
    3.  Once you "pass" the "exam," you are a "trained" System Owner.
