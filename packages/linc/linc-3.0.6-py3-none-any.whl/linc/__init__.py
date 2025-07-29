from .write.writer_nc import write_nc_legacy
from .config import get_config
from . import config, parse, write

__version__ = "3.0.6"

__all__ = [
    "write_nc_legacy",
    "get_config",
    "parse",
    "write",
    "config",
]
