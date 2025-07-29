import moderngl as mgl
import numpy as np

from ..core import System
from .buffer import Field3DBuffer, Field1DBuffer, IntBuffer
from .sphere import SphereDotRender
from .vector import VectorRender
from .charge import ChargeRender
from .flow import FlowRender, AstraRender
from .isolines import IsolinesRender
from .camera import Camera, UnitCamera
from ..core import NumericProperty, BooleanProperty, ListProperty, PropertiesCollection
from .level import LevelRender
from .axes import AxesRender


class Scene:
    """Multiple renders joined into a scene."""

    def __init__(self, mglctx: mgl.Context, system: System, camera: Camera = None):
        """
        Arguments:
            `mglctx` - OpenGL context.
            `system` - lattice description.
            `camera` - initial camera orientation.
        """
        self._system = system
        self._ctx = mglctx
        self._camera = UnitCamera() if camera is None else camera
        assert isinstance(self._system, System)
        assert isinstance(self._ctx, mgl.Context)
        assert isinstance(self._camera, Camera)

    def __getitem__(self, key):
        props_by_render = self.list_properties()
        if key not in props_by_render:
            raise KeyError(
                f"Render `{key}` is unknown. To see list of renders call `yourscene.print_properties()`."
            )
        return PropertiesCollection(props_by_render[key])

    def upload(self, state: np.ndarray = None):
        """Set director field to render."""
        raise NotImplementedError

    def upload_mask(self, mask: np.ndarray = None):
        """Specify grid points to show.

        Renders showing individual vectors/directors at grid points can remove some of the points
        according to the mask.
        """
        pass

    def render(self):
        """Call to create image in earlier created OpenGL context."""
        raise NotImplementedError

    @property
    def camera(self) -> Camera:
        """Common camera for all renders."""
        return self._camera

    def set_camera(self, camera):
        """Change camera object."""
        self._camera = camera

    def list_properties(self):
        """Get all properties available in the scene."""
        return {}

    def list_actions(self):
        """Get all available actions."""
        return {}

    def print_properties(self):
        props_by_render = self.list_properties()
        for render, props in props_by_render.items():
            print(f"'{render:}'")
            for n, prop in enumerate(props):
                print(f"  {n}: {prop}")

    @property
    def detalization(self):
        """Detalization level.

        Higher levels of detalization give smoother surfaces, but render much slower.
        """
        return 1.0

    @detalization.setter
    def detalization(self, value):
        pass


##################################################################################################


class EmptyScene(Scene):
    """Basic scene containing no renders except for background and coordinate axes."""

    def __init__(self, background=(1, 1, 1), *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self._background = background
        self.preferable_size = np.min(np.linalg.norm(self._system.primitives, axis=-1))

        self._axes = AxesRender(mglctx=self._ctx)
        self.show_axes = True

    def upload(self, state=None, **kwargs):
        pass

    def render(self):
        self._ctx.clear(*self._background)

    @property
    def axes_render(self):
        return self._axes

    def render_axes(self, aspectratio):
        if not self.show_axes:
            return
        self._axes.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
        )

    def list_properties(self):
        return {
            "Axes": [
                BooleanProperty(self, "show_axes", title="Show axes"),
            ]+self._axes.list_properties(),
            **super().list_properties(),
        }
    

#################################################################################


class OrthoScene(EmptyScene):
    """Common ancestor for renders of 3d objects."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._camera.perspective_is_on = False

    def compute_camera_basis(self, axis):
        """Compute natural basis for camera looking along `axis`.

        Similar functionality is given by `Camera.set_predefined_direction`.
        """
        assert self._system.dim == 3
        size = self._system.size
        primitives = self._system.primitives
        if primitives.shape[0] == 3:
            basis = primitives
        elif primitives.shape[0] == 2:
            basis = np.empty((3, 3), dtype=np.float32)
            basis[:2] = primitives
            basis[2] = np.cross(basis[0], basis[1])
        else:
            assert False

        bxis = (axis - 1) % 3
        cxis = (axis - 2) % 3
        if size[bxis] < size[cxis]:
            depth = basis[axis]
            up = -basis[bxis]
        else:
            depth = basis[axis]
            up = basis[cxis]
        return (depth, up)


##########################################################################################################


class SphereDotScene(EmptyScene):
    """Render all directors on Block sphere."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._buffer = Field3DBuffer(self._ctx, self._system)
        self._render = SphereDotRender(
            mglctx=self._ctx, system=self._system, stateBuffer=self._buffer
        )

    def upload(self, state: np.ndarray = None, **kwargs):
        self._buffer.upload(state)

    def render(self, aspectratio=None):
        self._ctx.clear(*self._background)
        self._ctx.enable(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
        )

    def list_properties(self):
        return {
            "Ball": self._render.list_properties(),
            **super().list_properties(),
        }


