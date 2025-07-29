import numpy as np

from .buffer import Float3DBuffer, IntBuffer


class Solid:
    pass


class SolidOfRevolution(Solid):
    SEGMENTS = []

    def vertices(self):
        result = []
        l = len(self.SEGMENTS)
        for n, s in enumerate(self.SEGMENTS):
            result.append(s)
            if n > 0 and n < l - 1:
                result.append(s)
        return result

    def normals(self):
        result = []
        for (x1, y1), (x2, y2) in zip(self.SEGMENTS[:-1], self.SEGMENTS[1:]):
            dx, dy = x2 - x1, y2 - y1
            l = np.sqrt(dx * dx + dy * dy)
            n = (dy / l, -dx / l)
            result.append(n)
            result.append(n)
        return result

    def __init__(self, mglctx=None, count=None):
        self.count = count
        self.mglctx = mglctx

        vs = self.vertices()
        ns = self.normals()
        l = len(vs)
        assert l == len(ns)

        self.pos = Float3DBuffer(mglctx=mglctx, count=l * self.count)
        self.normal = Float3DBuffer(mglctx=mglctx, count=l * self.count)
        self.idx = IntBuffer(mglctx=mglctx, count=(l - 1) * 6 * self.count)

        idx = np.empty((self.count, l - 1, 6), dtype=np.int32)
        rng = np.arange(self.count)
        for n in range(l - 1):
            idx[:, n, 0] = rng * l + n
            idx[:, n, 1] = rng * l + n + 1
            idx[:, n, 2] = (rng * l + n + l) % (l * self.count)

            idx[:, n, 3] = rng * l + n + 1
            idx[:, n, 4] = (rng * l + n + l) % (l * self.count)
            idx[:, n, 5] = (rng * l + n + l + 1) % (l * self.count)
        self.idx.upload(idx)

        angles = rng / self.count * 2 * np.pi
        c, s = np.cos(angles), np.sin(angles)
        pos = np.empty((self.count, l, 3), dtype=np.float32)
        normal = np.zeros((self.count, l, 3), dtype=np.float32)

        for n in range(l):
            pos[:, n, 0] = c * vs[n][1]
            pos[:, n, 1] = s * vs[n][1]
            pos[:, n, 2] = vs[n][0]

            normal[:, n, 0] = c * ns[n][1]
            normal[:, n, 1] = s * ns[n][1]
            normal[:, n, 2] = ns[n][0]

        self.pos.upload(pos)
        self.normal.upload(normal)


class ConicMesh(SolidOfRevolution):
    SEGMENTS = [(0.5, 0.0), (-0.5, 0.5)]


###############################################################################################################


class CylinderMesh(SolidOfRevolution):
    SEGMENTS = [(0.5, 0.0), (0.5, 0.25), (-0.5, 0.25), (-0.5, 0.0)]


###############################################################################################################


class DoubleConeMesh(SolidOfRevolution):
    SEGMENTS = [(0.5, 0.0), (0.0, 0.5), (-0.5, 0.0)]


class ArrowMesh(SolidOfRevolution):
    SEGMENTS = [(0.5, 0.0), (0.0, 0.5), (0.0, 0.25), (-0.5, 0.25), (-0.5, 0.0)]
