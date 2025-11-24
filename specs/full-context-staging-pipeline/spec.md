# Specification: Full Context Staging Pipeline

This document provides the detailed technical blueprint for `ITEM-027`, completing the context staging pipeline as defined in `ADR-020`.

## 1. New Template: `specs/TEMPLATE.md`

A new template is required for generating spec documents.

- **New File:** `specs/TEMPLATE.md`
- **Content:**
```markdown
# Specification: {{ITEM_TITLE}}

This document provides the detailed technical blueprint for `ITEM-{{ITEM_ID_PADDED}}`, as defined in `decisions/ADR-{{ADR_NUMBER}}.md`.

## 1. "Why" & "What" (from Backlog Item)

### 1.1. Description (Why)
{{WHY_SUMMARY}}

### 1.2. Acceptance Criteria (What)
{{ACCEPTANCE_CRITERIA}}

---

## 2. "How" (The Blueprint)

*This section is to be filled out by the Architect.*

### 2.1. Core Design & Rationale

*A high-level overview of the proposed implementation.*

### 2.2. Module & Function Design

*Detailed breakdown of new or modified modules, classes, and functions.*

### 2.3. Test Plan

*A checklist of test cases to be implemented.*
- [ ]
- [ ]
```

## 2. Parser Enhancement

- **Module:** `assemblage/parsers.py`
- **Action:** Add a new `parse_item` function.

```python
# assemblage/parsers.py (addition)

def parse_item(item_content: str) -> dict:
    """
    Parses the content of a Backlog Item Markdown file.
    """
    parsed_data = {
        "title": "",
        "description": "",
        "acceptance_criteria": "",
        "adr_link": ""
    }

    # Extract Title
    title_match = re.search(r"^#\s*ITEM-.*?:(.*)", item_content, re.MULTILINE)
    if title_match:
        parsed_data["title"] = title_match.group(1).strip().replace("[", "").replace("]", "")

    # Using the same helper as parse_adr
    def extract_section(section_name: str, content: str) -> str:
        pattern = re.compile(
            rf"##\s*{re.escape(section_name)}.*?\n(.*?)(?=\n##|\Z)",
            re.DOTALL
        )
        match = pattern.search(content)
        if match:
            return match.group(1).strip()
        return ""

    parsed_data["description"] = extract_section("1. Description", item_content)
    parsed_data["acceptance_criteria"] = extract_section("3. \"What\" (Acceptance Criteria)", item_content)

    # Extract ADR link
    adr_match = re.search(r"`decisions/(ADR-\d+-.*?.md)`", item_content)
    if adr_match:
        parsed_data["adr_link"] = adr_match.group(1)

    return parsed_data
```

## 3. Stager Enhancement

- **Module:** `assemblage/stager.py`
- **Actions:**
    1.  Create a new `ItemToSpecStage` class.
    2.  Update the `get_stage_handler` factory function to use it.

### `ItemToSpecStage` Class Design
```python
# assemblage/stager.py (addition)

class ItemToSpecStage(BaseStage):
    """Stage handler for creating a Spec from a Backlog Item."""

    def _get_template_path(self):
        return Path("specs/TEMPLATE.md")

    def _get_target_dir(self):
        return Path("specs")

    def _render(self, template, context):
        """Renders the spec template."""
        content = template
        content = content.replace("{{ITEM_TITLE}}", context.get("ITEM_TITLE", "[Item Title]"))
        content = content.replace("{{ITEM_ID_PADDED}}", context.get("ITEM_ID_PADDED", "XXX"))
        content = content.replace("{{ADR_NUMBER}}", context.get("ADR_NUMBER", "XXX"))
        content = content.replace("{{WHY_SUMMARY}}", context.get("WHY_SUMMARY", ""))
        content = content.replace("{{ACCEPTANCE_CRITERIA}}", context.get("ACCEPTANCE_CRITERIA", ""))
        return content

    def assemble_context(self):
        """Gathers context from the source Backlog Item."""
        if not self.from_id:
            raise ValueError("Creating a 'spec' requires a source item ID via --from-item.")

        # Find the item file
        item_dir = Path("backlog/items")
        item_files = list(item_dir.glob(f"{self.from_id:03d}-*.md"))
        if not item_files:
            raise FileNotFoundError(f"Could not find item with ID '{self.from_id:03d}'.")

        item_content = item_files[0].read_text(encoding="utf-8")
        parsed_item = parsers.parse_item(item_content)

        # Extract ADR number from the link
        adr_num_match = re.search(r"ADR-(\d+)", parsed_item["adr_link"])
        adr_number = adr_num_match.group(1) if adr_num_match else "XXX"

        return {
            "ITEM_TITLE": parsed_item["title"],
            "ITEM_ID_PADDED": f"{self.from_id:03d}",
            "ADR_NUMBER": adr_number,
            "WHY_SUMMARY": parsed_item["description"],
            "ACCEPTANCE_CRITERIA": parsed_item["acceptance_criteria"],
        }
```

### `get_stage_handler` Update
```python
# assemblage/stager.py (modification)

def get_stage_handler(doc_type, title, from_adr=None, from_item=None):
    """Factory function to get the correct stage handler."""
    if doc_type == "item":
        if from_adr:
            return AdrToItemStage(title, from_id=int(from_adr))
        else:
            raise ValueError("Creating an 'item' requires a source ADR via --from-adr.")
    elif doc_type == "spec":
        if from_item:
            return ItemToSpecStage(title, from_id=int(from_item))
        else:
            raise ValueError("Creating a 'spec' requires a source item via --from-item.")
    else:
        raise ValueError(f"Unknown document type '{doc_type}'.")
```

## 4. Test Plan

- **`tests/test_parsers.py`**:
    - Add `test_parse_item` to validate the new backlog item parser with mock content.

- **`tests/commands/test_new.py`**:
    - Add `test_create_spec_from_item`:
        - Mock the file system with a sample backlog item and the new spec template.
        - Call the `ItemToSpecStage` handler.
        - Assert that the generated spec file contains the correctly transplanted "Why" summary and "Acceptance Criteria" from the mock item.

```