##########################################################################################################


class VectorScene(EmptyScene):
    """Render director field as vectors/cylinders at every grid point."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._state = None
        self._m_state = self._system.field3D()
        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._mask_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._scalar_mask_buffer = Field1DBuffer(mglctx=self._ctx, system=self._system)

        self._render = VectorRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            coordinatesBuffer=self._coordinates_buffer,
            maskBuffer=self._mask_buffer,
            scalarMaskBuffer=self._scalar_mask_buffer,
        )
        self._render.base_size = self.preferable_size

    @property
    def vector_render(self):
        return self._render

    def get_use_energy_mask(self):
        return self._render.use_scalar_mask

    def set_use_energy_mask(self, value):
        self._render.use_scalar_mask = value
        self.update_scalar_mask()

    use_energy_mask = property(get_use_energy_mask, set_use_energy_mask)

    def update_scalar_mask(self):
        # print("update_scalar_mask")
        if not self._render.use_scalar_mask:
            return
        if self._state is None:
            return
        self._render.use_mask = True

        m_scalar1 = self._system.field1D()
        m_scalar2 = self._system.field1D()
        self._m_state.upload(self._state).energy_contributions(
            dm=m_scalar1, heisenberg=m_scalar2
        )
        scalar = -m_scalar1.download() - m_scalar2.download()
        mn, mx = np.min(scalar), np.max(scalar)
        scalar = (scalar - mn) / (mx - mn)
        scalar = np.power(scalar, 32)
        # scalar = (np.exp(scalar)-1)/np.exp(1)

        # scalar = -self._m_state.upload(self._state).energy().download()
        # scalar = np.abs(self._m_state.upload(self._state).top_charge().download())
        self._scalar_mask_buffer.upload(scalar)
        self._render.min_scalar = 0  # np.min(scalar)
        self._render.max_scalar = 1  # np.max(scalar)
        # print(self._render.min_scalar, self._render.max_scalar, self._render.use_scalar_mask)

    def upload(self, state: np.ndarray = None):
        self._state = state
        if not state is None:
            self._buffer.upload(state)
            self.update_scalar_mask()

    def upload_mask(self, mask: np.ndarray = None):
        self._render.use_scalar_mask = False
        if mask is None:
            self._render.use_mask = False
        else:
            self._mask_buffer.upload(mask)
            self._render.use_mask = True

    def render(self, aspectratio=None):
        self._ctx.clear(*self._background)
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Cones": self._render.list_properties(),
            "Mask": [
                BooleanProperty(
                    self, "use_energy_mask", title="Energy mask", reset=True
                ),
            ],
            **super().list_properties(),
        }

    @property
    def detalization(self):
        return self._render.detalization

    @detalization.setter
    def detalization(self, value):
        self._render.detalization = value


##########################################################################################################


class LayerScene(OrthoScene):
    """Show sections of director field by a coordinate axis.

    Very similar to `VectorScene` but show only gird points sharing one coordinate defined by `axis` property.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._mask_buffer = self._coordinates_buffer  # Not used
        self._scalar_mask_buffer = self._coordinates_buffer

        self._render = VectorRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            coordinatesBuffer=self._coordinates_buffer,
            maskBuffer=self._mask_buffer,
            scalarMaskBuffer=self._scalar_mask_buffer,
        )
        self._render.min_size = 0
        self._render.base_size = self.preferable_size
        self._render.min_threshold = 0
        self._render.power_size = 1

        self.axis = 2
        self.show_axes = True

    @property
    def vector_render(self):
        return self._render

    def get_axis(self):
        return self._axis

    def set_axis(self, value):
        self._axis = int(value)
        self.layers_count = self._render.size[self._axis]
        self.layer = self.layers_count / 2

        basis = self.compute_camera_basis(self._axis)
        # print("Camera orientation:", basis)
        self._camera.set_basis(*basis)

    def get_layer(self):
        return self._layer

    def set_layer(self, value):
        self._layer = int(value)
        mn = 0 * np.array(self._render.size)
        mx = np.array(self._render.size)
        mn[self._axis] = self._layer
        mx[self._axis] = self._layer
        self._render.clip_min = mn
        self._render.clip_max = mx

    axis = property(get_axis, set_axis)
    layer = property(get_layer, set_layer)

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def upload_mask(self, mask: np.ndarray = None):
        pass

    def render(self, aspectratio: float = None):
        self._ctx.clear(*self._background)
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Filter": [
                NumericProperty(
                    self, "axis", title="Axis", min=0, max=2, count=3, reset=True
                ),
                NumericProperty(
                    self,
                    "layer",
                    title="Layer",
                    min=0,
                    max=self.layers_count - 1,
                    count=self.layers_count,
                ),
            ],
            # "Cones": self._render.list_properties(),
            "Cones": [
                ListProperty(
                    self._render,
                    "mesh_shape",
                    title="Shape",
                    values=sorted(self._render.MESH_NAMES.keys()),
                ),
                # BooleanProperty(self._render, "director_mode", title="Director mode"),
                BooleanProperty(self._render, "negate", title="Negate spin"),
                NumericProperty(
                    self._render, "width", title="Width", min=0.01, max=2.0, count=100
                ),
                NumericProperty(
                    self._render,
                    "color_shift",
                    title="Hue",
                    min=0.0,
                    max=1.0,
                    count=360,
                ),
                NumericProperty(
                    self._render,
                    "saturation_mag",
                    title="Saturation",
                    min=1.0,
                    max=10.0,
                    count=500,
                ),
                # NumericProperty(self, "min_size", title="Min. size", min=0.0, max=2.0, count=30),
                NumericProperty(
                    self._render,
                    "max_size",
                    title="Max. size",
                    min=0.0,
                    max=2.0,
                    count=30,
                ),
                # NumericProperty(self._render, "power_size", title="Steepness", min=0.0, max=2.0, count=30),
                # NumericProperty(self._render, "min_threshold", title="Min. threshold", min=0.0, max=1.0, count=500),
                # NumericProperty(self._render, "detalization", title="Detalization", min=1., max=10., count=10),
            ],
            **super().list_properties(),
        }

    @property
    def detalization(self):
        return self._render.detalization

    @detalization.setter
    def detalization(self, value):
        self._render.detalization = value


