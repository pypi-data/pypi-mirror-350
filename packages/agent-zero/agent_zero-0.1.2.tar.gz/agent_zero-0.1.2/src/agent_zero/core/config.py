"""
This module provides functionality to parse the application's YAML configuration file.
It allows loading the configuration from a specified path or, by default, from
the project's root directory (config.yaml).
"""

import os
import yaml

__all__ = ["load_config", "init_config", "get_config", "config"]

_config_cache: dict[str, dict] | None = None
_cached_config_path: str | None = None


def _parse_config_file(config_file_path: str | None = None) -> dict:
    """
    Parse a single YAML configuration file and return its contents as a dictionary.

    Args:
        config_file_path (str | None): Path to the configuration file.
            If not provided, defaults to 'config.yaml' in the project root directory.

    Returns:
        dict: The parsed configuration data.
    """
    if config_file_path is None:
        # If no path is provided, derive the default config.yaml path relative to this file's directory
        base_dir = os.path.dirname(__file__)
        config_file_path = os.path.abspath(
            os.path.join(base_dir, os.pardir, "config.yaml")
        )
    else:
        config_file_path = os.path.abspath(config_file_path)
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def load_config(config_file_path: str) -> dict:
    """
    Load YAML configuration file and return its contents as a dictionary.
    Uses a cache to avoid reloading the same file multiple times.

    Args:
        config_file_path: Path to the configuration file.

    Returns:
        dict: The parsed configuration data.
    """
    global _config_cache, _cached_config_path
    config_file_path = os.path.abspath(config_file_path)
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    if _cached_config_path == config_file_path and _config_cache is not None:
        return _config_cache

    config = _parse_config_file(config_file_path)
    _config_cache = config
    _cached_config_path = config_file_path
    return config


# New API for initializing and retrieving config
def init_config(config_file_path: str) -> None:
    """
    Initialize the configuration by loading the given YAML file.
    Subsequent calls to get_config() will return this data.
    """
    # Use load_config to populate the cache
    load_config(config_file_path)


def get_config() -> dict:
    """
    Retrieve the initialized configuration.
    Raises an error if init_config() has not been called.
    """
    if _config_cache is None:
        raise RuntimeError("Configuration not initialized. Call init_config() first.")
    return _config_cache


# Lazily expose `config` by calling get_config() when accessed.
# def __getattr__(name: str):
#     """
#     Lazily expose `config` by calling get_config() when accessed.
#     """
#     if name == "config":
#         return get_config()
#     raise AttributeError(f"module {__name__} has no attribute {name}")
