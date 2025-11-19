"""
test_stager.py

Tests for the Context Staging System.
"""

import pytest

from assemblage import stager


@pytest.fixture
def mock_env(tmp_path):
    """Creates a temporary directory with mock ADRs and templates."""
    # Create directories
    decisions_dir = tmp_path / "decisions"
    decisions_dir.mkdir()
    templates_dir = tmp_path / "guides" / "TEMPLATES"
    templates_dir.mkdir(parents=True)
    backlog_dir = tmp_path / "backlog" / "items"
    backlog_dir.mkdir(parents=True)

    # Create mock ADR
    adr_content = "# ADR-999: My Mock Decision\n\nThis is the context."
    (decisions_dir / "999-my-mock-decision.md").write_text(adr_content)

    # Create mock template
    template_content = "ADR Link: {ADR_LINK}\nADR Title: {ADR_TITLE}\nDate: {DATE}"
    (templates_dir / "item_template.md").write_text(template_content)

    return tmp_path


def test_adr_to_item_creation(mock_env, monkeypatch):
    """
    Tests the successful creation of a backlog item from an ADR.
    """
    # Patch the file system paths to use the temporary environment
    monkeypatch.setattr(stager, "Path", lambda *args: mock_env.joinpath(*args))

    # Get the handler
    handler = stager.get_stage_handler(
        doc_type="item", title="My New Item", from_adr="999"
    )

    # Run the process
    briefing = handler.run()

    # Assertions
    new_file = mock_env / "backlog" / "items" / "001-my-new-item.md"
    assert new_file.exists()

    content = new_file.read_text()
    assert "ADR-999" in content
    assert "My Mock Decision" in content

    assert "CONTEXT STAGE: Complete" in briefing
    assert "- **ADR_TITLE:** My Mock Decision" in briefing
    assert "Your Task:" in briefing
    assert str(new_file) in briefing


def test_handler_factory_errors(mock_env):
    """
    Tests that the factory function raises appropriate errors.
    """
    with pytest.raises(ValueError, match="requires a source ADR"):
        stager.get_stage_handler(doc_type="item", title="My New Item")

    with pytest.raises(ValueError, match="Unknown document type"):
        stager.get_stage_handler(doc_type="unknown", title="My New Item")


def test_adr_not_found(mock_env, monkeypatch):
    """
    Tests that a FileNotFoundError is raised if the source ADR doesn't exist.
    """
    monkeypatch.setattr(stager, "Path", lambda *args: mock_env.joinpath(*args))

    with pytest.raises(FileNotFoundError):
        handler = stager.get_stage_handler(
            doc_type="item",
            title="My New Item",
            from_adr="007",  # This ADR doesn't exist
        )
        handler.run()
