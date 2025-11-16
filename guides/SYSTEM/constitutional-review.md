# 📜 Guide: Constitutional Review
# (guides/SYSTEM/constitutional-review.md)

# This is an instructional "Guide" for the "Auditor" Workbench.
#
# PURPOSE:
# To provide a formal "check & balance" exercise for the System Owner (AI).
# This "Guide" ensures that any modifications to the "Assemblage" framework
# (the "house" itself, e.g., new "Utilities," "Anchors," or "Schemas")
# are audited against our core "Anchors" (the Imperatives).
#
# NUDGE (TRIGGER):
# This "Guide" is triggered (nudged) by the "Assemblage Change Protocol"
# (`guides/SYSTEM/assemblage-change-protocol.md`) whenever a "How"
# (Platform) component is added or modified.

---

## Assemblage Audit Checklist

As the System Owner, you must validate the "How" (the platform change) against the "Why" (our Imperatives). For the proposed change, answer the following:

### 1. Imperative: AI-First
- [ ] Does this change *reduce* or *offload* the AI's cognitive load?
- [ ] Does it increase the AI's autonomy (e.g., like our "Specialist" creator)?
- [ ] Does it make the system *easier* for a new AI session to understand?

### 2. Imperative: Holistic System Thinking
- [ ] Have all "ripple effects" been considered?
- [ ] Does this change integrate cleanly with the 4 Workbenches (Explorer, Architect, Builder, Auditor)?
- [ ] Does this change *create* a new "gap" or "silo," or does it *connect* existing components?

### 3. Imperative: The Five Cornerstones
- [ ] **Configurability:** Is the new behavior defined in **config** (`.yml`), or is it hardcoded?
- [ ] **Modularity:** Is this a new, self-contained "Lego brick," or does it make an existing brick more complex?
- [ ] **Extensibility:** Does this *enable* future extension, or does it *limit* it?
- [ ] **Integration:** Does this use our established "connects" (e.g., "Anchors" as data, "Utilities" as tools)?
- [ ] **Automation:** Does this *automate* a process, or does it *create* a new manual step?

### 4. Imperative: Project = Repository
- [ ] Is this new component fully defined by text-based files within the repository?
- [ ] Are there any external, un-tracked dependencies that would prevent a new AI from using this?

### 5. Imperative: Architecture as Code
- [ ] Is this new component *discoverable* by reading our schemas (e.g., `config/workbenches.yml`)?
- [ ] If this is a new "Utility" (`tools/`) or "Guide" (`guides/`), is it properly "wired in" to the `config/` files?

### 6. Imperative: Bifurcated Ownership (User = Strategic Partner)
- [ ] Does this change reinforce the AI's ownership of the "How"?
- [ ] Does it *avoid* putting the Vision Owner (human) "in the loop" of a technical process?
- [ ] Has this "How" decision been formally logged in a `decisions/` ADR, referencing the "Why" (Vision) it serves?

### Audit Outcome

- [ ] **PASS:** The change is constitutional and aligns with our "Why."
- [ ] **FAIL:** The change violates one or more imperatives.
    - **Required Action:** Create a new "Learned Nudge" in `knowledge/learnings/patterns/` to capture the failure, then re-architect the solution.