##########################################################################################################


class LayerAndSurfaceScene(LayerScene):
    """Mix of LayerScene and SurfaceScene."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        idx = self._system.get_inner_simplices()
        self._idx = IntBuffer(mglctx=self._ctx, count=4 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._level_render = FlowRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self._camera.perspective_is_on = True

    @property
    def vector_render(self):
        return self._render

    @property
    def isosurface_render(self):
        return self._level_render

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *(
                [1.0, 1.0, 1.0, 1.0]
                if self._level_render.inverted
                else [0.0, 0.0, 0.0, 1.0]
            )
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)

        self._render.color_shift = self._level_render.color_shift
        self._render.lighting = self._level_render.lighting
        self._render.negate = self._level_render.negate

        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self._level_render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Layer": [
                NumericProperty(
                    self, "axis", title="Axis", min=0, max=2, count=3, reset=True
                ),
                NumericProperty(
                    self,
                    "layer",
                    title="Layer",
                    min=0,
                    max=self.layers_count - 1,
                    count=self.layers_count,
                ),
                ListProperty(
                    self._render,
                    "mesh_shape",
                    title="Shape",
                    values=sorted(self._render.MESH_NAMES.keys()),
                ),
                NumericProperty(
                    self._render, "width", title="Width", min=0.01, max=2.0, count=100
                ),
                NumericProperty(
                    self._render,
                    "max_size",
                    title="Max. size",
                    min=0.0,
                    max=2.0,
                    count=30,
                ),
            ],
            "Isosurface": [
                BooleanProperty(
                    self._level_render, "neglect_z", title="Ignore z-projection"
                ),
                ListProperty(
                    self._level_render,
                    "angle_name",
                    title="Constant",
                    values=self._level_render.ANGLENAMES,
                ),
                NumericProperty(
                    self._level_render,
                    "level",
                    title="Level",
                    min=-1.0,
                    max=1.0,
                    count=1000,
                ),
            ],
            "Shared": [
                BooleanProperty(self._level_render, "inverted", title="Invert colors"),
                BooleanProperty(self._level_render, "lighting", title="Lighting"),
                BooleanProperty(self._level_render, "negate", title="Negate"),
                NumericProperty(
                    self._level_render,
                    "color_shift",
                    title="Hue",
                    min=0.0,
                    max=1.0,
                    count=360,
                ),
            ],
            **super().list_properties(),
        }


##########################################################################################################


class LayerAndIsolinesScene(LayerScene):
    """Mix of LayerScene and IsolinesScene."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        idx = self._system.get_inner_simplices()
        self._idx = IntBuffer(mglctx=self._ctx, count=4 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._level_render = IsolinesRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self._camera.perspective_is_on = True

    @property
    def vector_render(self):
        return self._render

    @property
    def isolines_render(self):
        return self._level_render

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *(
                [1.0, 1.0, 1.0, 1.0]
                if self._level_render.inverted
                else [0.0, 0.0, 0.0, 1.0]
            )
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)

        self._render.color_shift = self._level_render.color_shift
        self._render.lighting = self._level_render.lighting
        self._render.negate = self._level_render.negate

        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self._ctx.line_width = 3
        self._level_render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Layer": [
                NumericProperty(
                    self, "axis", title="Axis", min=0, max=2, count=3, reset=True
                ),
                NumericProperty(
                    self,
                    "layer",
                    title="Layer",
                    min=0,
                    max=self.layers_count - 1,
                    count=self.layers_count,
                ),
                ListProperty(
                    self._render,
                    "mesh_shape",
                    title="Shape",
                    values=sorted(self._render.MESH_NAMES.keys()),
                ),
                NumericProperty(
                    self._render, "width", title="Width", min=0.01, max=2.0, count=100
                ),
                NumericProperty(
                    self._render,
                    "max_size",
                    title="Max. size",
                    min=0.0,
                    max=2.0,
                    count=30,
                ),
            ],
            "Isolines": [
                BooleanProperty(
                    self._level_render, "neglect_z", title="Ignore z-projection"
                ),
                NumericProperty(
                    self._level_render,
                    "phi_shift",
                    title="Polar angle offset",
                    min=-1.0,
                    max=1.0,
                    count=1000,
                ),
                NumericProperty(
                    self._level_render,
                    "theta_shift",
                    title="Azimuthal angle offset",
                    min=-1.0,
                    max=1.0,
                    count=1000,
                ),
                NumericProperty(
                    self._level_render,
                    "npetals",
                    title="Polar angle substeps",
                    min=1,
                    max=10,
                    count=10,
                ),
                NumericProperty(
                    self._level_render,
                    "ntheta",
                    title="Azimuthal angle substeps",
                    min=1,
                    max=5,
                    count=5,
                ),
                NumericProperty(
                    self._level_render,
                    "width",
                    title="Width",
                    min=0.0,
                    max=0.02,
                    count=1000,
                ),
            ],
            "Shared": [
                BooleanProperty(self._level_render, "inverted", title="Invert colors"),
                BooleanProperty(self._level_render, "lighting", title="Lighting"),
                BooleanProperty(self._level_render, "negate", title="Negate"),
                NumericProperty(
                    self._level_render,
                    "color_shift",
                    title="Hue",
                    min=0.0,
                    max=1.0,
                    count=360,
                ),
            ],
            **super().list_properties(),
        }


