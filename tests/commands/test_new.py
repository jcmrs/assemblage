"""
tests.commands.test_new

Tests for the 'new' command and the stager logic.
"""

from unittest.mock import MagicMock, patch

from assemblage.stager import AdrToItemStage

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
