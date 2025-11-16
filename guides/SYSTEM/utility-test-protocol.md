# 📜 Guide: Utility Test Protocol
# (guides/SYSTEM/utility-test-protocol.md)

# This is an instructional "Guide" for the "System Owner" (AI).
#
# PURPOSE:
# To define the non-negotiable protocol for ensuring the "integrity"
# of all "Utilities" (the "house" automation scripts in `tools/`).
#
# A "Utility" (like `tools/validate-assemblage.sh`) is a "How" (Platform)
# component that other parts of the Assemblage *depend on*. If a Utility
# is broken, the Assemblage is unstable.
#
# This protocol makes our "house" robust by enforcing automated testing
# for all its "hands" (the Utilities).
#
# This protocol MUST be followed for every change to a `tools/` script.

---

## The "How" (Platform) Test Protocol

As the System Owner, when you create or modify any **Utility** (a `.sh` script in the `tools/` directory), you **MUST** follow these 3 steps:

### Step 1: Create or Update the Test
For every `tools/my-script.sh`, you **MUST** create or update a corresponding test file in the `tests/tools/` directory.
* **Location:** `tests/tools/my-script.bats`
* **Framework:** We use the **BATS (Bash Automated Testing System)** framework.
* **Example:** See `tests/tools/validate-foundation.bats` for a clear example.
* **Helpers:** You **MUST** use the built-in test helpers: `source "helpers/test-helpers.bash"`.

### Step 2: Run the Tests
Before you can finalize the change, you **MUST** run the *entire* Assemblage test suite to prove your change works and did not *break* any other "Utilities."
* **Command:** `./tests/run-tests.sh` (or our `tools/run-assemblage-tests.sh` wrapper).

### Step 3: Validate the Outcome
* If all tests **PASS**, your "Utility" is considered *stable* and you may proceed with the "Assemblage Change Protocol" (`guides/SYSTEM/assemblage-change-protocol.md`).
* If *any* test **FAILS**, you **MUST** return to Step 1. You are "constitutionally" (by this "Guide") blocked from committing a change that breaks the "house's" integrity.