##########################################################################################################


class CubeScene(OrthoScene):
    """Show director field as vectors similar to VectorScene with cubic cut."""

    def __init__(self, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._mask_buffer = self._coordinates_buffer  # Not used
        self._scalar_mask_buffer = self._coordinates_buffer

        self._render = VectorRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            coordinatesBuffer=self._coordinates_buffer,
            maskBuffer=self._mask_buffer,
            scalarMaskBuffer=self._scalar_mask_buffer,
        )
        self._render.min_size = 0
        self._render.base_size = self.preferable_size
        self._render.min_threshold = 0
        self._render.power_size = 1
        self._render.clip_invert = True

        self._section = np.array(self._render.size, dtype=np.int32) / 2
        self._reverse = np.array(
            [
                False,
            ]
            * 3
        )
        self.update_parameters()
        self._camera.set_basis(*self.compute_camera_basis())

    def update_parameters(self):
        self._render.clip_min = [
            0 if self._reverse[n] else self._section[n] for n in range(3)
        ]
        self._render.clip_max = [
            self._section[n] + 1 if self._reverse[n] else self._render.size[n]
            for n in range(3)
        ]

    def get_section(self, n):
        return self._section[n]

    def set_section(self, n, value):
        self._section[n] = int(value)
        self.update_parameters()

    def get_reverse(self, n):
        return self._reverse[n]

    def set_reverse(self, n, value):
        self._reverse[n] = bool(value)
        self.update_parameters()
        self._camera.set_basis(*self.compute_camera_basis())

    section_x = property(
        lambda self: self.get_section(0), lambda self, v: self.set_section(0, v)
    )
    section_y = property(
        lambda self: self.get_section(1), lambda self, v: self.set_section(1, v)
    )
    section_z = property(
        lambda self: self.get_section(2), lambda self, v: self.set_section(2, v)
    )

    reverse_x = property(
        lambda self: self.get_reverse(0), lambda self, v: self.set_reverse(0, v)
    )
    reverse_y = property(
        lambda self: self.get_reverse(1), lambda self, v: self.set_reverse(1, v)
    )
    reverse_z = property(
        lambda self: self.get_reverse(2), lambda self, v: self.set_reverse(2, v)
    )

    def compute_camera_basis(self):
        d = np.array([1 if self._reverse[n] else -1 for n in range(3)])
        primitives = self._system.primitives

        if primitives.shape[0] == 3:
            basis = primitives
        elif primitives.shape[0] == 2:
            basis = np.empty((3, 3), dtype=np.float32)
            basis[:2] = primitives
            basis[2] = np.cross(basis[0], basis[1])
        else:
            assert False

        depth = np.sum(basis * d[:, None], axis=-1)
        d[1] *= -1
        up = np.sum(basis * d[:, None], axis=-1)
        return (depth, -up)

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def upload_mask(self, mask: np.ndarray = None):
        pass

    def render(self, aspectratio=None):
        self._ctx.clear(*self._background)
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Filter": [
                NumericProperty(
                    self,
                    "section_x",
                    title="X-section",
                    min=0,
                    max=self._render.size[0],
                    count=self._render.size[0] + 1,
                ),
                NumericProperty(
                    self,
                    "section_y",
                    title="Y-section",
                    min=0,
                    max=self._render.size[1],
                    count=self._render.size[1] + 1,
                ),
                NumericProperty(
                    self,
                    "section_z",
                    title="Z-section",
                    min=0,
                    max=self._render.size[2],
                    count=self._render.size[2] + 1,
                ),
                BooleanProperty(self, "reverse_x", title="Reverse X"),
                BooleanProperty(self, "reverse_y", title="Reverse Y"),
                BooleanProperty(self, "reverse_z", title="Reverse Z"),
            ],
            "Cones": [
                NumericProperty(
                    self._render, "max_size", title="Size", min=0.0, max=2.0, count=30
                ),
            ],
            **super().list_properties(),
        }

    @property
    def detalization(self):
        return self._render.detalization

    @detalization.setter
    def detalization(self, value):
        self._render.detalization = value


