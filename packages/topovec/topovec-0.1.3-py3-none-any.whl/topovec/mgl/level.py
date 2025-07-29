import moderngl as mgl
import numpy as np

from .render import *
from .buffer import Float3DBuffer, IntBuffer
from ..core import NumericProperty, ListProperty, BooleanProperty


######################################################################################################


class LevelRender(StateRender):
    VERTEX = """
            #version 330

            in vec3 in_center; // center of atom
            in vec3 in_spin; // spin direction

            out VS_OUT {
                vec3 origin; // atom position in world coordiantes
                vec3 spin; // spin direction in spin space
            } vs_out;

            void main() {
                vec3 spin = normalize(in_spin);
                vs_out.origin = in_center;
                vs_out.spin = spin;
            } 
        """
    GEOMETRY = """
            #version 330 core

            const float M_PI = 3.1415926535897932384626433832795;


            layout (lines_adjacency) in;
            layout (triangle_strip, max_vertices = 16) out;

            uniform vec3 u_axis; // Zenith direction.
            uniform float u_level;
            uniform bool u_constant_theta;


            uniform mat4 u_view;
            uniform mat4 u_projection;
            uniform int u_subdivide=1;

            uniform vec3 u_camera; // camera position in world coordinates
            uniform float u_color_shift;
            uniform bool u_neglect_z;
            uniform bool u_inverted;

            in VS_OUT {
                vec3 origin;
                vec3 spin;
            } vs_in[];

            out vec3 v_position;
            out vec3 v_color;
            out vec3 v_light_direction;

            struct Input {
                vec3 origin;
                vec3 spin;
                float potential;
            };

            vec3 hsv2rgb(vec3 c) {
                vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
            }

            vec3 spin_to_color(vec3 spin) {
                float s = spin.z;
                float phi = (atan(spin.y, spin.x)/M_PI+1)/2;
                vec3 hsv = vec3( phi, clamp(1-0.9*s, 0, 1), clamp(1+0.6*s, 0, 1) );
                hsv.x += u_color_shift;                        
                return hsv2rgb(hsv);
            }

            void run0(Input a, Input b) {
                // f(t)=f(0)+t*(f(1)-f(0))=0
                // t = f(0)/(f(0)-f(1)))
                float t = a.potential/(a.potential-b.potential);
                if (!(0<t && t<1)) return;
                v_position = mix(a.origin, b.origin, t);
                vec3 spin = mix(a.spin, b.spin, t); 
                if (u_neglect_z) {
                    v_color = spin_to_color(vec3(spin.xy, 0));
                } else {
                    v_color = spin_to_color(spin);
                };

                v_light_direction = - normalize(mix(a.origin, b.origin, t)-u_camera);

                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
            }

            void run(Input a, Input b, Input c, Input d) {
                // There should be no point on the edge ab.
                run0(a, c);
                run0(b, c);
                run0(a, d);
                run0(b, d);
                run0(c, d);
            }

            void process(Input a0, Input a1, Input a2, Input a3) {
                     if (sign(a0.potential)==sign(a1.potential)) run(a0, a1, a2, a3);
                else if (sign(a0.potential)==sign(a2.potential)) run(a0, a2, a1, a3);
                else if (sign(a1.potential)==sign(a2.potential)) run(a1, a2, a3, a0);
                EndPrimitive();
            }

            void interpolate(in float t0, in float t1, in float t2, in float t3, out Input res) {
                res.origin = t0*vs_in[0].origin+t1*vs_in[1].origin+t2*vs_in[2].origin+t3*vs_in[3].origin;
                res.spin = normalize(t0*vs_in[0].spin+t1*vs_in[1].spin+t2*vs_in[2].spin+t3*vs_in[3].spin);
                if (u_constant_theta) {
                    // float theta = acos(dot(res.spin, u_axis));
                    // res.potential = 2*theta/M_PI - u_level - 1.0;

                    // res.potential = cos(theta-0.5*M_PI*u_level);
                
                    float theta = dot(res.spin, u_axis);
                    res.potential = theta - u_level;
                } else {
                    float phi = atan(res.spin.y, res.spin.x);
                    res.potential = cos(phi-M_PI*u_level);
                };
            }

            void main() {
                Input a0, a1, a2, a3;
                interpolate(1, 0, 0, 0, a0);
                interpolate(0, 1, 0, 0, a1);
                interpolate(0, 0, 1, 0, a2);
                interpolate(0, 0, 0, 1, a3);
                process(a0, a1, a2, a3);

                
                Input ac;
                interpolate(0.25, 0.25, 0.25, 0.25, ac);
                process(a0, a1, a2, ac);
                process(a1, a2, a3, ac);
                process(a2, a3, a0, ac);
                process(a3, a0, a1, ac);
                

                /*
                Input a01, a02, a03, a12, a13, a23;
                interpolate(0.5, 0.5, 0, 0, a01);
                interpolate(0.5, 0, 0.5, 0, a02);
                interpolate(0.5, 0, 0, 0.5, a03);
                interpolate(0, 0.5, 0.5, 0, a12);
                interpolate(0, 0.5, 0, 0.5, a13);
                interpolate(0, 0, 0.5, 0.5, a23);
                process(a0, a01, a02, a03);
                process(a1, a01, a12, a13);
                process(a2, a02, a12, a23);
                process(a3, a03, a13, a23);
                process(a01, a02, a12, ac);
                process(a01, a03, a13, ac);
                process(a02, a03, a23, ac);
                process(a12, a13, a23, ac);
                */
            }   
        """
    FRAGMENT = """
            #version 330

            uniform vec3 u_camera;
            uniform bool u_lighting;

            // in vec3 v_normal;
            in vec3 v_position;
            in vec3 v_color;
            in vec3 v_light_direction;

            out vec4 f_color;

            void main() {
                if (u_lighting) {
                    vec3 normal = normalize(cross(dFdx(v_position), dFdy(v_position)));
                    // vec3 normal = normalize(v_normal);
                    float inner_reflected = dot(reflect(normalize(v_position-u_camera), normal), v_light_direction);
                    float inner_disperse = dot(normal, v_light_direction);
                    float intensity = 0.4+0.6*clamp(inner_disperse, 0.0, 1.0) + 0.3*clamp(inner_reflected, 0.0, 1.0);
                    f_color = vec4(intensity*v_color.xyz, 1.0);
                    // f_color = vec4(abs(normal), 1.0); // DEBUG
                } else {
                     f_color = vec4(v_color.xyz, 1.0);
                };
            }

        """

    ANGLENAMES = ["polar angle", "azimuthal angle"]

    def __init__(
        self,
        coordinatesBuffer=None,
        maskBuffer=None,
        indexBuffer=None,
        scalarMaskBuffer=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        assert self._system.dim == 3

        self.u_view = self._prog["u_view"]
        self.u_projection = self._prog["u_projection"]
        self.u_color_shift = self._prog["u_color_shift"]
        self.u_level = self._prog["u_level"]
        self.u_constant_theta = self._prog["u_constant_theta"]
        self.u_lighting = self._prog["u_lighting"]
        self.u_axis = self._prog["u_axis"]
        self.u_neglect_z = self._prog["u_neglect_z"]

        self._coordinatesBuffer = coordinatesBuffer
        self._coordinatesBuffer.upload(self._system.spin_positions())

        self._idx = indexBuffer

        self.init_vao()

        self.lighting = True
        self.inverted = True
        self.color_shift = 0.81
        self.level = 0.0
        self.constant_theta = True
        self.axis = (0, 0, 1)

    def init_vao(self):
        self._vao = self._ctx.vertex_array(
            self._prog,
            [
                (self._state.vbo, "3f/v", "in_spin"),
                (self._coordinatesBuffer.vbo, "3f/v", "in_center"),
            ],
            self._idx.ibo,
        )

    @property
    def angle_name(self):
        return self.ANGLENAMES[0 if self.constant_theta else 1]

    @angle_name.setter
    def angle_name(self, name):
        self.constant_theta = name == self.ANGLENAMES[0]
        # self.init_vao()

    def render(
        self, scales=None, modelview=None, projection=None, camera_position=None
    ):
        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())
        self.u_camera.value = tuple(camera_position)

        self.u_axis.value = self.axis
        # self.u_inverted.value = self.inverted
        self.u_constant_theta.value = self.constant_theta
        self.u_neglect_z.value = self.constant_theta
        self.u_color_shift.value = self.color_shift
        self.u_level.value = self.level
        self.u_lighting.value = self.lighting

        self._ctx.enable_only(mgl.DEPTH_TEST)

        self._vao.render(mode=mgl.LINES_ADJACENCY, vertices=-1, first=0)

    def list_properties(self):
        return [
            BooleanProperty(self, "lighting", title="Lighting"),
            BooleanProperty(self, "inverted", title="Invert colors"),
            ListProperty(self, "angle_name", title="Constant", values=self.ANGLENAMES),
            # BooleanProperty(self, "constant_theta", title="Constant z-projection of spin"),
            NumericProperty(
                self, "level", title="Level", min=-1.0, max=1.0, count=1000
            ),
            NumericProperty(
                self, "color_shift", title="Hue", min=0.0, max=1.0, count=360
            ),
        ]


####################################################################################################################
