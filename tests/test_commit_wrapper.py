"""
test_commit_wrapper.py

Tests for the git commit wrapper and its self-correction logic.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from assemblage import commit_wrapper


@patch("assemblage.commit_wrapper.subprocess.run")
def test_success_on_first_try(mock_run):
    """
    Tests that the script exits 0 if the first commit succeeds.
    """
    mock_run.return_value = MagicMock(returncode=0, stdout="Success!")
    with patch.object(sys, "argv", ["commit_wrapper.py", "-m", "test commit"]):
        with pytest.raises(SystemExit) as e:
            commit_wrapper.main()
        assert e.value.code == 0

        assert mock_run.call_count == 1

        # Check the call arguments more flexibly
        call_args, call_kwargs = mock_run.call_args
        assert call_args[0] == ["git", "commit", "-m", "test commit"]
        assert call_kwargs["capture_output"] is True
        assert call_kwargs["text"] is True


@patch("assemblage.commit_wrapper.subprocess.run")
def test_successful_self_correction(mock_run):
    """
    Tests the full self-correction happy path.
    """
    # Simulate the sequence of subprocess calls
    mock_run.side_effect = [
        # 1. First commit fails with fixable error
        MagicMock(returncode=1, stdout="- files were modified by this hook", stderr=""),
        # 2. 'git add -u' succeeds
        MagicMock(returncode=0),
        # 3. Second commit succeeds
        MagicMock(returncode=0, stdout="Success on second try!"),
    ]

    with patch.object(sys, "argv", ["commit_wrapper.py", "-m", "test commit"]):
        with pytest.raises(SystemExit) as e:
            commit_wrapper.main()
        assert e.value.code == 0

    assert mock_run.call_count == 3


@patch("assemblage.commit_wrapper.subprocess.run")
def test_failure_on_unfixable_error(mock_run):
    """
    Tests that the script fails if the error is not fixable.
    """
    mock_run.return_value = MagicMock(
        returncode=1, stdout="A real error", stderr="Something broke"
    )
    with patch.object(sys, "argv", ["commit_wrapper.py", "-m", "test commit"]):
        with pytest.raises(SystemExit) as e:
            commit_wrapper.main()
        assert e.value.code == 1

    assert mock_run.call_count == 1


@patch("assemblage.commit_wrapper.subprocess.run")
def test_failure_on_second_attempt(mock_run):
    """
    Tests that the script fails if the second commit attempt also fails.
    """
    mock_run.side_effect = [
        MagicMock(returncode=1, stdout="- files were modified by this hook", stderr=""),
        MagicMock(returncode=0),
        MagicMock(returncode=1, stderr="Still broken"),
    ]

    with patch.object(sys, "argv", ["commit_wrapper.py", "-m", "test commit"]):
        with pytest.raises(SystemExit) as e:
            commit_wrapper.main()
        assert e.value.code == 1

    assert mock_run.call_count == 3
