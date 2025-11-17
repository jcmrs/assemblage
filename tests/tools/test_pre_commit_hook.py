"""
test_pre_commit_hook.py

Tests for the pre_commit_hook utility.
"""

from unittest.mock import patch, MagicMock
import pytest
from assemblage.tools import pre_commit_hook

def test_hook_success_on_clean_code():
    """
    Tests that the script exits with 0 when ruff finds no errors.
    """
    with patch("subprocess.run") as mock_run:
        # Mock a successful run (returncode 0)
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        with pytest.raises(SystemExit) as e:
            pre_commit_hook.main()
        
        assert e.type == SystemExit
        assert e.value.code == 0

def test_hook_failure_on_lint_errors():
    """
    Tests that the script exits with 1 when ruff finds errors.
    """
    with patch("subprocess.run") as mock_run:
        # Mock a failed run (returncode 1)
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_run.return_value = mock_process
        
        with pytest.raises(SystemExit) as e:
            pre_commit_hook.main()
            
        assert e.type == SystemExit
        assert e.value.code == 1

def test_hook_handles_file_not_found():
    """
    Tests that the script exits with 1 if 'ruff' command is not found.
    """
    with patch("subprocess.run", side_effect=FileNotFoundError) as mock_run:
        with pytest.raises(SystemExit) as e:
            pre_commit_hook.main()
            
        assert e.type == SystemExit
        assert e.value.code == 1
