"""
tests.test_config_manager

Tests for the reusable YAML configuration management utility.
"""

import pytest
import yaml

from assemblage.config_manager import ConfigManager


@pytest.fixture
def temp_config_file(tmp_path):
    """Creates a temporary YAML config file for testing."""
    config_path = tmp_path / "test_config.yml"
    initial_data = {"key1": "value1", "key2": {"nested_key": "nested_value"}}
    config_path.write_text(yaml.dump(initial_data))
    return config_path


def test_read_config(temp_config_file):
    """Tests that the config file is read correctly."""
    manager = ConfigManager(temp_config_file)
    config = manager.read_config()
    assert config["key1"] == "value1"
    assert config["key2"]["nested_key"] == "nested_value"


def test_add_entry(temp_config_file):
    """Tests adding a new entry."""
    manager = ConfigManager(temp_config_file)
    manager.add_entry("key3", "new_value")
    config = manager.read_config()
    assert "key3" in config
    assert config["key3"] == "new_value"


def test_add_duplicate_raises_error(temp_config_file):
    """Tests that adding a duplicate key raises a KeyError."""
    manager = ConfigManager(temp_config_file)
    with pytest.raises(KeyError, match="Entry 'key1' already exists"):
        manager.add_entry("key1", "another_value")


def test_remove_entry(temp_config_file):
    """Tests removing an existing entry."""
    manager = ConfigManager(temp_config_file)
    manager.remove_entry("key1")
    config = manager.read_config()
    assert "key1" not in config


def test_remove_nonexistent_raises_error(temp_config_file):
    """Tests that removing a non-existent key raises a KeyError."""
    manager = ConfigManager(temp_config_file)
    with pytest.raises(KeyError, match="Entry 'nonexistent' not found"):
        manager.remove_entry("nonexistent")


def test_update_entry(temp_config_file):
    """Tests updating an existing entry."""
    manager = ConfigManager(temp_config_file)
    manager.update_entry("key1", "updated_value")
    config = manager.read_config()
    assert config["key1"] == "updated_value"


def test_update_nonexistent_raises_error(temp_config_file):
    """Tests that updating a non-existent key raises a KeyError."""
    manager = ConfigManager(temp_config_file)
    with pytest.raises(KeyError, match="Entry 'nonexistent' not found"):
        manager.update_entry("nonexistent", "some_value")


def test_init_creates_file_if_not_exists(tmp_path):
    """Tests that the manager creates a new config file if it doesn't exist."""
    new_config_path = tmp_path / "new_config.yml"
    assert not new_config_path.exists()
    manager = ConfigManager(new_config_path)
    assert new_config_path.exists()
    # The created file should contain an empty dictionary
    config = manager.read_config()
    assert isinstance(config, dict)
    assert not config
