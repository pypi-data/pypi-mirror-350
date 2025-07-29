import moderngl as mgl
import numpy as np

from .render import Render
from .buffer import Float3DBuffer
from .solid import ArrowMesh
from ..core import NumericProperty, BooleanProperty, ListProperty, PropertiesCollection


#######################################################################################################


class AxesRender(Render):
    VERTEX = """
                #version 330

                const float M_PI = 3.1415926535897932384626433832795;

                uniform mat4 u_view;
                uniform mat4 u_projection;

                uniform float u_ratio;
                uniform float u_length;
                uniform vec2 u_location;

                in vec3 in_origin; // origin of axis
                in vec3 in_dir; // direction of axis

                in vec3 in_pos; // mesh point in mesh coordinates
                in vec3 in_normal; // normal to mesh at in_pos in mesh coordinates
                in vec3 in_color; // color

                out vec3 v_pos; // vertex position in world coordinates
                out vec3 v_normal; // normal to surface in world coordinates
                out vec4 v_color;
                out vec3 v_camera;
                out vec3 v_light_direction;

                mat3 rotmat(vec3 z) {
                    vec3 a = cross(z, vec3(1.0,0.0,0.0));
                    vec3 b = cross(z, vec3(0.0,1.0,0.0));
                    vec3 c = (length(a)>length(b)) ? a : b;
                    vec3 x = normalize(c);
                    vec3 y = cross(x, z);
                    return mat3(x, y, z);
                }

                void main() {
                    vec3 dir = normalize(in_dir);
                    mat3 mesh = rotmat(dir);
                    vec3 pos = in_pos*vec3(u_ratio,u_ratio,1);
                    v_pos = in_origin + mesh * pos;

                    mat4 view = mat4(u_view);
                    mat4 projection = mat4(u_projection);
                    view[0] = normalize(view[0]);
                    view[1] = normalize(view[1]);
                    view[2] = normalize(view[2]);
                    view[3] = vec4(0,0,0,1);
                    projection[2][2] = 1;

                    vec4 glpos = projection * view * vec4(v_pos*u_length, 1.0);
                    gl_Position = glpos/glpos.w + vec4(u_location,0,0);
                    
                    v_normal = mesh * in_normal;

                    v_color = vec4( in_color, 1.0 );

                    v_camera = transpose(view)[2].xyz;
                    v_light_direction = -v_camera;
                } 
            """
    GEOMETRY = None
    FRAGMENT = """
                #version 330

                in vec3 v_normal;
                in vec3 v_pos;
                in vec4 v_color;
                in vec3 v_camera;
                in vec3 v_light_direction;

                out vec4 f_color;

                void main() {
                    vec3 normal = normalize(v_normal);
                    float inner_reflected = dot(reflect(normalize(v_pos-v_camera), normal), v_light_direction);
                    float inner_disperse = dot(normal, v_light_direction);
                    float intensity = 0.4+0.6*clamp(inner_disperse, 0.0, 1.0) + 0.3*clamp(inner_reflected, 0.0, 1.0);
                    f_color = vec4(intensity*v_color.xyz, v_color.t);
                }
            """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ratio = 0.2
        self.length = 0.1
        self.location_x, self.location_y = -0.8, -0.8

        origin = np.array([[0.55, 0, 0], [0, 0.55, 0], [0, 0, 0.55]], dtype=np.float32)
        self._originBuffer = Float3DBuffer(mglctx=self._ctx, count=origin.shape[0])
        self._originBuffer.upload(origin)

        direction = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
        self._directionBuffer = Float3DBuffer(
            mglctx=self._ctx, count=direction.shape[0]
        )
        self._directionBuffer.upload(direction)

        color = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
        self._colorBuffer = Float3DBuffer(mglctx=self._ctx, count=color.shape[0])
        self._colorBuffer.upload(color)

        self.init_vao()

    def init_vao(self):
        self.mesh = ArrowMesh(mglctx=self._ctx, count=10)
        self._vao = self._ctx.vertex_array(
            self._prog,
            [
                (self.mesh.pos.vbo, "3f", "in_pos"),
                (self.mesh.normal.vbo, "3f", "in_normal"),
                (self._directionBuffer.vbo, "3f/i", "in_dir"),
                (self._originBuffer.vbo, "3f/i", "in_origin"),
                (self._colorBuffer.vbo, "3f/i", "in_color"),
            ],
            self.mesh.idx.ibo,
        )

    def render(self, scales=None, modelview=None, projection=None):
        self._ctx.fbo.color_mask = False, False, False, False
        self._ctx.fbo.depth_mask = True
        self._ctx.fbo.clear()
        self._ctx.fbo.color_mask = True, True, True, True
        self._ctx.fbo.use() # Help with buggy driver.
        self._ctx.enable_only(mgl.DEPTH_TEST)

        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())

        self.u_ratio.value = self.ratio
        self.u_length.value = self.length
        self.u_location.value = (self.location_x, self.location_y)

        self._vao.render(mode=mgl.TRIANGLES, instances=3, vertices=-1, first=0)

    def list_properties(self):
        return [
            NumericProperty(self, "location_x", title="X", min=-1.0, max=1.0, count=200),
            NumericProperty(self, "location_y", title="Y", min=-1.0, max=1.0, count=200),
            NumericProperty(self, "length", title="Length", min=0.0, max=1.0, count=200),
            NumericProperty(self, "ratio", title="Ratio", min=0.01, max=1.0, count=100),
        ]
