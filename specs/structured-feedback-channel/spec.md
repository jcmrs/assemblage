# Specification: Structured Feedback Channel

This document provides the detailed technical blueprint for `ITEM-020`, implementing the Structured Feedback Channel as defined in `ADR-013`.

## 1. File and Directory Structure

- **New Directory:** `feedback/` will be created at the project root to store feedback logs.
- **New Module:** `assemblage/commands/feedback.py` will be created to house the command's logic.
- **New Test File:** `tests/commands/test_feedback.py` will be created.

## 2. Command Definition

- **File:** `config/commands.yml`
- **Action:** Add the new `feedback` command definition.

```yaml
  feedback:
    entry_point: "assemblage.commands.feedback.run"
    help: "Provide structured, two-phase feedback on a specific commit."
    arguments:
      - name: "--commit"
        required: true
        help: "The git commit hash to review."
```

## 3. `feedback.py` Module Design

This module will be responsible for the entire two-phase feedback process.

### 3.1. Main `run(args)` function
This function will orchestrate the process:
1.  Validate that the commit hash provided in `args.commit` exists using `git cat-file -e <hash>`.
2.  Call a private function `_generate_self_report(args.commit)` to get the objective data.
3.  Print the AI's self-report to the console in a clean, readable format.
4.  Call a private function `_prompt_vision_owner_review()` to get the subjective data.
5.  Combine the two dictionaries into a single payload.
6.  Call `_save_feedback(payload)` to write the final YAML file.
7.  Print a success message.

### 3.2. `_generate_self_report(commit_hash)` function
This function gathers objective data about the commit.
1.  **Commit Message & Task ID:**
    -   Run `git show -s --format=%B <commit_hash>` to get the full commit message.
    -   Use regex (`r"(ITEM|ADR)-\d+"`) to find the associated Task ID.
2.  **Commit Stats:**
    -   Run `git show --shortstat --oneline <commit_hash>` to get the summary line (e.g., `1 file changed, 5 insertions(+), 2 deletions(-)`).
    -   Use regex to parse the numbers for files changed, insertions, and deletions.
3.  **Test Analysis:**
    -   Run `git show --name-only --oneline <commit_hash>` to get a list of changed files.
    -   Count how many of the changed files are located in the `tests/` directory. This will be our `tests_impacted` metric.
4.  **Self-Correction (Future Work):**
    -   This field will be hardcoded to return `"N/A"` in this version. The blueprint acknowledges that implementing this requires changes to the `commit_wrapper` to log its actions, which is out of scope.
5.  **Return Value:** The function will return a dictionary containing all the gathered data.

### 3.3. `_prompt_vision_owner_review()` function
This function interactively prompts the user for their subjective review.
1.  It will use a helper function, `_prompt_for_rating(prompt_text)`, to ask for each of the three ratings (Clarity, Efficiency, Correctness), validating that the input is an integer between 1 and 5.
2.  It will use another helper, `_prompt_for_multiline(prompt_text)`, to capture the free-text `positive_notes` and `improvement_areas`.
3.  It will return a dictionary containing the user's input.

### 3.4. `_save_feedback(data)` function
1.  Generate a filename using the current UTC timestamp (e.g., `feedback/2025-11-22T023000Z.yml`).
2.  Use `yaml.dump` to write the `data` dictionary to the new file, ensuring a clean format.

## 4. Test Plan

- **File:** `tests/commands/test_feedback.py`
- **`test_generate_self_report`**:
    -   Will mock `subprocess.run` to return pre-canned output for `git show`.
    -   Will call `_generate_self_report` and assert that the returned dictionary correctly parses the numbers for files, insertions, deletions, and impacted tests from the mock git output.
- **`test_prompt_vision_owner_review`**:
    -   Will mock `sys.stdin.readline` to simulate a user entering ratings and multi-line comments.
    -   Will call `_prompt_vision_owner_review` and assert that the returned dictionary matches the simulated input.
- **`test_run_orchestration`**:
    -   An integration test for the main `run` function.
    -   It will patch the internal functions (`_generate_self_report`, `_prompt_vision_owner_review`, `_save_feedback`) to assert they are called in the correct order.

This blueprint provides a complete and actionable plan for the Builder.
