"""
test_analyze_feedback.py

Tests for the 'analyze_feedback' command.
"""

from unittest.mock import patch

import yaml

from assemblage.commands import analyze_feedback

MOCK_FEEDBACK_1 = {
    "ai_self_report": {},
    "vision_owner_review": {
        "clarity_rating": 5,
        "efficiency_rating": 4,
        "correctness_rating": 5,
        "improvement_areas": "Remember to update the documentation.",
    },
}

MOCK_FEEDBACK_2 = {
    "ai_self_report": {},
    "vision_owner_review": {
        "clarity_rating": 3,
        "efficiency_rating": 3,
        "correctness_rating": 4,
        "improvement_areas": (
            "The testing could be more thorough. " "Also, the documentation was missed."
        ),
    },
}


@patch("assemblage.commands.analyze_feedback.Path")
def test_calculate_stats(mock_path, capsys, tmp_path):
    """
    Tests that the aggregate stats are calculated and printed correctly.
    """
    # --- Setup ---
    feedback_dir = tmp_path / "feedback"
    feedback_dir.mkdir()
    (feedback_dir / "fb1.yml").write_text(yaml.dump(MOCK_FEEDBACK_1))
    (feedback_dir / "fb2.yml").write_text(yaml.dump(MOCK_FEEDBACK_2))

    # Mock the Path object to point to our temp dir
    mock_path.return_value = feedback_dir

    # --- Execution ---
    all_feedback = analyze_feedback._load_all_feedback()
    analyze_feedback._calculate_and_print_stats(all_feedback)

    # --- Assertions ---
    captured = capsys.readouterr()
    assert "Average Clarity Rating: 4.00 / 5.0" in captured.out
    assert "Average Efficiency Rating: 3.50 / 5.0" in captured.out
    assert "Average Correctness Rating: 4.50 / 5.0" in captured.out


@patch("assemblage.commands.analyze_feedback.Path")
def test_nudge_proposal(mock_path, capsys, tmp_path):
    """
    Tests that nudge proposals are generated from recurring keywords.
    """
    # --- Setup ---
    feedback_dir = tmp_path / "feedback"
    feedback_dir.mkdir()
    (feedback_dir / "fb1.yml").write_text(yaml.dump(MOCK_FEEDBACK_1))
    (feedback_dir / "fb2.yml").write_text(yaml.dump(MOCK_FEEDBACK_2))

    mock_path.return_value = feedback_dir

    # --- Execution ---
    all_feedback = analyze_feedback._load_all_feedback()
    analyze_feedback._analyze_and_propose_nudges(all_feedback)

    # --- Assertions ---
    captured = capsys.readouterr()
    assert "documentation" in captured.out
    assert "Found 2 times" in captured.out
    assert "testing" not in captured.out
