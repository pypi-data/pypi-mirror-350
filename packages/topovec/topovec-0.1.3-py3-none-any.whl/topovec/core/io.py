import numpy as np
import json

from .log import log
from .system import System


def load_magnes_npz(filename, path="PATH") -> tuple[np.ndarray, System]:
    raise NotImplementedError


def load_lcsim_npz(filename, path="PATH") -> tuple[np.ndarray, System, dict]:
    log.debug(f"Open '{filename}'")
    datafile = np.load(filename, allow_pickle=True)
    log.debug(f"Available keys {*datafile.keys(),}")
    images = datafile[path]
    if images.ndim != 6 or images.shape[-1] != 3:
        raise ValueError(f"Shape {images.shape} of '{path}' is not supported.")
    settings = json.loads(datafile["settings"][()]) if "settings" in datafile else None
    system = System.cubic(size=images.shape[1:4])
    return list(images), system, settings
