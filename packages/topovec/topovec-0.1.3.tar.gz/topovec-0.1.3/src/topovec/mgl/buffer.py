import numpy as np
import moderngl as mgl

from ..core import System


class Field3DBuffer:
    def __init__(self, mglctx: mgl.Context = None, system: System = None):
        self._ctx = mglctx
        self._system = system
        self.vbo = self._ctx.buffer(reserve=12 * self._system.number_of_spins)

    def upload(self, state: np.ndarray):
        assert isinstance(state, np.ndarray)
        self.vbo.write(state.reshape((-1, 3)).astype("f4").tobytes())


class Field1DBuffer:
    def __init__(self, mglctx: mgl.Context = None, system: System = None):
        self._ctx = mglctx
        self._system = system
        self.vbo = self._ctx.buffer(reserve=4 * self._system.number_of_spins)

    def upload(self, state: np.ndarray):
        assert isinstance(state, np.ndarray)
        self.vbo.write(state.flatten().astype("f4").tobytes())


class Float3DBuffer:
    def __init__(self, mglctx: mgl.Context = None, count: int = None):
        self._ctx = mglctx
        self._count = count
        self.vbo = self._ctx.buffer(reserve=12 * self._count)

    def upload(self, data: np.ndarray):
        assert isinstance(data, np.ndarray)
        data = data.reshape((-1, 3))
        assert data.shape[0] == self._count
        self.vbo.write(data.astype("f4").tobytes())

    def download(self):
        return np.frombuffer(self.vbo.read(), dtype=np.float32).reshape(
            (-1, 3)
        )  # , count=self._count)


class IntBuffer:
    def __init__(self, mglctx: mgl.Context = None, count=None):
        self._ctx = mglctx
        self._count = count
        self.ibo = self._ctx.buffer(reserve=4 * self._count)

    @property
    def count(self):
        return self._count

    def upload(self, data: np.ndarray):
        assert isinstance(data, np.ndarray)
        data = data.flatten()
        assert data.shape == (self._count,)
        self.ibo.write(data.astype("i4").tobytes())

    def download(self):
        return np.frombuffer(self.ibo.read(), dtype=np.int32)  # , count=self._count)
