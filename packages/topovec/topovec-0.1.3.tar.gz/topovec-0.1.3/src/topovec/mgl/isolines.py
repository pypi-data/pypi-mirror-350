import moderngl as mgl
import numpy as np

from .render import *
from .buffer import Float3DBuffer, IntBuffer
from ..core import NumericProperty, ListProperty, BooleanProperty


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


class IsolineRender(StateRender):
    VERTEX = """
            #version 330

            const float M_PI = 3.1415926535897932384626433832795;

            uniform vec3 u_camera; // camera position in world coordinates
            uniform float u_color_shift;
            uniform bool u_neglect_z; 
            uniform bool u_negate;

            in vec3 in_center; // center of atom
            in vec3 in_spin; // spin direction

            out VS_OUT {
                vec3 origin; // atom position in world coordiantes
                vec3 spin; // spin direction in spin space
                vec3 light_direction; 
                vec3 color;
            } vs_out;

            vec3 hsv2rgb(vec3 c) {
                vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
            }

            vec3 spin_to_color(vec3 spin) {
                float s = spin.z;
                float phi = (atan(spin.y, spin.x)/M_PI+1)/2;;
                vec3 hsv = vec3( phi, clamp(1-0.9*s, 0, 1), clamp(1+0.6*s, 0, 1) );
                hsv.x += u_color_shift;                        
                return hsv2rgb(hsv);
            }

            void main() {
                vec3 spin = normalize(in_spin);
                if(u_negate) spin=-spin;
                vs_out.origin = in_center;
                vs_out.spin = spin;
                vs_out.light_direction = - normalize(vs_out.origin-u_camera);
                if (u_neglect_z) {
                    vs_out.color = spin_to_color(vec3(spin.xy, 0));
                } else {
                    vs_out.color = spin_to_color(spin);
                };
            } 
        """
    GEOMETRY = """
            #version 330 core

            layout (lines_adjacency) in;
            layout (triangle_strip, max_vertices = 8) out;

            uniform mat4 u_view;
            uniform mat4 u_projection;
            uniform float u_width=0.0;

            uniform bool u_inverted;
            uniform vec3 u_axis; // Direction of the vector field on the isoline.


            in VS_OUT {
                vec3 origin; // atom position in world coordiantes
                vec3 spin; // spin direction in spin space
                vec3 light_direction; 
                vec3 color;
            } vs_in[];

            out vec3 v_position;
            out vec3 v_color;
            out vec3 v_light_direction;
            // out vec3 v_normal;

            int idx;
            struct {
                vec3 position;
                vec3 color;
                vec3 light_direction;
                vec4 glposition;
            } data[4];

            void run(int a, int b, int c) {
                // Compute barycentric coordinates q of u_axis in triangle in spanned by three spins a,b,c.
                // q.x+q.y+q.z=1, and a*q.x+b*q.y+c*q.z=q.t*u_axis
                mat4 m = mat4( 
                    vec4( vs_in[a].spin, 1.0 ),
                    vec4( vs_in[b].spin, 1.0 ),
                    vec4( vs_in[c].spin, 1.0 ),
                    vec4( -u_axis, 0.0)
                );
                vec4 q = inverse(m) * vec4(0.0,0.0,0.0,1.0) ;
                if(q.w<0) q=-q;
                // If u_axis is inside the spherical triangle spanned by a,b,c, then add the point to the curve.
                if(q.x>0 && q.y>0 && q.z>0 && q.w>0) {
                    data[idx].position = q.x*vs_in[a].origin + q.y*vs_in[b].origin + q.z*vs_in[c].origin;
                    data[idx].color = q.x*vs_in[a].color + q.y*vs_in[b].color + q.z*vs_in[c].color;
                    data[idx].light_direction = q.x*vs_in[a].light_direction + q.y*vs_in[b].light_direction + q.z*vs_in[c].light_direction;
                    data[idx].glposition = u_projection * u_view * vec4(data[idx].position, 1.0);
                    idx += 1;
                };
            }

            void main() {
                idx = 0;
                // Find intersections with the simplex.
                // v_color = random_vec();
                run(0, 1, 2);
                run(1, 2, 3);
                run(2, 3, 0);
                run(3, 0, 1);      

                // Generate vertices.
                for(int n=0; n<idx; n++) {
                    // Compute normal to the line.
                    vec2 tangent=vec2(0.,0.);
                    if(n>0) {
                        tangent += normalize(data[n].glposition.xy - data[n-1].glposition.xy);
                    };
                    if(n<idx-1) {
                        tangent += normalize(data[n+1].glposition.xy - data[n].glposition.xy);
                    };
                    tangent = normalize(tangent);
                    vec2 normal = vec2(-tangent.y,tangent.x); 

                    // Emit vertices.
                    v_position = data[n].position;
                    v_color = data[n].color;
                    v_light_direction = data[n].light_direction;
                    vec2 xy = data[n].glposition.xy;
                    if(n==0) xy-=tangent*u_width/4;
                    if(n==idx-1) xy+=tangent*u_width/4;
                    gl_Position = vec4(xy+normal*u_width, data[n].glposition.z, 1.0);
                    EmitVertex();                    

                    gl_Position = vec4(xy-normal*u_width, data[n].glposition.z, 1.0);
                    EmitVertex();                    
                };
                EndPrimitive();
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

    def __init__(
        self,
        coordinatesBuffer: Float3DBuffer = None,
        maskBuffer: Float3DBuffer = None,
        indexBuffer: IntBuffer = None,
        scalarMaskBuffer=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        assert self._system.dim == 3

        self._coordinatesBuffer = coordinatesBuffer
        self._coordinatesBuffer.upload(self._system.spin_positions())

        self._idx = indexBuffer

        self.init_vao()

        self.lighting = False
        self.inverted = True
        self.negate = False
        self.color_shift = 0.81
        self.axis = (0, 0, 1)
        self.neglect_z = False
        self.width = 0.01

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
        self.u_camera.value = tuple(camera_position)

        self.u_color_shift.value = self.color_shift
        self.u_lighting.value = self.lighting
        self.u_negate.value = self.negate
        self.u_axis.value = self.axis
        self.u_neglect_z.value = self.neglect_z
        # self.u_inverted.value = self.inverted
        self.u_width.value = self.width

        self._ctx.enable_only(mgl.DEPTH_TEST)

        self._ctx.line_width = 2
        self._vao.render(mode=mgl.LINES_ADJACENCY, vertices=-1, first=0)

    def list_properties(self):
        return [
            BooleanProperty(self, "lighting", title="Lighting"),
            BooleanProperty(self, "inverted", title="Invert colors"),
            BooleanProperty(self, "negate", title="Negate spin"),
            BooleanProperty(self, "neglect_z", title="Ignore z-projection"),
            NumericProperty(
                self, "color_shift", title="Hue", min=0.0, max=1.0, count=360
            ),
            NumericProperty(
                self, "width", title="Width", min=0.0, max=0.02, count=1000
            ),
        ]


####################################################################################################################


class IsolinesRender(IsolineRender):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.npetals = 16
        self.ntheta = 1
        self.theta_shift = 0
        self.phi_shift = 0

    def render(
        self, scales=None, modelview=None, projection=None, camera_position=None
    ):
        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())
        self.u_camera.value = tuple(camera_position)

        # self.u_inverted.value = self.inverted
        self.u_color_shift.value = self.color_shift
        self.u_lighting.value = self.lighting
        self.u_neglect_z.value = self.neglect_z
        self.u_negate.value = self.negate
        self.u_width.value = self.width
        # self._ctx.enable_only(mgl.DEPTH_TEST)
        thetas = np.linspace(0, np.pi / 2, int(np.round(self.ntheta)), endpoint=False)
        theta_offset = np.pi / 2 / len(thetas) * self.theta_shift
        for theta in thetas:
            z, xy = np.sin(theta + theta_offset), np.cos(theta + theta_offset)
            k = int(np.round(np.cos(theta) * self.npetals)) + 1
            phi_offset = 2 * np.pi / k * self.phi_shift
            for phi in np.linspace(0, 2 * np.pi, k, endpoint=False) + phi_offset:
                x, y = xy * np.cos(phi), xy * np.sin(phi)
                self.u_axis.value = (x, y, z)
                self._vao.render(mode=mgl.LINES_ADJACENCY, vertices=-1, first=0)
        for theta in -thetas[1:]:
            z, xy = np.sin(theta + theta_offset), np.cos(theta + theta_offset)
            k = int(np.round(np.cos(theta) * self.npetals)) + 1
            phi_offset = 2 * np.pi / k * self.phi_shift
            for phi in np.linspace(0, 2 * np.pi, k, endpoint=False) + phi_offset:
                x, y = xy * np.cos(phi), xy * np.sin(phi)
                self.u_axis.value = (x, y, z)
                self._vao.render(mode=mgl.LINES_ADJACENCY, vertices=-1, first=0)

    def list_properties(self):
        return [
            BooleanProperty(self, "lighting", title="Lighting"),
            BooleanProperty(self, "inverted", title="Invert colors"),
            BooleanProperty(self, "negate", title="Negate spin"),
            BooleanProperty(self, "neglect_z", title="Ignore z-projection"),
            NumericProperty(
                self,
                "phi_shift",
                title="Polar angle offset",
                min=-1.0,
                max=1.0,
                count=1000,
            ),
            NumericProperty(
                self,
                "theta_shift",
                title="Azimuthal angle offset",
                min=-1.0,
                max=1.0,
                count=1000,
            ),
            NumericProperty(
                self, "npetals", title="Polar angle substeps", min=1, max=10, count=10
            ),
            NumericProperty(
                self, "ntheta", title="Azimuthal angle substeps", min=1, max=5, count=5
            ),
            NumericProperty(
                self, "color_shift", title="Hue", min=0.0, max=1.0, count=360
            ),
            NumericProperty(
                self, "width", title="Width", min=0.0, max=0.02, count=1000
            ),
        ]
