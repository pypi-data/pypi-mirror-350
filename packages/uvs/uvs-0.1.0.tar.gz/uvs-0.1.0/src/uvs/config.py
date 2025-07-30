"""Configuration management for uvs."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class UVSConfig:
    github_token: str | None = None
    default_auth: str = "auto"  # "auto", "ssh", "https"
    bin_dir: str | None = None
    scripts_dir: str | None = None


class ConfigManager:
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> UVSConfig:
        """Load configuration from file"""
        if not self.config_file.exists():
            return UVSConfig()

        try:
            with open(self.config_file) as f:
                data = json.load(f)
            return UVSConfig(**data)
        except (json.JSONDecodeError, TypeError):
            return UVSConfig()

    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, "w") as f:
            json.dump(asdict(self._config), f, indent=2)

    def get(self, key: str) -> Any:
        """Get configuration value"""
        return getattr(self._config, key, None)

    def set(self, key: str, value: Any):
        """Set configuration value"""
        if hasattr(self._config, key):
            setattr(self._config, key, value)
            self.save_config()
        else:
            raise KeyError(f"Unknown configuration key: {key}")

    @property
    def github_token(self) -> str | None:
        return self._config.github_token

    @github_token.setter
    def github_token(self, value: str | None):
        self._config.github_token = value
        self.save_config()
