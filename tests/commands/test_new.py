"""
test_new.py

Tests for the 'new' command module.
"""

from unittest.mock import MagicMock, patch

from assemblage.commands import new


@patch("assemblage.commands.new.stager")
def test_new_command_calls_stager(mock_stager):
    """
    Tests that the 'new' command correctly calls the stager module.
    """
    # --- Setup Mocks ---
    mock_handler = MagicMock()
    mock_stager.get_stage_handler.return_value = mock_handler

    # Mock the command line arguments
    args = MagicMock()
    args.type = "item"
    args.title = "Test Title"
    args.from_adr = "123"
    args.from_item = None

    # --- Execution ---
    with patch.object(new.sys, "exit") as mock_exit:
        new.run(args)

    # --- Assertions ---
    # Assert that the factory was called correctly
    mock_stager.get_stage_handler.assert_called_once_with(
        "item", "Test Title", from_adr="123", from_item=None
    )

    # Assert that the handler's run method was called
    mock_handler.run.assert_called_once()

    # Assert that the command exits successfully
    mock_exit.assert_called_once_with(0)
