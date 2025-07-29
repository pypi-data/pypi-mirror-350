import sadcompressor as sad
import numpy as np

from ..core import System


def load_lcsim_sad_single(
    reader: sad.ContainerReader,
) -> tuple[np.ndarray, System, dict]:
    x, y, z = list(reader[n] for n in ["x", "y", "z"])
    director = np.stack([x, y, z], axis=-1).transpose((2, 1, 0, 3))[:, :, :, None]
    settings = reader["s"]
    system = System.cubic(size=director.shape[:3])
    return director, system, settings
