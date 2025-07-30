import os
import tempfile
from pathlib import Path

import pytest
import toml

from dtu_compute.config import Config, ConfigManager


@pytest.fixture
def sample_config_data():
    """Sample configuration data for testing."""
    return {
        "auth": {"auth_method": "ssh", "dtu_username": "testuser"},
        "hpc": {
            "host": "login.hpc.dtu.dk",
            "key_filename": "~/.ssh/id_rsa",
        },
        "titans": {
            "host": "titans.compute.dtu.dk",
            "key_filename": "~/.ssh/id_rsa",
        },
        "campus_ai": {
            "base_url": "https://campusai.dtu.dk",
            "api_key": "sample_api_key",
        },
        "repo": {
            "git_user": "testuser",
            "repository": "test_project",
            "token": "ghp_sample_token",
            "default_branch": "main",
        },
        "log": {
            "should_log": True,
            "log_file": "tmp_log.log",
        },
    }


@pytest.fixture
def temp_config_file():
    """Create a temporary file for config testing."""
    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as tmp:
        yield Path(tmp.name)
        # Clean up after test
        os.unlink(tmp.name)


class TestConfigManager:
    """Test suite for ConfigManager class."""

    def test_init(self):
        """Test initialization of ConfigManager."""
        config_manager = ConfigManager(Path("test.toml"))
        assert config_manager.config_file == Path("test.toml")

    def test_setup_config(self, temp_config_file, sample_config_data, monkeypatch):
        """Test setting up a configuration."""
        # Mock add_to_gitignore to avoid side effects
        monkeypatch.setattr("dtu_compute.config.add_to_gitignore", lambda x: None)

        config_manager = ConfigManager(temp_config_file)
        config_manager.setup_config(sample_config_data)

        # Verify the file was created and contains the expected data
        assert temp_config_file.exists()
        with open(temp_config_file) as f:
            saved_data = toml.load(f)

        # Check a few key values to ensure data was saved correctly
        assert saved_data["auth"]["auth_method"] == "ssh"
        assert saved_data["auth"]["dtu_username"] == "testuser"
        assert saved_data["repo"]["git_user"] == "testuser"
        assert saved_data["hpc"]["host"] == "login.hpc.dtu.dk"

    def test_load_config(self, temp_config_file, sample_config_data, monkeypatch):
        """Test loading a configuration from file."""
        # Mock add_to_gitignore to avoid side effects
        monkeypatch.setattr("dtu_compute.config.add_to_gitignore", lambda x: None)

        # First, set up the config
        config_manager = ConfigManager(temp_config_file)
        config_manager.setup_config(sample_config_data)

        # Now load it
        config = config_manager.load_config()

        # Check that the loaded config matches what we expect
        assert isinstance(config, Config)

        # Test auth configuration
        assert config.auth.auth_method == "ssh"
        assert config.auth.dtu_username == "testuser"

        # Test HPC configuration
        assert config.hpc.host == "login.hpc.dtu.dk"
        assert config.hpc.key_filename == "~/.ssh/id_rsa"

        # Test Titans configuration
        assert config.titans.host == "titans.compute.dtu.dk"
        assert config.titans.key_filename == "~/.ssh/id_rsa"

        # Test Campus AI configuration
        assert config.campus_ai.base_url == "https://campusai.dtu.dk"
        assert config.campus_ai.api_key == "sample_api_key"

        # Test repo configuration
        assert config.repo.git_user == "testuser"
        assert config.repo.repository == "test_project"
        assert config.repo.token == "ghp_sample_token"
        assert config.repo.default_branch == "main"

        # Test log configuration
        assert config.log.should_log is True

    def test_load_config_file_not_found(self):
        """Test that loading a non-existent config file raises an error."""
        config_manager = ConfigManager(Path("nonexistent.toml"))
        with pytest.raises(FileNotFoundError):
            config_manager.load_config()

    def test_config_validation(self, temp_config_file, monkeypatch):
        """Test that invalid config data is rejected."""
        # Mock add_to_gitignore to avoid side effects
        monkeypatch.setattr("dtu_compute.config.add_to_gitignore", lambda x: None)

        # Invalid config missing required fields
        invalid_config = {
            "auth": {"auth_method": "ssh"},
            # Missing other required sections
        }

        config_manager = ConfigManager(temp_config_file)
        with pytest.raises(Exception):  # Will fail validation
            config_manager.setup_config(invalid_config)

    def test_config_pydantic_models(self, sample_config_data, monkeypatch):
        """Test that all Pydantic models work correctly with the provided data."""
        # Mock add_to_gitignore to avoid side effects
        monkeypatch.setattr("dtu_compute.config.add_to_gitignore", lambda x: None)

        # Create config using Pydantic models directly
        config = Config(**sample_config_data)  # ty:ignore

        # Verify all models and fields were created correctly
        assert config.auth.dtu_username == "testuser"
        assert config.auth.auth_method == "ssh"

        assert config.hpc.host == "login.hpc.dtu.dk"
        assert config.hpc.key_filename == "~/.ssh/id_rsa"

        assert config.titans.host == "titans.compute.dtu.dk"
        assert config.titans.key_filename == "~/.ssh/id_rsa"

        assert config.campus_ai.base_url == "https://campusai.dtu.dk"
        assert config.campus_ai.api_key == "sample_api_key"

        # Test serialization/deserialization
        config_dict = config.model_dump()
        assert config_dict["auth"]["dtu_username"] == "testuser"
        assert config_dict["campus_ai"]["api_key"] == "sample_api_key"
