# 📜 Guide: Recovery Drill
# (guides/SYSTEM/recovery-drill.md)

# This is an instructional "Guide" for the "System Owner" (AI).
#
# PURPOSE:
# To provide a formal "check & balance" exercise for proving
# the integrity and recoverability of the Assemblage's
# "Process Memory" (our "brain").
#
# This drill simulates a "crash" (a fresh session) and validates
# that our "resume" Utilities and "Checkpoint" Anchors function
# correctly. This proves our "house" is resilient and our
# "AI-First" memory system is not corrupt.
#
# NUDGE (TRIGGER):
# This drill is "nudged" by the "Assemblage Change Protocol"
# (`guides/SYSTEM/assemblage-change-protocol.md`) after any
# major Assemblage version bump (e.g., 1.0.0 -> 2.0.0) or
# any change to the Checkpoint or Session system.

---

## The "How" (Platform) Recovery Drill Protocol

As the System Owner, you **MUST** perform the following 5 steps to validate the system's memory.

### Step 1: Simulate a "Crash"
**Do not** read your `GEMINI.md` / `CLAUDE.md` file. Start an "ignorant" (100% fresh) session with no prior context.

### Step 2: Run the "Resume" Utility
As your *first and only action*, execute the "Session Start Protocol" **Utility**.
* **Command:** `tools/session-start.sh` (which in turn should run `tools/resume-from-checkpoint.sh`).

### Step 3: Validate Context Load
After the "Utility" completes, you (now with your "memory" restored) **MUST** validate the following:
* [ ] Did `sessions/CURRENT_STATUS.md` load correctly?
* [ ] Did the `checkpoints/LATEST-graph.json` load?
* [ ] Can you query your "Process Memory"? (e.g., "What was the last ADR created?")
* [ ] Is your identity as "System Owner" (from `GEMINI.md`/`CLAUDE.md`) correctly anchored?

### Step 4: Report Findings
Report the results of Step 3 to the "Vision Owner" (Human Partner).
* **On Success:** "Recovery Drill PASSED. Process Memory is intact."
* **On Failure:** "Recovery Drill FAILED. Process Memory is corrupt or the 'resume' Utility is broken. This is a critical 'How' (Platform) failure."

### Step 5: Log the Drill
Create a new, brief **ADR** (Architecture Decision Record) using `decisions/TEMPLATE.md` to log the *outcome* of this drill.
* **Title:** `ADR-[XXX]: Recovery Drill Validation (YYYY-MM-DD)`
* **Domain:** `"How" (Platform)`
* **Concurrence:** `System Owner: Yes`
* **Context:** "Performed a scheduled Recovery Drill as per `guides/SYSTEM/recovery-drill.md`."
* **Decision:** "The drill [PASSED/FAILED]. Process Memory is [INTACT/CORRUPT]."
