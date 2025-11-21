"""
test_index.py

Tests for the 'index' command.
"""

from unittest.mock import patch

from assemblage.commands import index


@patch("assemblage.commands.index.code_search")
def test_index_success(mock_code_search):
    """Tests that the index command calls the code_search module."""
    with patch.object(index.sys, "exit") as mock_exit:
        index.run(None)
        mock_code_search.build_index.assert_called_once()
        mock_exit.assert_called_once_with(0)


@patch("assemblage.commands.index.code_search")
def test_index_failure(mock_code_search):
    """Tests that the index command handles exceptions."""
    mock_code_search.build_index.side_effect = Exception("Test Exception")
    with patch.object(index.sys, "exit") as mock_exit:
        index.run(None)
        mock_code_search.build_index.assert_called_once()
        mock_exit.assert_called_once_with(1)
