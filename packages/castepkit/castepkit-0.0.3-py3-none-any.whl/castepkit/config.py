from pathlib import Path

import toml
from platformdirs import user_config_dir

CONFIG_PATH = Path(user_config_dir("castepkit")) / "config.toml"

__all__ = ["load_config", "get_exec_path", "use_mpi", "get_nproc"]


def load_config():
    if CONFIG_PATH.is_file():
        return toml.load(CONFIG_PATH)
    return {}


def get_exec_path(name: str) -> str:
    """Get path to external executable."""
    config = load_config()
    return config.get("executables", {}).get(name, name)


def use_mpi() -> bool:
    config = load_config()
    return config.get("mpirun", {}).get("enabled", False)


def get_nproc() -> int:
    config = load_config()
    return config.get("mpirun", {}).get("nproc", 1)
