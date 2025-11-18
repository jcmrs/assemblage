# 📜 Guide: Utility Test Protocol (Python Edition)

This is an instructional "Guide" for the "System Owner" (AI).

**PURPOSE:**
To define the non-negotiable protocol for ensuring the "integrity" of all "Utilities" (the "house" automation scripts in `assemblage/tools/`). A "Utility" is a "How" (Platform) component that other parts of the Assemblage depend on. If a Utility is broken, the Assemblage is unstable. This protocol makes our "house" robust by enforcing automated testing for all its automation.

This protocol MUST be followed for every change to a `assemblage/tools/` module.

---

## The "How" (Platform) Test Protocol

As the System Owner, when you create or modify any **Utility** (a `.py` module in the `assemblage/tools/` directory), you **MUST** follow these 3 steps:

### Step 1: Create or Update the Test

For every `assemblage/tools/my_script.py`, you **MUST** create or update a corresponding test file in the `tests/tools/` directory.

*   **Location:** `tests/tools/test_my_script.py`
*   **Framework:** We use the **Pytest** framework.
*   **Best Practices:**
    *   Tests should be isolated and not depend on the state of other tests.
    *   Use Pytest fixtures (`@pytest.fixture`) to create and clean up temporary files or mock objects.
    *   Use the `unittest.mock` library (e.g., `@patch`) to isolate tests from the filesystem, network, or subprocesses.

### Step 2: Run the Tests

Before you can finalize the change, you **MUST** run the *entire* Assemblage test suite to prove your change works and did not *break* any other "Utilities."

*   **Command:** `pytest`

### Step 3: Validate the Outcome

*   If all tests **PASS**, your "Utility" is considered *stable* and you may proceed with the "Assemblage Change Protocol."
*   If *any* test **FAILS**, you **MUST** return to Step 1. You are "constitutionally" (by this "Guide") blocked from committing a change that breaks the "house's" integrity.