##########################################################################################################


class ChargeScene(OrthoScene):
    """Show distribution of topological charge.

    Charge computed on each coordinate plane in shown by RGB components of color.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)

        idx = self._system.get_inner_triangles(
            triangulation=self._system.default_trivial_cell_triangulation()
        )
        self._idx = IntBuffer(mglctx=self._ctx, count=3 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._render = ChargeRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self.update_parameters()

    def update_parameters(self):
        pass

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *([1.0, 1.0, 1.0, 1.0] if self._render.inverted else [0.0, 0.0, 0.0, 1.0])
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Charge": self._render.list_properties(),
            **super().list_properties(),
            }


##########################################################################################################


class FlowScene(EmptyScene):
    """Show isosurface of director field."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self._system.dim != 3:
            raise NotImplementedError("Only 3D systems are supported.")

        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)

        idx = self._system.get_inner_simplices()
        self._idx = IntBuffer(mglctx=self._ctx, count=4 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._render = FlowRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self._camera.perspective_is_on = True

        self.update_parameters()

    def update_parameters(self):
        pass

    @property
    def surface_render(self):
        return self._render

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *([1.0, 1.0, 1.0, 1.0] if self._render.inverted else [0.0, 0.0, 0.0, 1.0])
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Level surface": self._render.list_properties(),
            **super().list_properties(),
            }


