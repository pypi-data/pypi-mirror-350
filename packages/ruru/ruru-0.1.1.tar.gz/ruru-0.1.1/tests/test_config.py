"""Tests for configuration management."""

import os
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml

from ruru.config import Config, ConfigManager


class TestConfig:
    """Test the Config data class."""

    def test_config_default_values(self):
        """Test that Config has sensible default values."""
        config = Config()
        assert config.api_url == "https://api.ruru.dev"
        assert config.api_timeout == 30
        assert config.default_location == "./"
        assert config.auto_create_dirs is True
        assert config.sync_on_get is False
        assert config.output_format == "table"
        assert config.color is True
        assert config.verbose is False
        assert config.cache_enabled is True
        assert config.cache_ttl == 300
        assert config.use_keyring is True
        assert config.verify_ssl is True

    def test_config_from_dict(self):
        """Test creating Config from dictionary."""
        data = {
            "api": {"url": "https://custom.api.com", "timeout": 60},
            "defaults": {"location": "./prompts", "auto_create_dirs": False},
            "output": {"format": "json", "color": False},
        }
        config = Config.from_dict(data)
        assert config.api_url == "https://custom.api.com"
        assert config.api_timeout == 60
        assert config.default_location == "./prompts"
        assert config.auto_create_dirs is False
        assert config.output_format == "json"
        assert config.color is False

    def test_config_to_dict(self):
        """Test converting Config to dictionary."""
        config = Config(
            api_url="https://test.com", api_timeout=45, output_format="yaml"
        )
        data = config.to_dict()
        assert data["api"]["url"] == "https://test.com"
        assert data["api"]["timeout"] == 45
        assert data["output"]["format"] == "yaml"


class TestConfigManager:
    """Test the ConfigManager class."""

    def test_config_manager_init(self, temp_dir: Path):
        """Test ConfigManager initialization."""
        config_dir = temp_dir / ".ruru"
        manager = ConfigManager(config_dir)
        assert manager.config_dir == config_dir
        assert isinstance(manager.config, Config)

    def test_get_config_dir_default(self, monkeypatch):
        """Test getting default config directory."""
        home_dir = Path("/fake/home")
        monkeypatch.setattr("pathlib.Path.home", lambda: home_dir)

        manager = ConfigManager()
        expected = home_dir / ".ruru"
        assert manager.config_dir == expected

    def test_get_config_dir_env_var(self, monkeypatch, temp_dir: Path):
        """Test getting config directory from environment variable."""
        config_dir = temp_dir / "custom_config"
        monkeypatch.setenv("RURU_CONFIG_DIR", str(config_dir))

        manager = ConfigManager()
        assert manager.config_dir == config_dir

    def test_load_config_file_not_exists(self, temp_dir: Path, isolated_env):
        """Test loading config when file doesn't exist."""
        config_dir = temp_dir / ".ruru"
        manager = ConfigManager(config_dir)
        manager.load()

        # Should use default config
        assert manager.config.api_url == "https://api.ruru.dev"

    def test_load_config_file_exists(self, temp_dir: Path, isolated_env):
        """Test loading config from existing file."""
        config_dir = temp_dir / ".ruru"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "config.yaml"
        config_data = {
            "api": {"url": "https://custom.api.com", "timeout": 60},
            "output": {"format": "json"},
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_dir)
        manager.load()

        assert manager.config.api_url == "https://custom.api.com"
        assert manager.config.api_timeout == 60
        assert manager.config.output_format == "json"

    def test_save_config(self, temp_dir: Path):
        """Test saving config to file."""
        config_dir = temp_dir / ".ruru"
        manager = ConfigManager(config_dir)

        manager.config.api_url = "https://test.api.com"
        manager.config.output_format = "yaml"
        manager.save()

        # Verify file was created
        config_file = config_dir / "config.yaml"
        assert config_file.exists()

        # Verify content
        with open(config_file) as f:
            data = yaml.safe_load(f)

        assert data["api"]["url"] == "https://test.api.com"
        assert data["output"]["format"] == "yaml"

    def test_get_api_key_from_keyring(self, mock_keyring, isolated_env):
        """Test getting API key from keyring."""
        mock_keyring["get"].return_value = "test-api-key"

        manager = ConfigManager()
        api_key = manager.get_api_key()

        assert api_key == "test-api-key"
        mock_keyring["get"].assert_called_once_with("ruru", "api_key")

    def test_get_api_key_from_env_var(self, mock_keyring, monkeypatch):
        """Test getting API key from environment variable."""
        mock_keyring["get"].return_value = None
        monkeypatch.setenv("RURU_API_KEY", "env-api-key")

        manager = ConfigManager()
        api_key = manager.get_api_key()

        assert api_key == "env-api-key"

    def test_get_api_key_priority_env_over_keyring(self, mock_keyring, monkeypatch):
        """Test that environment variable takes priority over keyring."""
        mock_keyring["get"].return_value = "keyring-key"
        monkeypatch.setenv("RURU_API_KEY", "env-key")

        manager = ConfigManager()
        api_key = manager.get_api_key()

        assert api_key == "env-key"

    def test_set_api_key_to_keyring(self, mock_keyring):
        """Test setting API key to keyring."""
        manager = ConfigManager()
        manager.set_api_key("new-api-key")

        mock_keyring["set"].assert_called_once_with("ruru", "api_key", "new-api-key")

    def test_clear_api_key_from_keyring(self, mock_keyring):
        """Test clearing API key from keyring."""
        manager = ConfigManager()
        manager.clear_api_key()

        mock_keyring["delete"].assert_called_once_with("ruru", "api_key")

    def test_get_config_from_env_vars(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("RURU_API_URL", "https://env.api.com")
        monkeypatch.setenv("RURU_API_TIMEOUT", "120")
        monkeypatch.setenv("RURU_OUTPUT_FORMAT", "json")
        monkeypatch.setenv("RURU_NO_COLOR", "1")
        monkeypatch.setenv("RURU_CACHE_ENABLED", "false")

        manager = ConfigManager()
        config = manager._get_config_from_env()

        assert config.api_url == "https://env.api.com"
        assert config.api_timeout == 120
        assert config.output_format == "json"
        assert config.color is False
        assert config.cache_enabled is False
