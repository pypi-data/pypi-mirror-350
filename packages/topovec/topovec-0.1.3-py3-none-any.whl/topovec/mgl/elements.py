import moderngl as mgl
import numpy as np

from .render import *
from .buffer import Float3DBuffer, IntBuffer
from ..core import NumericProperty

######################################################################################################


class ChargeRender(StateRender):
    VERTEX = """
                #version 330

                const float M_PI = 3.1415926535897932384626433832795;

                uniform mat4 u_view;
                uniform mat4 u_projection;

                in vec3 in_center; // center of atom
                in vec3 in_spin; // spin direction

                out vec3 v_pos; // vertex position in world coordiantes
                out vec3 v_spin;

                mat3 rotmat(vec3 z) {
                    vec3 a = cross(z, vec3(1.0,0.0,0.0));
                    vec3 b = cross(z, vec3(0.0,1.0,0.0));
                    vec3 c = (length(a)>length(b)) ? a : b;
                    vec3 x = normalize(c);
                    vec3 y = cross(x, z);
                    return mat3(x, y, z);
                }

                void main() {
                    float len = length(in_spin);
                    vec3 spin = in_spin/len;
                    mat3 mesh = rotmat(spin);
                    vec3 v_pos = in_center;
                    gl_Position = u_projection * u_view * vec4(v_pos, 1.0);

                    v_spin = spin;
                } 
            """
    GEOMETRY = None
    FRAGMENT = """
                #version 330

                in vec4 v_color;

                out vec4 f_color;

                void main() {
                    f_color = v_color;
                }
            """

    def __init__(
        self, light=(1, 2, -3), coordinatesBuffer=None, maskBuffer=None, **kwargs
    ):
        super().__init__(**kwargs)

        self.u_view = self._prog["u_view"]
        self.u_projection = self._prog["u_projection"]
        self.u_camera = self._prog["u_camera"]
        self.u_light_direction = self._prog["u_light_direction"]
        self.u_use_mask = self._prog["u_use_mask"]
        self.u_min_size = self._prog["u_min_size"]
        self.u_max_size = self._prog["u_max_size"]
        self.u_power_size = self._prog["u_power_size"]
        self.u_min_threshold = self._prog["u_min_threshold"]
        self.u_size = self._prog["u_size"]
        self.u_clip_min = self._prog["u_clip_min"]
        self.u_clip_max = self._prog["u_clip_max"]
        self.u_clip_invert = self._prog["u_clip_invert"]

        self._light = np.array(light, dtype=np.float32)
        self._light /= np.linalg.norm(self._light)

        self._coordinatesBuffer = coordinatesBuffer
        self._coordinatesBuffer.upload(self._system.spin_positions())

        self._maskBuffer = maskBuffer

        self.mesh = ConicMesh(mglctx=self._ctx)

        self._vao = self._ctx.vertex_array(
            self._prog,
            [
                (self.mesh.pos.vbo, "3f", "in_pos"),
                (self.mesh.normal.vbo, "3f", "in_normal"),
                (self._state.vbo, "3f/i", "in_spin"),
                (self._coordinatesBuffer.vbo, "3f/i", "in_center"),
                (self._maskBuffer.vbo, "3f/i", "in_mask"),
            ],
            self.mesh.idx.ibo,
        )

        self.use_mask = False
        self.base_size = 1.0
        self.min_size = 0.0
        self.max_size = 1.5
        self.power_size = 1.0
        self.min_threshold = 0.5
        self.size = self._system.size + (1,) * (3 - self._system.dim)
        self.clip_min = (0, 0, 0)
        self.clip_max = tuple(self.size)
        self.clip_invert = False

    def render(
        self, scales=None, modelview=None, projection=None, camera_position=None
    ):
        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())
        self.u_camera.value = tuple(camera_position)
        self.u_light_direction.value = tuple(self._light)
        self.u_use_mask.value = self.use_mask
        self.u_min_size.value = self.min_size * self.base_size
        self.u_max_size.value = self.max_size * self.base_size
        self.u_power_size.value = self.power_size
        self.u_min_threshold.value = self.min_threshold
        self.u_size.value = tuple(self.size)
        self.u_clip_min.value = tuple(self.clip_min)
        self.u_clip_max.value = tuple(self.clip_max)
        self.u_clip_invert.value = self.clip_invert

        self._vao.render(
            mode=mgl.TRIANGLES,
            instances=self._system.number_of_spins,
            vertices=-1,
            first=0,
        )

    def list_properties(self):
        return [
            NumericProperty(
                self, "min_size", title="Min. size", min=0.0, max=2.0, count=30
            ),
            NumericProperty(
                self, "max_size", title="Max. size", min=0.0, max=2.0, count=30
            ),
            NumericProperty(
                self, "power_size", title="Steepness", min=0.0, max=2.0, count=30
            ),
            NumericProperty(
                self,
                "min_threshold",
                title="Min. threshold",
                min=0.0,
                max=1.0,
                count=50,
            ),
        ]
