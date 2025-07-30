from importlib.metadata import PackageNotFoundError, version

__all__ = [
    "Resume",
    "RenderCtx",
    "get_default_resume",
    "generate_typ",
    "generate",
    "dump_empty_json",
    "dump_empty_yaml",
    "dump_empty_toml",
]

from .models import Resume, RenderCtx, get_default_resume
from .render import (
    generate_typ,
    generate,
)
from .utils import (
    dump_empty_json,
    dump_empty_yaml,
    dump_empty_toml,
)

try:
    __version__ = version("cv_model")
except PackageNotFoundError:
    __version__ = "unknown"
