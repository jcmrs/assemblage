"""
test_nudge.py

Tests for the nudge utility.
"""

from unittest.mock import patch
import pytest
import yaml
from assemblage.tools import nudge

@pytest.fixture
def temp_configs(tmp_path):
    """Fixture to create temporary workbench and nudge config files."""
    workbench_file = tmp_path / "workbenches.yml"
    nudge_file = tmp_path / "nudges.yml"

    workbench_content = {
        "workbenches": {
            "architect": {"available_nudges": ["holistic_check"]},
            "builder": {"available_nudges": []},
        }
    }
    nudge_content = {"nudges": {"holistic_check": "This is a test nudge."}}

    with open(workbench_file, "w") as f:
        yaml.dump(workbench_content, f)
    with open(nudge_file, "w") as f:
        yaml.dump(nudge_content, f)

    with patch.object(nudge, "WORKBENCH_CONFIG", workbench_file), \
         patch.object(nudge, "NUDGE_LIBRARY", nudge_file):
        yield

def test_successful_nudge(capsys, temp_configs):
    """Tests that a valid nudge for a valid workbench is delivered."""
    with patch("sys.argv", ["nudge.py", "holistic_check", "architect"]):
        with pytest.raises(SystemExit) as e:
            nudge.main()
        
        assert e.value.code == 0
        captured = capsys.readouterr()
        assert "This is a test nudge." in captured.out

def test_blocked_nudge(capsys, temp_configs):
    """Tests that a nudge is blocked if not available for the workbench."""
    with patch("sys.argv", ["nudge.py", "holistic_check", "builder"]):
        with pytest.raises(SystemExit) as e:
            nudge.main()
            
        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Nudge 'holistic_check' is NOT available" in captured.err

def test_non_existent_nudge(capsys, temp_configs):
    """Tests that an error is raised for a nudge that doesn't exist."""
    with patch("sys.argv", ["nudge.py", "fake_nudge", "architect"]):
        with pytest.raises(SystemExit) as e:
            nudge.main()
            
        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Nudge 'fake_nudge' is NOT available" in captured.err

def test_no_arguments(capsys):
    """Tests that argparse exits if no arguments are provided."""
    with patch("sys.argv", ["nudge.py"]):
        with pytest.raises(SystemExit) as e:
            nudge.main()
        
        assert e.value.code != 0 # argparse exits with 2
        captured = capsys.readouterr()
        assert "usage: nudge.py" in captured.err
