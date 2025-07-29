# type: ignore

# Do not remove -- required for torch library resolution to work
import torch  # noqa: F401
import vidur  # noqa: F401

from .version import __version__, __version_tuple__

__all__ = [
    "__version__",
    "__version_tuple__",
]
