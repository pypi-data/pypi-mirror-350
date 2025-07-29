import numpy as np

from ..core import System


def snap_vector(vec, tol=0.4):
    target = np.round(2 * vec) / 2
    target /= np.linalg.norm(target)
    return target if np.linalg.norm(target - vec) < tol else vec


class Camera:
    def __init__(
        self,
        look_at=[0, 0, 0],
        look_direction=[0, 0, 1],
        look_up=[1, 0, 0],
        scale=1.0,
        perspective=True,
    ):
        """
        Initialize camera position.
        """
        self.depth = 1000
        self.MAG = 1.5
        self.MAGA = (self.MAG + 1.0 / self.MAG) / 2
        self.perspective_is_on = perspective
        self.look_at = np.asarray(look_at, dtype=np.float32)
        self.look_direction = np.asarray(look_direction, dtype=np.float32)
        self.look_up = np.asarray(look_up, dtype=np.float32)
        self.look_scale = scale
        self.normalize()
        # self.set_predefined_direction(2)

    @classmethod
    def from_angles(self, theta, phi, alpha, scale, perspective, look_at):
        camera = Camera(scale=scale, perspective=perspective, look_at=look_at)
        camera.set_orientation_by_angles(theta=theta, phi=phi, alpha=alpha)
        return camera

    def __str__(self):
        return self.__repr__()
        # return "along {} up {} at {} scale {} per. {}".format(self.look_direction, self.look_up, self.look_at, self.look_scale, self.perspective_is_on)

    def __repr__(self):
        theta, phi, alpha = self.get_orientation_angles()
        return f"Camera.from_angles(theta={theta}, phi={phi}, alpha={alpha}, scale={self.look_scale}, look_at={self.look_at.tolist()}, perspective={self.perspective_is_on})"

    def _complete_basis(self, depth) -> tuple[np.ndarray, np.ndarray]:
        z = np.array([0, 0, 1], dtype=np.float32)
        y = np.array([0, 1, 0], dtype=np.float32)
        depth = np.asarray(depth)
        b = z if abs(np.sum(depth * z)) < abs(np.sum(depth * y)) else y
        r = np.cross(depth, b)
        r /= np.sqrt(np.sum(r**2))
        u = np.cross(r, depth)
        u /= np.sqrt(np.sum(u**2))
        return u, r

    def set_orientation_by_angles(self, theta, phi, alpha):
        """Set camera basis in terms of three angles.

        Arguments:
            theta - polar angle of viewing direction,
            phi -  azimuthal angle of viewing direction.
            alpha - angle between direction up and polar axis (z).
        """
        depth = np.array(
            [np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta)],
            dtype=np.float32,
        )
        u, r = self._complete_basis(depth)
        up = np.cos(alpha) * u + np.sin(alpha) * r
        return self.set_basis(depth=depth, up=up)

    def get_orientation_angles(self):
        """Inverse function to `Camera.set_orientation_by_angles`."""
        depth = self.look_direction
        up = self.look_up
        theta = np.arccos(depth[2])
        phi = np.arctan2(depth[1], depth[0])
        u, r = self._complete_basis(depth)
        alpha = np.arctan2(np.sum(r * up), np.sum(u * up))
        return theta, phi, alpha

    def snap_orientation(self) -> "Camera":
        self.look_direction = snap_vector(self.look_direction)
        self.look_up = snap_vector(self.look_up)
        self.normalize()
        return self

    def set_predefined_direction(self, preset: int) -> "Camera":
        if preset == 2:
            depth = [0, 0, -1]
            up = [0, 1, 0]
        elif preset == 1:
            depth = [0, 1, 0]
            up = [0, 0, 1]
        elif preset == 0:
            depth = [-1, 0, 0]
            up = [0, 0, -1]
        elif preset == 3:
            depth = [-1, 1, -1]
            up = [0, 0, 1]
        else:
            raise ValueError(f"Preset `{preset}` is unknown")
        self.set_basis(depth=depth, up=up)
        return self

    def reset_FOV(self, system: System) -> "Camera":
        """
        Set default field of view.
        """
        self.reset_center_of_FOV(system)
        self.reset_direction_of_FOV(system)
        return self

    def reset_center_of_FOV(self, system: System) -> "Camera":
        self.look_at = np.dot(np.asarray(system.size) - 1, system.primitives) / 2
        return self

    def reset_direction_of_FOV(self, system: System) -> "Camera":
        primitives = [p for p in system.primitives]
        if len(primitives) < 3:
            primitives.append(np.array([0.0, 0.0, 1.0]))
        self.look_direction = -np.cross(primitives[0], primitives[2])
        self.look_direction /= np.linalg.norm(self.look_direction)
        self.look_up = primitives[2]
        self.look_up /= np.linalg.norm(self.look_up)
        self.look_scale = np.linalg.norm(self.look_at) / np.sqrt(2)
        return self

    def adjust_fov(self, system: System) -> "Camera":
        self.reset_center_of_FOV(system)
        return self

    def adjust_scale(self, system: System, factor: float = 1.1) -> float:
        """
        Adjust scale to completely put the `system` to the screen.
        Return recommended aspect ratio for the image.
        """
        b = system.primitives * system.size[:, None]  # Box sides.
        v = np.stack(
            [
                0 * b[0] + 0 * b[1] + 0 * b[2],
                0 * b[0] + 0 * b[1] + 1 * b[2],
                0 * b[0] + 1 * b[1] + 0 * b[2],
                0 * b[0] + 1 * b[1] + 1 * b[2],
                1 * b[0] + 0 * b[1] + 0 * b[2],
                1 * b[0] + 0 * b[1] + 1 * b[2],
                1 * b[0] + 1 * b[1] + 0 * b[2],
                1 * b[0] + 1 * b[1] + 1 * b[2],
            ],
            axis=0,
        )  # Box vertices
        p = (v[None, :, :] + system.representatives[:, None, :]).reshape(
            (-1, 3)
        )  # Extreme points.
        p = p - self.look_at[None, :]  # Shift origin to the center of view.
        # Project to screen plane.
        x = np.einsum("pk,k->p", v, self.look_right)
        y = np.einsum("pk,k->p", v, self.look_up)
        width = np.max(np.abs(x))
        height = np.max(np.abs(y))
        aspectratio = width / height
        self.look_scale = 0.5 * max(width, height) * factor
        return aspectratio

    @property
    def look_right(self):
        """
        Camera orientation is defined by:
        `self.look_direction` - where we look at (OZ axis),
        `self.look_up` - direction for screen's OY axis,
        `self.look_right` - direction for screen's OX axis.
        """
        horizont = -np.cross(self.look_up, self.look_direction)
        return horizont / np.linalg.norm(horizont)

    @property
    def scale(self):
        return (
            float(self.MAGA) / self.look_scale
            if self.perspective_is_on
            else 1.0 / self.look_scale
        )

    def camera_position(self):
        return self.look_at - self.look_direction / self.scale * 2

    def get_view_matrix(self):
        """
        Return ModelView matrix (should be transposed to use in GL).
        """
        shift = np.eye(4, dtype=np.float32)
        shift[:3, 3] = -self.look_at
        rotate = np.zeros((4, 4), dtype=np.float32)
        rotate[3, 3] = 1
        rotate[0, :3] = self.look_right
        rotate[1, :3] = self.look_up
        rotate[2, :3] = self.look_direction
        scale = np.eye(4, dtype=np.float32)
        scale[0, 0] = scale[1, 1] = scale[2, 2] = self.scale
        modelview = np.dot(scale, np.dot(rotate, shift))
        return modelview

    def get_projection_matrix(self, aspectratio=None):
        """
        Compute ViewProjection matrix (should be transposed to use in GL).
        """
        projection = np.eye(4, dtype=np.float32)
        if aspectratio > 1:
            projection[1, 1] = aspectratio
        else:
            projection[0, 0] = 1.0 / aspectratio
        projection[2, 2] = 1.0 / self.scale / self.depth
        if self.perspective_is_on:
            # w(z)=az+b
            # w(-1)=-a+b=1/mag, w(1)=a+b=mag
            projection[3, 3] = self.MAGA
            projection[3, 2] = self.MAG - self.MAGA
        return projection

    def move_field_of_view(self, x=0, y=0, z=0, rate=0.01) -> "Camera":
        self.look_at += x * self.look_right * self.look_scale * rate
        self.look_at += y * self.look_up * self.look_scale * rate
        self.look_at += z * self.look_direction * self.look_scale * rate
        return self

    def rotate_field_of_view(self, x=0, y=0, rate=0.01 * 2 * np.pi) -> "Camera":
        self.look_direction, self.look_up = (
            self.look_direction - x * rate * self.look_right - y * rate * self.look_up,
            self.look_up + y * rate * self.look_direction,
        )
        return self.normalize()

    def rotate_around(self, x=0, y=0, z=0, rate=0.01 * 2 * np.pi) -> "Camera":
        s, c = np.sin(rate), np.cos(rate)
        self.look_direction, self.look_up = (
            c * self.look_direction + x * s * self.look_up,
            -x * s * self.look_direction + c * self.look_up,
        )
        self.look_direction = c * self.look_direction + y * s * self.look_right
        self.look_up = c * self.look_up + z * s * self.look_right
        return self.normalize()

    def set_basis(self, depth=None, up=None) -> "Camera":
        self.look_direction = np.array(depth, dtype=np.float32)
        self.look_up = np.array(up, dtype=np.float32)
        return self.normalize()

    def normalize(self) -> "Camera":
        self.look_direction /= np.linalg.norm(self.look_direction)
        self.look_up -= np.sum(self.look_direction * self.look_up) * self.look_direction
        self.look_up /= np.linalg.norm(self.look_up)
        return self

    def zoom(self, v, rate=0.01):
        if v > 0:
            self.look_scale /= 1 + rate
        else:
            self.look_scale *= 1 + rate

    def toggle_perspective(self):
        self.perspective_is_on = not self.perspective_is_on


class UnitCamera(Camera):
    def __init__(self):
        self.depth = 10
        self.MAG = 1.0
        self.MAGA = (self.MAG + 1.0 / self.MAG) / 2
        self.perspective_is_on = True
        self.reset_FOV()

    def reset_center_of_FOV(self):
        self.look_at = np.array([0, 0, 0], dtype=np.float32)

    def reset_direction_of_FOV(self):
        self.look_direction = np.array([0, 0, -1], dtype=np.float32)
        self.look_up = np.array([0, 1, 0], dtype=np.float32)
        self.look_scale = 1

    def move_field_of_view(self, x=None, y=None, z=None, rate=0.01):
        return
