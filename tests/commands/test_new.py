"""
tests.commands.test_new

Tests for the 'new' command and the stager logic.
"""

from unittest.mock import MagicMock, patch

from assemblage.stager import AdrToItemStage, ItemToSpecStage

MOCK_ADR_CONTENT = """
# ADR-001: Some Great Decision

**Date:** 2025-01-01
**Status:** Accepted

---

## 1. Context

This is the context section. It has multiple lines.

## 2. Decision

We have decided to do the thing.
- Thing 1
- Thing 2

This decision has implications.

## 3. Rationale

This is why we did it.

## 4. Consequences

- Consequence A
- Consequence B
"""


@patch("pathlib.Path.glob")
def test_create_item_from_adr(mock_glob):
    """
    Tests that creating an item from an ADR correctly parses the ADR
    and generates the context summary.
    """
    # --- Arrange ---
    # Mock the file system interactions
    mock_adr_path = MagicMock()
    mock_adr_path.read_text.return_value = MOCK_ADR_CONTENT
    mock_glob.return_value = [mock_adr_path]

    # Instantiate the stage handler
    stage = AdrToItemStage(title="New Item Title", from_id=1)

    # --- Act ---
    context = stage.assemble_context()

    # --- Assert ---
    # Check that the "Why" summary was generated correctly
    assert (
        "implements the decision from **ADR-001: Some Great Decision**"
        in context["WHY_SUMMARY"]
    )
    assert "Context:** This is the context section." in context["WHY_SUMMARY"]
    assert "Decision:** We have decided to do the thing." in context["WHY_SUMMARY"]

    # Check that acceptance criteria were suggested
    assert "- [ ] Thing 1" in context["SUGGESTED_ACCEPTANCE_CRITERIA"]
    assert "- [ ] Thing 2" in context["SUGGESTED_ACCEPTANCE_CRITERIA"]
    assert "- [ ] Consequence A" in context["SUGGESTED_ACCEPTANCE_CRITERIA"]
    assert "- [ ] Consequence B" in context["SUGGESTED_ACCEPTANCE_CRITERIA"]


MOCK_ITEM_CONTENT = """
# ITEM-027: [Implement Full Context Staging Pipeline]

## 1. Description
This item implements the decision from **ADR-020: Full Context Staging Pipeline**.
**Context:** The Context Staging System is incomplete...
**Decision:** We will extend the Context Staging System...

## 2. "Why" (The Source Material)
* **Decision (The "Why"):**
    * `decisions/ADR-020-full-context-staging-pipeline.md`

## 3. "What" (Acceptance Criteria)
- [ ] The `control_plane new --type spec` command is enhanced.
- [ ] A new `spec.md` file is generated.
"""

MOCK_SPEC_TEMPLATE = """
# Specification: {{ITEM_TITLE}}
From ITEM-{{ITEM_ID_PADDED}} and ADR-{{ADR_NUMBER}}.
Why: {{WHY_SUMMARY}}
What: {{ACCEPTANCE_CRITERIA}}
"""


@patch("pathlib.Path.mkdir")
@patch("pathlib.Path.write_text")
@patch("pathlib.Path.read_text")
@patch("pathlib.Path.glob")
def test_create_spec_from_item(
    mock_glob, mock_read_text, mock_write_text, mock_mkdir, tmp_path
):
    """
    Tests that creating a spec from an item correctly generates the spec file.
    """
    # --- Arrange ---
    # Mock the file system to find the item and read its content
    mock_item_path = MagicMock()
    mock_item_path.read_text.return_value = MOCK_ITEM_CONTENT
    mock_glob.return_value = [mock_item_path]

    # Mock the reading of the spec template
    mock_read_text.return_value = MOCK_SPEC_TEMPLATE

    # Instantiate and run the stage handler
    stage = ItemToSpecStage(title="Implement Full Context Staging Pipeline", from_id=27)

    # --- Act ---
    # We call the private methods directly to test the logic without creating real files
    context = stage.assemble_context()
    rendered_content = stage._render(MOCK_SPEC_TEMPLATE, context)

    # --- Assert ---
    assert "Implement Full Context Staging Pipeline" in rendered_content
    assert "ITEM-027" in rendered_content
    assert "ADR-020" in rendered_content
    assert "The Context Staging System is incomplete" in rendered_content
    assert (
        "- [ ] The `control_plane new --type spec` command is enhanced."
        in rendered_content
    )
