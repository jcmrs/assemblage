"""
assemblage.config_manager

Provides a reusable utility for safely managing YAML configuration files.
"""

from pathlib import Path

import yaml


class ConfigManager:
    """A manager for reading, writing, and modifying YAML config files."""

    def __init__(self, config_path: Path):
        """
        Initializes the manager for a specific YAML config file.
        If the file doesn't exist, it will be created.
        """
        self.path = config_path
        if not self.path.exists():
            # Ensure parent directory exists
            self.path.parent.mkdir(parents=True, exist_ok=True)
            # Create the file with an empty dict
            self.path.write_text(yaml.dump({}))

    def read_config(self) -> dict:
        """Reads and parses the YAML file."""
        with open(self.path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            # Ensure we always return a dict, even if the file is empty
            return config if isinstance(config, dict) else {}

    def write_config(self, data: dict):
        """Writes a dictionary to the YAML file."""
        with open(self.path, "w", encoding="utf-8") as f:
            # Use a standard format for consistency
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

    def add_entry(self, key: str, value: any, unique: bool = True):
        """
        Adds a new top-level entry.
        Raises KeyError if 'unique' is True and the key already exists.
        """
        config = self.read_config()
        if unique and key in config:
            raise KeyError(f"Entry '{key}' already exists in {self.path.name}.")
        config[key] = value
        self.write_config(config)

    def remove_entry(self, key: str):
        """
        Removes a top-level entry.
        Raises KeyError if the key does not exist.
        """
        config = self.read_config()
        if key not in config:
            raise KeyError(f"Entry '{key}' not found in {self.path.name}.")
        del config[key]
        self.write_config(config)

    def update_entry(self, key: str, value: any):
        """
        Updates an existing top-level entry.
        Raises KeyError if the key does not exist.
        """
        config = self.read_config()
        if key not in config:
            raise KeyError(f"Entry '{key}' not found in {self.path.name}.")
        config[key] = value
        self.write_config(config)
