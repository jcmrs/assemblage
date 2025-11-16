# 📜 Guide: "Triage Docs" Protocol
# (guides/SYSTEM/triage-docs-protocol.md)

# This is an instructional "Guide" for the "System Owner" (AI).
#
# PURPOSE:
# This "Guide" provides the formal "Triage" protocol for cleaning
# the "junk drawer" (`docs/`) folder inherited from the `perplex`
# repository.
#
# The `docs/` folder is a "Holistic System" failure; it mixes
# "house" (Assemblage) files, "furniture" (Product) files, and
# "historical" (Legacy) files. This "Guide" is the "How"
# for separating them.
#
# This "Guide" is executed by the "Utility" `tools/triage-docs.sh`.

---

## The "How" (Triage) Protocol

As the System Owner, you **MUST** apply the following 3 "triage" rules to *every file* currently in the `docs/` directory.

### Rule 1: Is this a "House" (Assemblage) Guide?
* **Test:** Does this file define a *protocol*, *process*, or *best practice* for the "Assemblage" framework itself? Does it belong in our "Owner's Manual"?
* **Example 1:** `docs/COMPLETENESS_REVIEW.md` (Yes, this is a "house" **Guide** for the "Auditor" Workbench).
* **Example 2:** `docs/BRANCH_MANAGEMENT.md` (Yes, this is a "house" **Guide**).
* **Action:**
    1.  Move the file to `guides/SYSTEM/` (for "Assemblage" protocols) or `guides/PRODUCT/` (for "Product" protocols).
    2.  **Crucial:** You **MUST** update any "wiring" (`config/workbenches.yml`) or "Guardrails" (`.githooks/`) that *pointed* to this file's old location.

### Rule 2: Is this a "Product" (Furniture) Anchor?
* **Test:** Does this file define the "Why" (Vision) or "What" (Source Material) for the *end-product* we are building?
* **Example 1:** `docs/PRODUCT_VISION.md` (Yes, this is the *core* "Product" **Anchor**).
* **Action:**
    1.  Move the file to `product/`.
    2.  Update any "wiring" in `config/workbenches.yml` (e.g., the "Explorer's" `context_anchors:`) to point to the new location.

### Rule 3: Is this "Historical" (Legacy) Process Memory?
* **Test:** Is this file a *log* or *analysis* of the *old* `perplex` "house" (e.g., the CDIR/CEXE migration)? Is it "contamination risk" if left in the main "house"?
* **Example 1:** `docs/THREE_AGENT_MIGRATION_ARCHITECTURE.md` (Yes, this is *legacy* "Process Memory").
* **Example 2:** `docs/SPEC_KIT_INTEGRATION_FINDINGS.md` (Yes, this is *legacy* analysis of the *old* "hardcoded" Spec Kit).
* **Action:**
    1.  Move the file to `archive/perplex_legacy/docs/`.
    2.  This "cleans" the "house" of "cognitive contamination" while *preserving* the "Process Memory" in an "attic" (the `archive/` folder) in case we need it later.
