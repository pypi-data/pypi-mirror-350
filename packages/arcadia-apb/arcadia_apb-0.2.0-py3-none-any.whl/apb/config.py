from pathlib import Path

HOME = Path.home()

CONFIG_DIR = HOME / ".config" / "apb"


def ensure_config_dir_exists() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
