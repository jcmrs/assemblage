"""
test_feedback.py

Tests for the 'feedback' command.
"""

from unittest.mock import MagicMock, patch

from assemblage.commands import feedback


@patch("assemblage.commands.feedback.subprocess.run")
def test_generate_self_report(mock_run):
    """
    Tests that the self-report function correctly parses git output.
    """
    # --- Setup Mocks ---
    # Mock for 'git cat-file -e' (just needs to succeed)
    mock_cat_file = MagicMock(stdout="")

    # Mock for 'git show -s --format=%B'
    mock_commit_msg = MagicMock(
        stdout="feat(test): My test commit\n\nThis is for ITEM-123."
    )

    # Mock for 'git show --shortstat'
    mock_stat = MagicMock(
        stdout="...\n 1 file changed, 10 insertions(+), 5 deletions(-)"
    )

    # Mock for 'git show --name-only'
    mock_files = MagicMock(stdout="commit-hash\nREADME.md\ntests/test_new.py")

    mock_run.side_effect = [mock_cat_file, mock_commit_msg, mock_stat, mock_files]

    # --- Execution ---
    report = feedback._generate_self_report("fake_hash")

    # --- Assertions ---
    assert report["task_id"] == "ITEM-123"
    assert report["files_changed"] == 1
    assert report["lines_added"] == 10
    assert report["lines_deleted"] == 5
    assert report["tests_impacted"] == 1
    assert report["self_correction_loops"] == "N/A"


@patch("builtins.input")
def test_prompt_vision_owner_review(mock_input):
    """
    Tests that the user prompting function correctly gathers data.
    """
    # --- Setup Mocks ---
    mock_input.side_effect = [
        "5",  # Clarity
        "4",  # Efficiency
        "3",  # Correctness
        "Good work.",
        "EOF",  # Positive notes
        "Could be faster.",
        "EOF",  # Improvement areas
    ]

    # --- Execution ---
    review = feedback._prompt_vision_owner_review()

    # --- Assertions ---
    assert review["clarity_rating"] == 5
    assert review["efficiency_rating"] == 4
    assert review["correctness_rating"] == 3
    assert review["positive_notes"] == "Good work."
    assert review["improvement_areas"] == "Could be faster."


@patch("assemblage.commands.feedback._generate_self_report")
@patch("assemblage.commands.feedback._prompt_vision_owner_review")
@patch("assemblage.commands.feedback._save_feedback")
def test_run_orchestration(mock_save, mock_prompt, mock_report):
    """
    Tests that the main run function calls its helpers in the correct order.
    """
    # --- Setup Mocks ---
    mock_report.return_value = {"key": "value"}
    mock_prompt.return_value = {"key2": "value2"}

    args = MagicMock()
    args.commit = "fake_hash"

    # --- Execution ---
    with patch.object(feedback.sys, "exit") as mock_exit:
        feedback.run(args)

    # --- Assertions ---
    mock_report.assert_called_once_with("fake_hash")
    mock_prompt.assert_called_once()

    # Check that the combined payload was saved
    expected_payload = {
        "ai_self_report": {"key": "value"},
        "vision_owner_review": {"key2": "value2"},
    }
    mock_save.assert_called_once_with(expected_payload)

    mock_exit.assert_called_once_with(0)
