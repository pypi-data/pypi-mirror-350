from dataclasses import dataclass
import numpy as np

########################################################################################################


class Vertex:
    """
    Storage for vertex indices.
    """

    def __init__(self, cell, representative=0):
        self.representative = representative
        self.cell = np.asarray(cell, dtype=np.int32)

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return NotImplemented
        return (
            np.all(self.cell == other.cell)
            and self.representative == other.representative
        )

    # def validate(self, system:'System'):
    #     """
    #     Check if parameters match the lattice.
    #     """
    #     assert system.representatives >= 0
    #     assert system.representatives < system.rank
    #     assert system.cell.shape == (system.dim,)
    #     assert np.all(self.cell >= 0)
    #     assert np.all(self.cell < system.size)

    def flat_indices(self, system: "System", wrap=True):
        single = [c + np.arange(n) for c, n in zip(self.cell, system.size)]
        if not wrap:
            mask = (np.logical_or(c < 0, c >= s) for c, s in zip(single, system.size))
        single.append([self.representative])
        grid = np.meshgrid(*single, indexing="ij")
        result = np.ravel_multi_index(grid, system.size + (system.rank,), mode="wrap")[
            ..., 0
        ]
        if not wrap:
            mask = np.any(np.meshgrid(*mask, indexing="ij"), axis=0)
            result[mask] = -1
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}@{}".format(self.representative, ",".join(str(x) for x in self.cell))

    def coordinates(self, system):
        return system.representatives[self.representative] + np.dot(
            self.cell, system.primitives
        )

    def transposed(self, axes=None):
        return Vertex(self.cell[list(axes)], representative=self.representative)


########################################################################################################


