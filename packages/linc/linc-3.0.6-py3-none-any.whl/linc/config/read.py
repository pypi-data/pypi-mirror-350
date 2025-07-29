from functools import lru_cache
from pathlib import Path

from tomli import load
from .models import Config

FALLBACK_CONFIG = Path(__file__).parent / "default-config.toml"
CURRENT_DIR_CONFIG = Path("./lidar-conf.toml")


@lru_cache
def get_config(file: Path | str | None = None, use_default: bool = False) -> Config:
    if file is not None:
        _cf = Path(file)
        if _cf.exists():
            config_path = _cf
        elif CURRENT_DIR_CONFIG.exists():
            config_path = CURRENT_DIR_CONFIG
        else:
            if use_default:
                config_path = FALLBACK_CONFIG
            else:
                raise FileNotFoundError()
    else:
        if use_default:
            config_path = FALLBACK_CONFIG
        else:
            raise FileNotFoundError()

    with open(config_path, "rb") as f:
        settings_dict = load(f)

    return Config(**settings_dict)
