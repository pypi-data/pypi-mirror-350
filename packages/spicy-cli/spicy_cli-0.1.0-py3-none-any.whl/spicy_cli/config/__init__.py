"""Configuration utilities for the Spicy CLI."""

import json
import os
from pathlib import Path

import pydantic
from pydantic import BaseModel


class SpicyConfig(BaseModel):
    """Configuration model for the Spicy CLI."""

    debug: bool = False
    timeout: int = 30
    default_command: str = "command1"
    log_level: str = "INFO"
    max_retries: int = 3


def get_config_path() -> Path:
    """Get the path to the config file.

    Returns:
        Path to the config file
    """
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        config_dir = Path(xdg_config_home) / "spicy-cli"
    else:
        config_dir = Path.home() / ".config" / "spicy-cli"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config(config_path: Path | None = None) -> SpicyConfig:
    """Load configuration from a file.

    Args:
        config_path: Optional path to a config file

    Returns:
        SpicyConfig object
    """
    if config_path is None:
        config_path = get_config_path()

    if not config_path.exists():
        return SpicyConfig()

    try:
        with open(config_path, encoding="utf-8") as f:
            config_data = json.load(f)
        return SpicyConfig(**config_data)
    except (json.JSONDecodeError, pydantic.ValidationError):
        # Return default config if there's an error parsing the config file
        return SpicyConfig()


def save_config(config: SpicyConfig, config_path: Path | None = None) -> None:
    """Save configuration to a file.

    Args:
        config: SpicyConfig object to save
        config_path: Optional path to a config file
    """
    if config_path is None:
        config_path = get_config_path()

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, indent=2)
