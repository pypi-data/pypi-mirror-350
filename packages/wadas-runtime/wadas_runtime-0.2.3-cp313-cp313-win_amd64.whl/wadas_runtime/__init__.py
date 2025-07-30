import openvino  # noqa
from ._core import load_and_compile_model, WADASModelServer
from ._version import __version__

__all__ = ["WADASModelServer", "load_and_compile_model", "__version__"]