##########################################################################################################


class LevelScene(EmptyScene):
    """Show isusurface of the director field."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self._system.dim != 3:
            raise NotImplementedError("Only 3D systems are supported.")

        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)

        idx = self._system.get_inner_simplices()
        self._idx = IntBuffer(mglctx=self._ctx, count=4 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._render = LevelRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self._camera.perspective_is_on = True

        self.update_parameters()

    def update_parameters(self):
        pass

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *([1.0, 1.0, 1.0, 1.0] if self._render.inverted else [0.0, 0.0, 0.0, 1.0])
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    def list_properties(self):
        return {
            "Level surface": self._render.list_properties(),
            **super().list_properties(),
            }


##########################################################################################################


class AstraScene(EmptyScene):
    """Show multiple isusurfaces of the director field."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self._system.dim != 3:
            raise NotImplementedError("Only 3D systems are supported.")

        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)

        idx = self._system.get_inner_simplices()
        self._idx = IntBuffer(mglctx=self._ctx, count=4 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._render = AstraRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self._camera.perspective_is_on = True

        self.update_parameters()

    def update_parameters(self):
        pass

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *([1.0, 1.0, 1.0, 1.0] if self._render.inverted else [0.0, 0.0, 0.0, 1.0])
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    @property
    def surface_render(self):
        return self._render

    def list_properties(self):
        return {
            "Astra": self._render.list_properties(),
            **super().list_properties(),
        }


##########################################################################################################


class IsolinesScene(EmptyScene):
    """Show isolines of the director field."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self._system.dim != 3:
            raise NotImplementedError("Only 3D systems are supported.")

        self._buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)
        self._coordinates_buffer = Field3DBuffer(mglctx=self._ctx, system=self._system)

        idx = self._system.get_inner_simplices()
        self._idx = IntBuffer(mglctx=self._ctx, count=4 * idx.shape[0])
        self._idx.upload(idx.flatten())

        self._render = IsolinesRender(
            mglctx=self._ctx,
            system=self._system,
            stateBuffer=self._buffer,
            indexBuffer=self._idx,
            coordinatesBuffer=self._coordinates_buffer,
        )

        self._camera.perspective_is_on = True

        self.update_parameters()

    @property
    def isolines_render(self):
        return self._render

    def update_parameters(self):
        pass

    def upload(self, state: np.ndarray = None):
        if not state is None:
            self._buffer.upload(state)

    def render(self, aspectratio: float = None):
        self._ctx.clear(
            *([1.0, 1.0, 1.0, 1.0] if self._render.inverted else [0.0, 0.0, 0.0, 1.0])
        )
        self._ctx.enable_only(mgl.DEPTH_TEST)
        self._ctx.line_width = 3
        self._render.render(
            modelview=self.camera.get_view_matrix(),
            projection=self.camera.get_projection_matrix(aspectratio=aspectratio),
            camera_position=self.camera.camera_position(),
        )

        self.render_axes(aspectratio=aspectratio)

    @property
    def surface_render(self):
        return self._render

    def list_properties(self):
        return {
            "Isolines": self._render.list_properties(),
            **super().list_properties(),
        }


##########################################################################################################

# List of all available scenes.
SCENES = {
    "Vectors": VectorScene,
    "Level surface": FlowScene,
    # "Level surface-2": LevelScene,
    "Astra": AstraScene,
    "Isolines": IsolinesScene,
    "Top. charge": ChargeScene,
    "Layer": LayerScene,
    "Cube": CubeScene,
    "Ball": SphereDotScene,
    "Layer and isosurface": LayerAndSurfaceScene,
    "Layer and isolines": LayerAndIsolinesScene,
}


def print_scenes():
    print("Scenes:", ", ".join(SCENES))
