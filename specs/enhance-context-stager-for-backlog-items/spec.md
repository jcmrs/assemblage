# Specification: Enhance Context Stager for Backlog Items

This document provides the detailed technical blueprint for `ITEM-033`, enhancing the `control_plane new --type item` command as defined in `ADR-026`. This is a "Context Engineering" initiative.

## 1. Core Design: ADR Parser Utility

The central challenge is extracting structured information from the free-form Markdown of an ADR. We will create a new utility function for this purpose.

- **New Function:** in a new `assemblage/parsers.py` module.

```python
# assemblage/parsers.py
import re

def parse_adr(adr_content: str) -> dict:
    """
    Parses the content of an ADR Markdown file to extract key sections.
    """
    parsed_data = {
        "title": "",
        "context": "",
        "decision": "",
        "consequences": ""
    }

    # Extract Title (assumes the first H1 is the title)
    title_match = re.search(r"^#\s*(.*)", adr_content, re.MULTILINE)
    if title_match:
        parsed_data["title"] = title_match.group(1).strip()

    # A generic function to extract content between two headings
    def extract_section(section_name: str, content: str) -> str:
        pattern = re.compile(
            rf"##\s*{re.escape(section_name)}.*?$(.*?)##",
            re.DOTALL | re.MULTILINE
        )
        match = pattern.search(content + "\n##") # Add sentinel heading
        if match:
            return match.group(1).strip()
        return ""

    parsed_data["context"] = extract_section("1. Context", adr_content)
    parsed_data["decision"] = extract_section("2. Decision", adr_content)
    parsed_data["consequences"] = extract_section("4. Consequences", adr_content)

    return parsed_data
```

## 2. `new.py` Module Refactoring

The `_create_item` function within `assemblage/commands/new.py` will be significantly enhanced.

### Refactored `_create_item(args)` Logic

1.  **Guard Clause:** If `args.adr` is not provided, the function proceeds as it currently does (creating a blank item from the template).
2.  **Read ADR:** If `args.adr` is provided, read the content of the specified ADR file.
3.  **Parse ADR:** Call `parsers.parse_adr()` with the ADR content to get the structured data.
4.  **Generate "Why" Summary:** Create a summary string for the "Why" section of the new backlog item. This summary will include the title and a snippet of the context and decision from the parsed ADR data.
    ```python
    why_summary = (
        f"This item is based on the decision made in **{parsed_data['title']}**.\n\n"
        f"**Context:** {parsed_data['context'][:200]}...\n\n"  # Truncate for brevity
        f"**Decision:** {parsed_data['decision'][:300]}..."
    )
    ```
5.  **Suggest "What" (Acceptance Criteria):**
    *   Analyze the "Decision" and "Consequences" sections of the parsed ADR for bullet points or numbered lists, which often correspond to acceptance criteria.
    *   Extract these points and format them as a suggested list of acceptance criteria.
    *   This can be a simple regex for lines starting with `-` or `*` or a number.
6.  **Read Template:** Read the `backlog/items/TEMPLATE.md` file.
7.  **Populate Template:** Use `str.replace()` to substitute placeholders in the template with the generated content:
    *   Replace a `{{WHY_SUMMARY}}` placeholder with `why_summary`.
    *   Replace a `{{SUGGESTED_ACCEPTANCE_CRITERIA}}` placeholder with the suggested criteria.
    *   Update the ADR link as it does now.
8.  **Write New File:** Write the populated content to the new backlog item file.

## 3. `TEMPLATE.md` Update

- **File:** `backlog/items/TEMPLATE.md`
- **Action:** Update the template to include the new placeholders.

```markdown
# ITEM-XXX: [Item Title]

**Date Created:** {{DATE}}
**Status:** Ready for Architect
**Priority:** Medium
**Owner:** Architect

## 1. Description
{{WHY_SUMMARY}}

## 2. "Why" (The Source Material)

* **Decision (The "Why"):**
    * `decisions/ADR-XXX.md`

## 3. "What" (Acceptance Criteria)
{{SUGGESTED_ACCEPTANCE_CRITERIA}}

## 4. "How" (Implementation Link)

* **Blueprint (The "How"):**
    * `specs/XXX-spec-name/spec.md`
```

## 4. Test Plan

- **`tests/test_parsers.py`**:
    - A new test file for the `parse_adr` function.
    - `test_parse_valid_adr`: Provide mock ADR content and assert that the title, context, decision, and consequences are extracted correctly.
    - `test_parse_adr_missing_sections`: Assert that the function returns empty strings for sections that are not present.

- **`tests/commands/test_new.py`**:
    - Enhance the existing test file for the `new` command.
    - `test_create_item_from_adr`:
        - Mock the file system to include a sample ADR file and the item template.
        - Call `_create_item` with the `--adr` argument.
        - Assert that the newly created backlog item file exists.
        - Read the new file and assert that the `{{WHY_SUMMARY}}` and `{{SUGGESTED_ACCEPTANCE_CRITERIA}}` placeholders have been replaced with content derived from the mock ADR.

```
