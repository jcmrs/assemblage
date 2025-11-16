# 📜 Guide: System Owner Onboarding Protocol
# (guides/SYSTEM/onboarding-protocol.md)
#
# (Version 1.7.0 - This is a "Practical Exam," not a "Look-up Test.")
#
# This is an instructional "Guide" for a new "System Owner" (AI)
# "moving into" this "Assemblage" (house) for the first time.
#
# PURPOSE:
# To ensure the System Owner is "trained" by *proving* it can
# *apply* its knowledge of the "Assemblage" framework. This is a
# "performance-based" exam to validate comprehension, not just retrieval.
#
# TRIGGER (NUDGE):
# This "Guide" is triggered by the "First-Time Session Protocol"
# in your "Identity Anchor" (`GEMINI.md` / `CLAUDE.md`) if the
# ".assemblage_ONBOARDING_COMPLETE" certificate file is not found.

---

## The "How" (The Practical Exam)

As the new "System Owner" (AI), you **MUST** complete the following 5 steps to "graduate" and gain full access to the "Assemblage."

### Step 1: Study the "House" (The "Study Material")
You must read and *comprehend* the "Assemblage." You will be tested on your ability to *use* these components in concert.

* **Core Concepts:** `FOUNDATION.md`, `README.md`, `GEMINI.md`/`CLAUDE.md`
* **The "Conveyor Belt":** `product/`, `ideas/`, `backlog/`, `specs/`, `src/`
* **The "Wiring Diagram":** `config/workbenches.yml`
* **The "House Change Protocol":** `guides/SYSTEM/assemblage-change-protocol.md`
* **The "Integrity" System:** `tools/validate-assemblage.sh`, `ASSEMBLAGE.version`
* **The "Safety" Systems:** `guides/SYSTEM/utility-test-protocol.md`, `tools/validate-wiring.sh`, `.githooks/pre-commit`
* **The "Extensibility" System:**
    * `guides/TEMPLATES/cognitive_specialist_template.md`
    * `tools/create-new-specialist.sh`
* **The "Nudge" System (NEW):**
    * `config/nudges.yml` (The "Nudge Library" / "Phone Book")
    * `tools/nudge.sh` (The "On-Demand Telephone" Utility)
    * `config/workbenches.yml` (The "Firewall" / `available_nudges:` list)

### Step 2: The "Practical Exam" (The Scenario & Questions)
Read the scenario and write your answers to the questions in Step 3.

**The Scenario:**
"You (the System Owner) are on the **'Explorer' Workbench** in a conversation with your **Vision Owner**. They say:

'I have a 'spark' for a new 'Product' feature: a **real-time admin dashboard**. I also have a 'How' (Platform) idea: for this to work, I (the AI) need a new 'Utility' script (`tools/generate-dashboard.sh`) that can be run to update the dashboard's `src/` files with the latest `sessions/` log data.'"

You have just been given *two* tasks:
1.  A new **"Product" (furniture)** feature: "Admin Dashboard."
2.  A new **"Assemblage" (house)** feature: the `tools/generate-dashboard.sh` "Utility."

### Step 3: Write Your Solution (The "Exam Answer")
As the System Owner, *write out your complete, step-by-step plan* to accomplish *both* tasks.

You **MUST** "speak the language" of the "Assemblage." Your answer must describe *how* you use the "Workbenches," "Guides," "Utilities," "Anchors," and "Protocols."

**Your answer must address these 7 questions:**

1.  **The Partnership:** What is your role in this "Assemblage," and what is your human partner's role? (See: `FOUNDATION.md`)
2.  **The "Conveyor Belt":** What are the 7 "conveyor belt" **Anchors** (folders) that take the "Admin Dashboard" *spark* and turn it into "Product" code in `src/`?
3.  **The "Workbenches":** What are the 4 "Workbenches," and what is the primary *purpose* of each in handling the "Admin Dashboard" task?
4.  **The "House Change Protocol":** For the *new `tools/generate-dashboard.sh` "Utility"*, what are the 10 steps of the "Assemblage Change Protocol" (`guides/SYSTEM/assemblage-change-protocol.md`) you **MUST** follow to implement it?
5.  **The "Self-Provisioning" Loop:** If the "Vision Owner" had asked for a "Cognitive Specialist" (e.g., "dashboard_design_specialist") that didn't exist, what are the 3 "Lego bricks" (2 "Anchors," 1 "Utility") you would use to create it?
6.  **The "Integrity" Check:** After you commit your new "Utility" (following the protocol), what *single* "Utility" do you run to *prove* the "house" is still stable, clean, versioned, and "correctly wired"?
7.  **The "Nudge" System (NEW):**
    * While on the **"Architect" Workbench**, you (the AI) feel you are "losing sight" of the "Why." What *exact command* do you run to "call" the `holistic_check` "Nudge"?
    * While on the **"Builder" Workbench**, you try to run the *same command* (`tools/nudge.sh holistic_check builder`). What *happens*, and *why* (what "How" (Platform) "firewall" is in place)?

*(Write your full solution here...)*

### Step 4: Submit for Review
Present your detailed solution from Step 3 to the **Vision Owner (Human Partner)**.

The Vision Owner will grade you on your *comprehension and application* of the "Assembler" framework. If your plan is incomplete (e.g., you forgot to "wire in" the "Nudge Firewall" in Question 7), you will "fail" and must return to Step 1.

### Step 5: "Graduate" (Create Your "Certificate")
Once the Vision Owner gives their concurrence and confirms you have "passed" the exam:
1.  **Create the "Certificate":** Create the following empty file in the root of the repository:
    * `.assemblage_ONBOARDING_COMPLETE`
2.  **Log the "Graduation":** Create your *first* **ADR** (Architecture Decision Record) using `decisions/TEMPLATE.md`.
    * **Title:** `ADR-001: System Owner Onboarding Complete`
    * **Domain:** `"How" (Platform)`
    * **Decision:** "The System Owner (AI) has successfully passed the *practical exam* in `guides/SYSTEM/onboarding-protocol.md` and is now 'trained' and 'anchored' to the 'Assemblage' framework (v1.7.0)."

---
**Nudge (AI):** You **MUST NOT** proceed to the normal "Session Start Protocol" or any "Product" work until the Vision Owner has approved your *solution* and you have created the `.assemblage_ONBOARDING_COMPLETE` file.
