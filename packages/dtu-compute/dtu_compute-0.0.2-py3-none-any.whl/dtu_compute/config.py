from pathlib import Path

import toml
from pydantic import BaseModel

from dtu_compute.utils import add_to_gitignore


class AuthConfig(BaseModel):
    """Configuration for authentication."""

    dtu_username: str
    auth_method: str


class HPCSSHConfig(BaseModel):
    """Configuration for SSH connection to the HPC cluster."""

    host: str
    key_filename: str


class TitansSSHConfig(BaseModel):
    """Configuration for SSH connection to the Titans cluster."""

    host: str
    key_filename: str


class CampusAIConfig(BaseModel):
    """Configuration for SSH connection to the Campus AI cluster."""

    base_url: str
    api_key: str


class RepoConfig(BaseModel):
    """Configuration for repository integration."""

    git_user: str
    repository: str
    token: str
    default_branch: str


class LogConfig(BaseModel):
    """Configuration for logging."""

    should_log: bool
    log_file: Path


class Config(BaseModel):
    """Complete configuration for DTU Compute interaction."""

    auth: AuthConfig
    hpc: HPCSSHConfig
    titans: TitansSSHConfig
    campus_ai: CampusAIConfig
    repo: RepoConfig
    log: LogConfig


class ConfigManager:
    """Configuration manager for DTU Compute.

    Args:
        config_file: Path to the config file. If None, will search in default locations.

    """

    def __init__(self, config_file: Path = Path("dtu.toml")):
        self.config_file = config_file

    def setup_config(self, config_data: dict[str, dict]) -> None:
        """Set up configuration and save it to the config file.

        Args:
            config_data: Dictionary containing configuration data

        """
        # Validate with Pydantic
        config = Config(**config_data)  # type: ignore

        # Write to file
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            toml.dump(config.model_dump(), f)

        # Add to .gitignore
        add_to_gitignore(self.config_file)

    def load_config(self) -> Config:
        """Load configuration from the config file.

        Returns:
            Config: The loaded configuration

        """
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")

        with open(self.config_file) as f:
            config_data = toml.load(f)

        return Config(**config_data)  # type: ignore
