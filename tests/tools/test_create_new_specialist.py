"""
test_create_new_specialist.py

Tests for the create_new_specialist utility.
"""

import io
from unittest.mock import patch
import pytest
import yaml
from assemblage.tools import create_new_specialist

@pytest.fixture
def mock_stdin(monkeypatch):
    """Fixture to mock sys.stdin for user input."""
    def mock_input(inputs):
        input_stream = io.StringIO("\n".join(inputs) + "\n")
        monkeypatch.setattr("sys.stdin", input_stream)
    return mock_input

@pytest.fixture
def temp_registry(tmp_path):
    """Fixture to create a temporary specialists.yml file."""
    registry_path = tmp_path / "config"
    registry_path.mkdir()
    registry_file = registry_path / "specialists.yml"
    initial_content = {"specialists": {"existing_specialist": {}}}
    with open(registry_file, "w") as f:
        yaml.dump(initial_content, f)
    
    with patch.object(create_new_specialist, "REGISTRY_FILE", registry_file):
        yield registry_file

def test_successful_creation(mock_stdin, temp_registry):
    """Tests that a new specialist is created successfully."""
    user_inputs = [
        "new_id",
        "A new description.",
        "knowledge/new_report.md",
        "This is the guide.",
        "EOF"
    ]
    mock_stdin(user_inputs)

    with pytest.raises(SystemExit) as e:
        create_new_specialist.main()
    
    assert e.value.code == 0

    with open(temp_registry, "r") as f:
        data = yaml.safe_load(f)
    
    assert "new_id" in data["specialists"]
    assert data["specialists"]["new_id"]["description"] == "A new description."
    assert "This is the guide." in data["specialists"]["new_id"]["guide_prompt"]

def test_id_already_exists(mock_stdin, temp_registry):
    """Tests that the script exits if the specialist ID already exists."""
    user_inputs = ["existing_specialist"]
    mock_stdin(user_inputs)

    with pytest.raises(SystemExit) as e:
        create_new_specialist.main()
        
    assert e.value.code == 1

def test_empty_id_fails(mock_stdin, temp_registry):
    """Tests that the script exits if the specialist ID is empty."""
    user_inputs = [""]
    mock_stdin(user_inputs)

    with pytest.raises(SystemExit) as e:
        create_new_specialist.main()
        
    assert e.value.code == 1
