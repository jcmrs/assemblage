"""
test_status.py

Tests for the 'status' command.
"""

from unittest.mock import MagicMock, patch

from assemblage.commands import status


@patch("assemblage.commands.status.code_search")
@patch("builtins.open")
@patch("json.load")
def test_status_index_exists(mock_json_load, mock_open, mock_code_search):
    """Tests the status command when the index exists."""
    args = MagicMock()
    args.index = True

    mock_code_search.INDEX_PATH.exists.return_value = True
    mock_code_search.INDEX_PATH.stat.return_value.st_mtime = (
        1678886400  # A fixed timestamp
    )
    mock_json_load.return_value = [1, 2, 3]  # 3 items

    with patch.object(status.sys, "exit") as mock_exit:
        status.run(args)
        mock_exit.assert_called_once_with(0)


@patch("assemblage.commands.status.code_search")
def test_status_index_not_exists(mock_code_search, capsys):
    """Tests the status command when the index does not exist."""
    args = MagicMock()
    args.index = True

    mock_code_search.INDEX_PATH.exists.return_value = False

    with patch.object(status.sys, "exit") as mock_exit:
        status.run(args)
        captured = capsys.readouterr()
        assert "Index not found" in captured.out
        mock_exit.assert_called_once_with(0)
