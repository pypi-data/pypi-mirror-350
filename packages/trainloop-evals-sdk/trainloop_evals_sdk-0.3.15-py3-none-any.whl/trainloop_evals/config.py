"""
YAML/env loader from `trainloop.config.yaml`:

    trainloop:
      data_folder: "./trainloop/data"
      host_allowlist: ["api.openai.com", "api.anthropic.com"]
      log_level: "info"
"""

from __future__ import annotations

import os
from pathlib import Path
import yaml
from .logger import create_logger
from .types import TrainloopConfig
from .instrumentation.utils import DEFAULT_HOST_ALLOWLIST

_log = create_logger("trainloop-config")


def resolve_data_folder_path(data_folder: str, config_path: str | None, root_dir: Path) -> str:
    """
    Resolves the data folder path based on whether it's absolute or relative.
    
    Args:
        data_folder: The data folder path from config
        config_path: The path to the config file, if provided
        root_dir: The current working directory
        
    Returns:
        The resolved data folder path as a string
    """
    if not data_folder:
        return ""
        
    data_folder_path = Path(data_folder)
    if data_folder_path.is_absolute():
        # If it's an absolute path, use it directly
        return str(data_folder_path)
    else:
        # If it's relative and config path was provided, make it relative to config directory
        if config_path:
            config_dir = Path(config_path).parent
            return str(config_dir / data_folder_path)
        else:
            # Otherwise, make it relative to current working directory
            return str(root_dir / data_folder_path)


def load_config_into_env(trainloop_config_path: str | None = None) -> None:
    root = Path.cwd()
    cfg = (
        Path(trainloop_config_path)
        if trainloop_config_path
        else root / "trainloop.config.yaml"
    )
    _log.info("Loading config from %s", cfg)
    if not cfg.exists():
        _log.warning("Config file not found")
        return

    data: TrainloopConfig = yaml.safe_load(cfg.read_text())
    tl = data.get("trainloop", {})
    # Set data folder path in environment variables
    data_folder = tl.get("data_folder", "")
    resolved_path = resolve_data_folder_path(data_folder, trainloop_config_path, root)
    os.environ.setdefault("TRAINLOOP_DATA_FOLDER", resolved_path)
    os.environ.setdefault(
        "TRAINLOOP_HOST_ALLOWLIST",
        ",".join(tl.get("host_allowlist", DEFAULT_HOST_ALLOWLIST)),
    )
    os.environ.setdefault(
        "TRAINLOOP_LOG_LEVEL", str(tl.get("log_level", "info")).upper()
    )
