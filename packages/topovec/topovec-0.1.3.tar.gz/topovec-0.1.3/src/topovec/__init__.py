from .core import log, System

__all__ = ["log", "System"]

#########################################################################################################################
# Load plugins

import importlib
from importlib.util import find_spec
from importlib.metadata import entry_points
import sys


class LazyModule:
    def __init__(self, name: str, extra: str):
        self.name = name
        self.extra = extra
        self.module = None

    def __getattr__(self, attr):
        if self.module is None:
            log.debug(f"Importing plugin {self.name}")
            s = find_spec(self.name)
            if s:
                self.module = importlib.import_module(self.name)
            else:
                raise ImportError(
                    f"Plugin {self.name} is not found. Install the library with `uv sync --extra {self.extra}` or `uv sync --all-extras`"
                )
        return getattr(self.module, attr)


def load_plugins():
    plugins = {}
    for ep in entry_points(group="my_library_plugins"):
        module = LazyModule(ep.value, ep.name)
        setattr(sys.modules[__name__], ep.name, module)
    return plugins


load_plugins()
