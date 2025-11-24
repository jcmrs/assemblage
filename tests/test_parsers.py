"""
tests.test_parsers

Tests for the reusable parsing functions.
"""

from assemblage.parsers import parse_adr

MOCK_ADR_CONTENT = """
# ADR-001: Some Great Decision

**Date:** 2025-01-01
**Status:** Accepted

---

## 1. Context

This is the context section.
It has multiple lines.

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

MOCK_ADR_NO_CONSEQUENCES = """
# ADR-002: Another Decision

## 1. Context

Some context.

## 2. Decision

Another decision.
"""


def test_parse_valid_adr():
    """Tests that a valid ADR is parsed correctly."""
    parsed = parse_adr(MOCK_ADR_CONTENT)
    assert parsed["title"] == "ADR-001: Some Great Decision"
    assert "This is the context section." in parsed["context"]
    assert "We have decided to do the thing." in parsed["decision"]
    assert "Consequence A" in parsed["consequences"]


def test_parse_adr_missing_sections():
    """Tests that missing sections result in empty strings."""
    parsed = parse_adr(MOCK_ADR_NO_CONSEQUENCES)
    assert parsed["title"] == "ADR-002: Another Decision"
    assert "Some context." in parsed["context"]
    assert "Another decision." in parsed["decision"]
    assert parsed["consequences"] == ""
