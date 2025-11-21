"""
test_query.py

Tests for the 'query' command.
"""

from unittest.mock import MagicMock, patch

from assemblage.commands import query


@patch("assemblage.commands.query.code_search")
def test_query_success(mock_code_search):
    """Tests that the query command calls the code_search module."""
    args = MagicMock()
    args.query = "test query"

    mock_code_search.search_index.return_value = [
        {"path": "a.py", "line": 1, "score": 0.9, "content": "content a"}
    ]

    with patch.object(query.sys, "exit") as mock_exit:
        query.run(args)
        mock_code_search.search_index.assert_called_once_with("test query")
        mock_exit.assert_called_once_with(0)


@patch("assemblage.commands.query.code_search")
def test_query_no_results(mock_code_search, capsys):
    """Tests the query command when no results are found."""
    args = MagicMock()
    args.query = "test query"

    mock_code_search.search_index.return_value = []

    with patch.object(query.sys, "exit") as mock_exit:
        query.run(args)
        captured = capsys.readouterr()
        assert "No relevant code snippets found" in captured.out
        mock_exit.assert_called_once_with(0)
