import re
from abc import ABC
from pathlib import Path

import yaml
from pydantic import BaseModel


class Walltime(BaseModel):
    """Configuration for job walltime."""

    hours: int
    minutes: int
    seconds: int


class Notification(BaseModel):
    """Configuration for job notifications."""

    email: str
    email_on_start: bool
    email_on_end: bool


class GPU(BaseModel):
    """Configuration for GPU resources."""

    num_gpus: int
    gpu_type: str


class JobConfig(BaseModel):
    """Configuration for a job to be submitted to a scheduler."""

    name: str
    queue: str
    single_host: bool
    walltime: Walltime
    std_out: str
    std_err: str
    memory: int
    memory_kill_limit: float
    cores: int
    notification: Notification
    core_block_size: int
    core_p_tile_size: int
    gpu: GPU
    commands: list[str]


class ConfigProcessor(ABC):
    """Abstract base class for processing configuration files."""

    config: dict
    processed_config: dict | None = None

    def __init__(self, config_path: Path):
        """Initialize the ConfigProcessor with either a path to a config file or a config dictionary.

        Args:
            config_path: Path to the YAML config file
            config_dict: Dictionary containing configuration (alternative to config_path)

        """
        with config_path.open("r") as f:
            self.config = yaml.safe_load(f)

    def _substitute_placeholders(self, config, substitutions):
        """Recursively traverse the config and replace placeholders in strings with values from substitutions."""
        if isinstance(config, dict):
            return {k: self._substitute_placeholders(v, substitutions) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._substitute_placeholders(item, substitutions) for item in config]
        elif isinstance(config, str):
            # Replace all occurrences of ${key} with the corresponding substitution value
            def replacer(match):
                key = match.group(1)
                return str(substitutions.get(key, match.group(0)))

            return re.sub(r"\$\{([^}]+)\}", replacer, config)
        else:
            return config

    def process(self) -> None:
        """Process the config by substituting placeholders."""
        config_copy = self.config.copy()
        substitutions = config_copy.pop("substitutions", {})

        if substitutions:
            self.processed_config = self._substitute_placeholders(config_copy, substitutions)
        else:
            self.processed_config = config_copy

    def get_job_config(self):
        """Return a JobConfig object built from the processed configuration."""
        if self.processed_config is None:
            self.process()

        if isinstance(self.processed_config, list):
            return [JobConfig(**job) for job in self.processed_config]  # type: ignore
        return JobConfig(**self.processed_config)  # type: ignore
