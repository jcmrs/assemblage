# Specification: Feedback Analysis Loop

This document provides the detailed technical blueprint for `ITEM-021`, implementing the Feedback Analysis Loop as defined in `ADR-014`.

## 1. Command Definition

- **File:** `config/commands.yml`
- **Action:** Add the new `analyze_feedback` command definition.

```yaml
  analyze_feedback:
    entry_point: "assemblage.commands.analyze_feedback.run"
    help: "Analyzes all feedback files and proposes new nudges."
```

## 2. `analyze_feedback.py` Module Design

A new module, `assemblage/commands/analyze_feedback.py`, will be created to house the command's logic.

### 2.1. Main `run(args)` function
This function will orchestrate the analysis:
1.  Call a private function `_load_all_feedback()` to get a list of all feedback data structures.
2.  If the list is empty, print a message and exit.
3.  Call `_calculate_and_print_stats(all_feedback)` to display aggregate rating data.
4.  Call `_analyze_and_propose_nudges(all_feedback)` to generate and print nudge proposals.

### 2.2. `_load_all_feedback()` function
1.  Define `feedback_dir = Path("feedback/")`.
2.  If the directory doesn't exist, return an empty list.
3.  Use `feedback_dir.glob("*.yml")` to find all feedback files.
4.  Iterate through the files, load each with `yaml.safe_load`, and append the resulting dictionary to a list.
5.  Return the list of feedback data.

### 2.3. `_calculate_and_print_stats(all_feedback)` function
1.  Extract all `vision_owner_review` sections from the feedback list.
2.  For each rating (`clarity_rating`, `efficiency_rating`, `correctness_rating`), create a list of all submitted scores.
3.  Calculate the average for each rating list, handling potential division by zero if no ratings are present.
4.  Print the results in a formatted summary table to the console.

### 2.4. `_analyze_and_propose_nudges(all_feedback)` function
This function will perform text analysis and generate nudge proposals.
1.  **Corpus Aggregation:** Concatenate the `improvement_areas` string from every feedback file into a single large text corpus.
2.  **Text Normalization:**
    -   Convert the entire corpus to lowercase.
    -   Use regex (`re.findall(r'\b\w{3,}\b', ...)`) to extract all words of 3 or more characters, effectively filtering out punctuation and very short words.
3.  **Stop Word Filtering:**
    -   Define a simple, hardcoded `set` of common English stop words (e.g., `{'the', 'and', 'for', 'are', 'was', 'but', 'not', 'this', 'that'}`).
    -   Filter the list of extracted words to remove any that are in the stop word set.
4.  **Keyword Frequency:**
    -   Use `collections.Counter` to count the occurrences of the remaining words.
    -   Get the top 3-5 most common words using `most_common()`.
5.  **Nudge Generation & Printing:**
    -   Print a clear header for the proposals.
    -   For each of the top keywords (e.g., "documentation", "testing", "refactor"):
        -   Create a new nudge ID: `nudge_{keyword}_check`.
        -   Create a new nudge text: `f"Did you remember to address {keyword} in this change?"`
        -   Print the proposed nudge to the console in a format that can be easily copied into `config/nudges.yml`.

## 3. Test Plan

- **File:** `tests/commands/test_analyze_feedback.py`
- **Fixture:** A `pytest` fixture will create a temporary `feedback/` directory and populate it with 2-3 mock YAML files containing sample ratings and `improvement_areas` with some overlapping keywords (e.g., "testing").
- **`test_calculate_stats`**:
    -   Will use the fixture, load the mock data, and call `_calculate_and_print_stats`.
    -   Will use `capsys` to capture the console output and assert that the printed averages match the expected values from the mock data.
- **`test_nudge_proposal`**:
    -   Will use the fixture, load the mock data, and call `_analyze_and_propose_nudges`.
    -   Will use `capsys` to capture the console output and assert that a correctly formatted nudge proposal for the overlapping keyword ("testing") is present in the output.

This blueprint provides a complete and actionable plan for the Builder.
