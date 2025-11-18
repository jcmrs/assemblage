"""
test_control_plane.py

Tests for the main control_plane module.
"""

import sys
from unittest.mock import patch, MagicMock
import pytest
from assemblage import control_plane

def test_observe_command_success(monkeypatch):
    """
    Tests that the 'observe' command successfully calls the dashboard generator.
    """
    # Patch the dashboard_generator's main function
    mock_generate = MagicMock()
    monkeypatch.setattr(control_plane.dashboard_generator, "generate", mock_generate)
    
    # Mock sys.argv to simulate command line call
    monkeypatch.setattr(sys, "argv", ["control_plane.py", "observe"])
    
    with pytest.raises(SystemExit) as e:
        control_plane.main()
        
    assert e.value.code == 0
    mock_generate.assert_called_once()

def test_invalid_command(capsys):
    """
    Tests that an invalid command exits with an error.
    """
    with patch("sys.argv", ["control_plane.py", "invalid_command"]):
        with pytest.raises(SystemExit) as e:
            control_plane.main()
            
        assert e.value.code != 0
        captured = capsys.readouterr()
        assert "usage: control_plane.py" in captured.err
        assert "invalid choice: 'invalid_command'" in captured.err
