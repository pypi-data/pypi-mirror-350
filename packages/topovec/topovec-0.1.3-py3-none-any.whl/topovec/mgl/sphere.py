import moderngl as mgl
import numpy as np

from .render import StateRender
from .buffer import Float3DBuffer


class SphereDotRender(StateRender):
    VERTEX = """
                #version 330

                uniform mat4 u_view;
                uniform mat4 u_projection;
                uniform vec3 u_axis;
                in vec3 in_spin;
                out vec3 v_color;
                
                const float M_PI=3.1415926535897932384626433832795;

                vec3 hsv2rgb(vec3 c) {
                    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
                }

                void main() {
                    vec4 v_eye_position = u_view * vec4(in_spin, 1.0);
                    gl_Position = u_projection * v_eye_position;

                    //gl_Position = vec4(in_spin.xy, (in_spin.z+1)/2, 1.0);

                    float h = (atan(in_spin.y, in_spin.x)/M_PI+1)/2;
                    float s = dot(u_axis, in_spin);
                    vec3 hsv = vec3(h, clamp(1+s, 0, 1), clamp(1-s, 0, 1));
                    v_color = hsv2rgb(hsv);
                }
            """
    GEOMETRY = None
    FRAGMENT = """
                #version 330
                in vec3 v_color;
                out vec4 f_color;
                void main() {
                    f_color = vec4(v_color, 1.0);
                }
            """

    def __init__(self, dot_size=10, axis=(0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self._dot_size = dot_size
        self.u_axis = self._prog["u_axis"]
        self.u_view = self._prog["u_view"]
        self.u_projection = self._prog["u_projection"]

        if axis is None:
            self._axis = self._system.field.reshape(-1, 3)[0]
        else:
            self._axis = axis
        if np.linalg.norm(self._axis) < 1e-8:
            self._axis = (0, 0, 1)
        self._axis = np.array(self._axis, dtype=np.float32)
        self._axis /= np.linalg.norm(self._axis)

    def render(self, scales=None, modelview=None, projection=None, **kwargs):
        self._ctx.point_size = self._dot_size
        self.u_axis.value = tuple(self._axis)
        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())
        self._vao.render(mode=mgl.POINTS)