class System:
    def __init__(
        self,
        size: tuple[int],
        primitives: list[tuple[float]],
        representatives: list[tuple[float]],
        triangulation: list[tuple[Vertex]],
    ):
        self.size = np.asarray(size, dtype=int)
        self.primitives = np.asarray(primitives, dtype=np.float32)
        self.representatives = np.asarray(representatives, dtype=np.float32)
        self.triangulation = triangulation

    @property
    def number_of_spins(self):
        return np.prod(self.size)

    @property
    def dim(self):
        return len(self.size)

    @property
    def rank(self):
        """Number of points in the fundamental cell."""
        return len(self.representatives)

    @classmethod
    def cubic(cls, size: tuple[int]):
        assert len(size) == 3
        return cls(
            size=size,
            primitives=[(1, 0, 0), (0, 1, 0), (0, 0, 1)],
            representatives=[(0, 0, 0)],
            triangulation=cls.default_trivial_cell_triangulation(3),
        )

    @classmethod
    def rectangular(cls, size: tuple[int]):
        return cls(
            size=size,
            primitives=[(1, 0, 0), (0, 1, 0), (0, 0, 1)],
            representatives=[(0, 0, 0)],
            triangulation=cls.default_trivial_cell_triangulation(2),
        )

    # Lattice operations.
    def _thinned_system(self, steps: np.ndarray, include: np.ndarray) -> "System":
        return self.__class__(
            size=self.size // steps,
            primitives=self.primitives * steps[:, None],
            representatives=self.representatives + include[None] @ self.primitives,
            triangulation=self.triangulation,
        )

    def _thinned_field(
        self, data: np.ndarray, steps: np.ndarray, include: np.ndarray
    ) -> np.ndarray:
        return data[
            tuple(slice(i, None, s) for s, i in zip(steps, include))
            + (slice(None), slice(None))
        ]

    def thinned(
        self, data: np.ndarray, steps: tuple[int], include: tuple[int] = None
    ) -> tuple[np.ndarray, "System"]:
        steps = np.asarray(steps, dtype=int)
        if steps.ndim == 0:
            steps = np.stack([steps] * 3, axis=0)

        D = self.dim
        if steps.shape != (D,):
            raise ValueError(
                "Number of coefficients in `steps` must be equal the grid dimensionality."
            )

        if np.any(steps <= 0):
            raise ValueError("`steps` must be positive.")

        if include is None:
            include = tuple(0 for _ in steps)
        include = np.asarray(include, dtype=int)

        if include.shape != (D,):
            raise ValueError(
                "Number of coefficients in `include` must be equal the grid dimensionality."
            )

        include %= steps

        return self._thinned_field(
            data=data, steps=steps, include=include
        ), self._thinned_system(steps=steps, include=include)

    # Surfaces generator.
    def get_inner_triangles(self, triangulation=None):
        results = []
        if triangulation is None:
            triangulation = self.triangulation()
        for vertices in triangulation:
            cells = np.array([v.cell for v in vertices])
            reprs = np.array([v.representative for v in vertices])
            cells -= np.min(cells, axis=0)[None]
            mx = self.size - np.max(cells, axis=0)
            mesh = np.meshgrid(*[np.arange(m) for m in mx], indexing="ij")
            D = cells.shape[0]
            triangles = np.empty(mesh[0].shape + (D,), dtype=np.int32)
            for d in range(D):
                meshm = list([mesh[k] + cells[d, k] for k in range(self.dim)])
                idx = meshm[0]
                for k in range(1, self.dim):
                    idx = idx * self.size[k] + meshm[k]
                idx = idx * self.rank + reprs[d]
                triangles[..., d] = idx
            results.append(triangles.reshape(-1, D))
        return np.concatenate(results, axis=0)

    def get_inner_simplices(self):
        return self.get_inner_triangles(
            triangulation=self.default_trivial_cell_simplices(self.dim)
        )

    @staticmethod
    def default_trivial_cell_triangulation(dim):
        if dim < 2:
            return []
        elif dim == 2:
            return [
                (Vertex([0, 0]), Vertex([1, 0]), Vertex([0, 1])),
                (Vertex([1, 1]), Vertex([0, 1]), Vertex([1, 0])),
            ]
        elif dim == 3:
            return [
                (Vertex([0, 0, 0]), Vertex([1, 0, 0]), Vertex([0, 1, 0])),
                (Vertex([1, 1, 0]), Vertex([0, 1, 0]), Vertex([1, 0, 0])),
                (Vertex([0, 0, 0]), Vertex([0, 1, 0]), Vertex([0, 0, 1])),
                (Vertex([0, 1, 1]), Vertex([0, 0, 1]), Vertex([0, 1, 0])),
                (Vertex([0, 0, 0]), Vertex([0, 0, 1]), Vertex([1, 0, 0])),
                (Vertex([1, 0, 1]), Vertex([1, 0, 0]), Vertex([0, 0, 1])),
            ]
        else:
            raise NotImplementedError(f"Grid dimension {dim} is not supported.")

    @staticmethod
    def default_trivial_cell_simplices(dim):
        if dim == 3:
            return [
                (
                    Vertex([0, 0, 0]),
                    Vertex([1, 0, 0]),
                    Vertex([0, 1, 0]),
                    Vertex([0, 0, 1]),
                ),
                (
                    Vertex([1, 1, 1]),
                    Vertex([1, 1, 0]),
                    Vertex([1, 0, 1]),
                    Vertex([0, 1, 1]),
                ),
                (
                    Vertex([0, 1, 1]),
                    Vertex([0, 1, 0]),
                    Vertex([1, 1, 0]),
                    Vertex([0, 0, 1]),
                ),
                (
                    Vertex([0, 1, 0]),
                    Vertex([1, 0, 0]),
                    Vertex([1, 1, 0]),
                    Vertex([0, 0, 1]),
                ),
                (
                    Vertex([1, 0, 0]),
                    Vertex([1, 0, 1]),
                    Vertex([1, 1, 0]),
                    Vertex([0, 0, 1]),
                ),
                (
                    Vertex([0, 1, 1]),
                    Vertex([1, 0, 1]),
                    Vertex([1, 1, 0]),
                    Vertex([0, 0, 1]),
                ),
            ]
        raise NotImplementedError(f"Grid dimension {dim} is not supported.")

    ###

    def spin_positions(self) -> np.ndarray:
        if self.dim == 1:
            pos = (
                self.representatives[None, :, :]
                + np.arange(self.size[0])[:, None, None, None]
                * self.primitives[0][None, None, None, :]
            )
        elif self.dim == 2:
            pos = (
                self.representatives[None, None, :, :]
                + np.arange(self.size[0])[:, None, None, None]
                * self.primitives[0][None, None, None, :]
                + np.arange(self.size[1])[None, :, None, None]
                * self.primitives[1][None, None, None, :]
            )
        elif self.dim == 3:
            pos = (
                self.representatives[None, None, None, :, :]
                + np.arange(self.size[0])[:, None, None, None, None]
                * self.primitives[0][None, None, None, None, :]
                + np.arange(self.size[1])[None, :, None, None, None]
                * self.primitives[1][None, None, None, None, :]
                + np.arange(self.size[2])[None, None, :, None, None]
                * self.primitives[2][None, None, None, None, :]
            )
        else:
            raise NotImplementedError(f"Unsupported lattice dimensionality {self.dim}.")
        return pos
