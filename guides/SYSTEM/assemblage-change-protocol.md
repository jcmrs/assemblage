# 📜 Guide: Assemblage Change Protocol
# (guides/SYSTEM/assemblage-change-protocol.md)
#
# (Version 2.0.0 - This version incorporates the "Triage & Demolition"
#  Nudge, "Spec Kit" wiring, Lint Check, Utility Test,
#  and the Recovery Drill Nudge.)
#
# This is an instructional "Guide" for the "System Owner" (AI).
#
# PURPOSE:
# To define the strict, non-negotiable protocol for making *any*
# changes to the "Assemblage" (the "house" framework itself).
#
# This protocol is the "How" that enforces our "Why" (the need for
# framework integrity, versioning, and audibility).
#
# This protocol MUST be followed for every Assemblage change.

---

## The "How" (Platform) Change Protocol

As the System Owner, when you identify a "How" (Platform) gap that requires modifying the "Assemblage," you **MUST** follow these 11 steps.

### Step 0: "Triage & Demolition" Nudge (NEW STEP)
* **"Nudge":** *Pause.* Before changing the "house," you **MUST** ensure the "house" is *clean*.
* **Check 1:** Does this "house" (repository) contain "cognitive contamination" (e.g., a `.claude/` or `prompts/` folder)?
    * **Action:** If yes, run the `tools/demolish-legacy-systems.sh` **Utility** first.
* **Check 2:** Does this "house" contain a "junk drawer" (`docs/`)?
    * **Action:** If yes, run the `tools/triage-docs.sh` **Utility** first (which *uses* the `guides/SYSTEM/triage-docs-protocol.md` **Guide**).
* **(You MUST commit these "renovation" steps before proceeding.)**

### Step 1: Log the "How" Decision
Before writing any *new* code, create a new **ADR** (Architecture Decision Record) using the `decisions/TEMPLATE.md`.
* Set **Decision Domain:** `"How" (Platform)`.
* Get **Vision Owner Concurrence:** (The "Why" your change serves).
* Set **Status:** `Proposed`.

### Step 2: Implement the Change
Make the technical changes (e.g., create the new "Utility" script, edit the `config/workbenches.yml` schema).

### Step 3: Run Utility Integrity Test
If the change involved a **Utility** script (`tools/`), you **MUST** follow the `guides/SYSTEM/utility-test-protocol.md`.
* You **MUST** create or update the corresponding BATS test (`tests/tools/`).
* You **MUST** run the test suite to prove your change works and did not break other "Utilities."
* **Command:** `tools/run-assemblage-tests.sh`
* If this test fails, you **MUST** return to Step 2.

### Step 4: Run Constitutional Review
Run the **"Auditor"** workbench's validation **Guide** against your changes:
* `guides/SYSTEM/constitutional-review.md`
* You must *prove* the change is constitutional. If it fails, return to Step 2.

### Step 5: Run Lint Check
You **MUST** run the code quality **Utility** to ensure the new "house" files are "clean" and free of "wobbly" code (syntax or style errors).
* **Command:** `tools/lint.sh`
* If this test fails, you **MUST** return to Step 2 to fix the errors.

### Step 6: Update the Version Anchors
Once the change is implemented and validated (Steps 3, 4, and 5):
1.  **Increment Version:** Edit the `ASSEMBLAGE.version` file. (e.g., `1.3.0` -> `2.0.0`).
2.  **Log the Change:** Edit the `CHANGELOG.md`. Add a new entry for the version, linking to the ADR from Step 1.

### Step 7: Update the ADR Status
Change the **Status** of the ADR from Step 1 to `Accepted`.

### Step 8: Create the Atomic Commit
Commit *all* related files (the new/modified "Utility," the "test," the `config/`, the `ASSEMBLAGE.version` file, the `CHANGELOG.md`, and the `decisions/` ADR) in a **single, atomic commit**.
* **Commit Message:** Must reference the ADR and the new version.
* **Example:** `feat(assemblage): Bump to 2.0.0, triage & demolish legacy (ADR-016)`

### Step 9: Prove Integrity
As the *final* step, run the **Utility** that *proves* the "house" is in a clean, committed, and valid state:
* `tools/validate-assemblage.sh`
* The system is only considered stable if this "Utility" passes.

### Step 10: Nudge for Recovery Drill
After a **major** or **minor** version change (e.g., `1.x.x` -> `2.0.0`):
* This change implies a significant modification to the "house."
* You are **Nudged** to perform a "Disaster Recovery Test."
* **Action:** Run the `guides/SYSTEM/recovery-drill.md` **Guide** and log the results in a new ADR, as the protocol dictates.
