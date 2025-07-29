import moderngl as mgl
import numpy as np

from .render import *
from .buffer import Float3DBuffer, IntBuffer
from ..core.property import NumericProperty, ListProperty, BooleanProperty


######################################################################################################

# GLSL functions for lattice points computation. For future usage.
#
# uniform ivec4 u_size; // Number of spins per each asis+number of atoms per unit cell.
# uniform mat3 u_generators; // Lattice generators.
# uniform vec3 u_representatives[]; // Atoms in the the unit cell.
#
# ivec4 reshape(int id) {
#     ivec4 stride;
#     stride.t = 1;
#     stride.z = stride.t*u_size.t;
#     stride.y = stride.z*u_size.z;
#     stride.x = stride.t*u_size.y;
#     return (id / stride) % u_size;
# }
#
# pos get_coordinates() {
#     ivec4 idx = reshape(gl_VertexID);
#     return u_generators*idx.xyz + u_representatives[idx.t];
# }


class ChargeRender(StateRender):
    VERTEX = """
            #version 330

            const float M_PI = 3.1415926535897932384626433832795;

            uniform mat4 u_view;
            uniform mat4 u_projection;
            uniform vec3 u_camera; // camera position in world coordinates

            in vec3 in_center; // center of atom
            in vec3 in_spin; // spin direction

            out VS_OUT {
                vec3 origin; // atom position in world coordiantes
                vec3 spin; // spin direction in spin space
                vec3 light_direction; 
            } vs_out;

            void main() {
                vs_out.origin = in_center;
                vs_out.spin = in_spin;
                vs_out.light_direction = - normalize(vs_out.origin-u_camera);

                gl_Position = u_projection * u_view * vec4(vs_out.origin, 1.0);
            } 
        """
    GEOMETRY = """
            #version 330 core

            layout (triangles) in;
            layout (triangle_strip, max_vertices = 4) out;

            uniform float u_brightness;
            uniform bool u_inverted;

            in VS_OUT {
                vec3 origin; 
                vec3 spin; 
                vec3 light_direction; 
            } vs_in[];

            out vec3 v_normal;
            out vec3 v_position;
            out vec3 v_color;
            out vec3 v_light_direction;

            void main() {
                vec3 ab = vs_in[1].origin - vs_in[0].origin;
                vec3 ac = vs_in[2].origin - vs_in[0].origin;
                v_normal = normalize(cross(ab, ac));

                float top_charge = dot(vs_in[0].spin, cross(vs_in[1].spin, vs_in[2].spin));

                vec3 top_color;

                // 2D charge
                /*
                float plus_intens = clamp(u_brightness*top_charge, 0, 1);
                float minus_intens = clamp(-u_brightness*top_charge, 0, 1);

                if (u_inverted) {
                    top_color = vec3(1-minus_intens, 1-plus_intens-minus_intens, 1-plus_intens);
                } else {
                    top_color = vec3(plus_intens, 0, minus_intens);
                };
                */

                // 3D charge
                vec3 clr = v_normal.yzx*top_charge;
                if (u_inverted) {
                    top_color = 1.0-u_brightness*(clamp(abs(clr),0.,1.)+clamp(-clr.yzx,0.,1.)+clamp(clr.zxy,0.,1.));
                } else {
                    top_color = u_brightness*(clamp(clr.yzx,0.,1.)+clamp(-clr.zxy,0.,1.));
                };

                for (int k=0; k<3; k++) {
                    gl_Position = gl_in[k].gl_Position;
                    v_position = vs_in[k].origin;
                    v_color = top_color;
                    EmitVertex();
                };
                EndPrimitive();
            }   
        """
    FRAGMENT = """
            #version 330

            uniform vec3 v_camera;

            in vec3 v_normal;
            in vec3 v_position;
            in vec3 v_color;
            in vec3 v_light_direction;

            out vec4 f_color;

            void main() {
                f_color = vec4(v_color, 1.0);
            }
        """

    def __init__(
        self,
        coordinatesBuffer: Float3DBuffer = None,
        maskBuffer=None,
        indexBuffer: IntBuffer = None,
        scalarMaskBuffer=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.u_view = self._prog["u_view"]
        self.u_projection = self._prog["u_projection"]

        self._coordinatesBuffer = coordinatesBuffer
        self._coordinatesBuffer.upload(self._system.spin_positions())

        self._idx = indexBuffer

        self.init_vao()

        self.brightness = 3.0
        self.inverted = True

    def init_vao(self):
        self._vao = self._ctx.vertex_array(
            self._prog,
            [
                (self._state.vbo, "3f/v", "in_spin"),
                (self._coordinatesBuffer.vbo, "3f/v", "in_center"),
            ],
            self._idx.ibo,
        )

    def render(
        self, scales=None, modelview=None, projection=None, camera_position=None
    ):
        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())

        self.u_brightness.value = self.brightness
        self.u_inverted.value = self.inverted

        self._ctx.enable_only(mgl.BLEND)
        self._ctx.blend_func = mgl.ONE, mgl.ONE
        self._ctx.blend_equation = mgl.MIN if self.inverted else mgl.MAX

        self._vao.render(mode=mgl.TRIANGLES, vertices=-1, first=0)

    def list_properties(self):
        return [
            BooleanProperty(self, "inverted", title="Invert colors"),
            NumericProperty(
                self, "brightness", title="Brightness", min=0.0, max=10.0, count=1000
            ),
        ]
