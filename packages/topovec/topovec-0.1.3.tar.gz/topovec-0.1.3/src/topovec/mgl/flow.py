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

# /// Random number generator
# // https://stackoverflow.com/questions/4200224/random-noise-functions-for-glsl
# // A single iteration of Bob Jenkins' One-At-A-Time hashing algorithm.
# uint hash( uint x ) {
#     x += ( x << 10u );
#     x ^= ( x >>  6u );
#     x += ( x <<  3u );
#     x ^= ( x >> 11u );
#     x += ( x << 15u );
#     return x;
# }

# // Compound versions of the hashing algorithm I whipped together.
# uint hash( uvec2 v ) { return hash( v.x ^ hash(v.y)                         ); }
# uint hash( uvec3 v ) { return hash( v.x ^ hash(v.y) ^ hash(v.z)             ); }
# uint hash( uvec4 v ) { return hash( v.x ^ hash(v.y) ^ hash(v.z) ^ hash(v.w) ); }

# // Construct a float with half-open range [0:1] using low 23 bits.
# // All zeroes yields 0.0, all ones yields the next smallest representable value below 1.0.
# float floatConstruct( uint m ) {
#     const uint ieeeMantissa = 0x007FFFFFu; // binary32 mantissa bitmask
#     const uint ieeeOne      = 0x3F800000u; // 1.0 in IEEE binary32

#     m &= ieeeMantissa;                     // Keep only mantissa bits (fractional part)
#     m |= ieeeOne;                          // Add fractional part to 1.0

#     float  f = uintBitsToFloat( m );       // Range [1:2]
#     return f - 1.0;                        // Range [0:1]
# }

# // Pseudo-random value in half-open range [0:1].
# float random( float x ) { return floatConstruct(hash(floatBitsToUint(x))); }
# float random( vec2  v ) { return floatConstruct(hash(floatBitsToUint(v))); }
# float random( vec3  v ) { return floatConstruct(hash(floatBitsToUint(v))); }
# float random( vec4  v ) { return floatConstruct(hash(floatBitsToUint(v))); }

# vec3 random_vec() {
#     float r = floatConstruct(uint(gl_PrimitiveIDIn));
#     float g = random(r);
#     float b = random(g);
#     return vec3(r,g,b);
# }

# /// END random number generator


class FlowRender(StateRender):
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
                if (u_negate) spin = -spin;
                vs_out.origin = in_center;
                vs_out.spin = spin;
                if (u_neglect_z) {
                    vs_out.color = spin_to_color(vec3(spin.xy, 0));
                } else {
                    vs_out.color = spin_to_color(spin);
                };
            } 
        """

    GEOMETRY = """
            #version 330 core

            const float M_PI = 3.1415926535897932384626433832795;

            layout (lines_adjacency) in;

            layout (triangle_strip, max_vertices = 20) out;
//            layout (line_strip, max_vertices = 78) out;
//            layout (points, max_vertices = 4) out;

            uniform vec3 u_axis; // Zenith direction.
            uniform float u_level;
            uniform bool u_constant_theta;
            uniform int u_nparts=1;
            uniform int u_part_x=0;
            uniform int u_part_y=0;
            uniform int u_part_z=0;

            uniform mat4 u_view;
            uniform mat4 u_projection;

            uniform vec4 u_clip;

            uniform bool u_inverted;

            in VS_OUT {
                vec3 origin;
                vec3 spin;
                vec3 color;
            } vs_in[];

            out vec3 v_position;
            out vec3 v_color;
            out float v_clip;

            vec3 baryint(vec4 x, vec3 a, vec3 b, vec3 c, vec3 d) {
                return x[0]*a+x[1]*b+x[2]*c+x[3]*d;
            };

            void run0(vec4 a, vec4 b, vec2 phi) {
                // f(t)=f(0)+t*(f(1)-f(0))=0
                // t = f(0)/(f(0)-f(1)))
                float t = phi.x/(phi.x-phi.y);
                if (t<0 || t>1) return;
                v_position = mix(
                    baryint(a, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin), 
                    baryint(b, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin), 
                    t);
                v_color = mix(
                    baryint(a, vs_in[0].color, vs_in[1].color, vs_in[2].color, vs_in[3].color), 
                    baryint(b, vs_in[0].color, vs_in[1].color, vs_in[2].color, vs_in[3].color), 
                    t);

                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                v_clip = dot(vec4(v_position,1.0), u_clip); 
                EmitVertex();
            };

            void run(vec4 x, vec4 y, vec4 z, vec4 w, vec4 phi) {
                // There should be no point on the edge ab.
                run0(x, z, phi.xz);
                run0(y, z, phi.yz);
                run0(x, w, phi.xw);
                run0(y, w, phi.yw);
                run0(z, w, phi.zw); 

                /* For debug only.
                run0(x, z, phi.xz);
                run0(y, z, phi.yz);
                run0(x, w, phi.xw);
                run0(y, w, phi.yw);
                */

                EndPrimitive();
            };

            float potential(vec3 spin) {
                spin = normalize(spin); 
                if (u_constant_theta) {
                    return dot(spin, u_axis)-u_level;
                    // float theta = acos(dot(spin, u_axis));
                    // return cos(theta-0.5*M_PI*u_level);
                } else {
                    float phi = atan(spin.y, spin.x);
                    return cos(phi-M_PI*u_level);
                };
            };

            void process_simplex(vec4 x, vec4 y, vec4 z, vec4 w) {
                /* For debug only. Draw simplex in line-strip mode.
                v_color = vec3(0,0,0);
                v_position = baryint(x, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(y, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(z, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(w, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(x, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(z, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(y, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                v_position = baryint(w, vs_in[0].origin, vs_in[1].origin, vs_in[2].origin, vs_in[3].origin);
                gl_Position = u_projection * u_view * vec4(v_position, 1.0);
                EmitVertex();
                EndPrimitive();
                */

                vec4 phi = vec4(
                    potential(baryint(x, vs_in[0].spin, vs_in[1].spin, vs_in[2].spin, vs_in[3].spin)),
                    potential(baryint(y, vs_in[0].spin, vs_in[1].spin, vs_in[2].spin, vs_in[3].spin)),
                    potential(baryint(z, vs_in[0].spin, vs_in[1].spin, vs_in[2].spin, vs_in[3].spin)),
                    potential(baryint(w, vs_in[0].spin, vs_in[1].spin, vs_in[2].spin, vs_in[3].spin))
                );

                if (phi.x>0 && phi.y>0 && phi.z>0 && phi.w>0) return;
                if (phi.x<0 && phi.y<0 && phi.z<0 && phi.w<0) return;

                if      ((phi.x>0 && phi.y>0) || (phi.x<0 && phi.y<0)) run(x, y, z, w, phi.xyzw);
                else if ((phi.x>0 && phi.z>0) || (phi.x<0 && phi.z<0)) run(x, z, y, w, phi.xzyw);
                else run(z, y, x, w, phi.zyxw);
            };

            void main() {
                int w=u_nparts-1-u_part_x-u_part_y-u_part_z;
                vec4 o=vec4(u_part_x,u_part_y,u_part_z,w);
                
                process_simplex(
                    (o+vec4(1,0,0,0))/u_nparts,
                    (o+vec4(0,1,0,0))/u_nparts,
                    (o+vec4(0,0,1,0))/u_nparts,
                    (o+vec4(0,0,0,1))/u_nparts
                );
                
                if (u_part_x>0) {
                    process_simplex(
                        (o+vec4(0,0,0,1))/u_nparts,
                        (o+vec4(-1,0,1,1))/u_nparts,
                        (o+vec4(-1,1,1,0))/u_nparts,
                        (o+vec4(0,0,1,0))/u_nparts
                    );
                    
                    process_simplex(
                        (o+vec4(0,0,0,1))/u_nparts,
                        (o+vec4(0,1,0,0))/u_nparts,
                        (o+vec4(-1,1,1,0))/u_nparts,
                        (o+vec4(0,0,1,0))/u_nparts
                    );
                    
                    process_simplex(
                        (o+vec4(0,0,0,1))/u_nparts,
                        (o+vec4(-1,0,1,1))/u_nparts,
                        (o+vec4(-1,1,1,0))/u_nparts,
                        (o+vec4(-1,1,0,1))/u_nparts
                    );
                    
                    process_simplex(
                        (o+vec4(0,0,0,1))/u_nparts,
                        (o+vec4(0,1,0,0))/u_nparts,
                        (o+vec4(-1,1,1,0))/u_nparts,
                        (o+vec4(-1,1,0,1))/u_nparts
                    );
                };
            };
        """
    FRAGMENT = """
            #version 330

            uniform vec3 u_camera;
            uniform bool u_lighting;

            in vec3 v_position;
            in vec3 v_color;
            in float v_clip;

            out vec4 f_color;

            void main() {
                if(v_clip<0) discard;
                if (u_lighting) {
                    vec3 normal = normalize(cross(dFdx(v_position), dFdy(v_position)));
                    vec3 light_direction = -normalize(v_position-u_camera);
                    float inner_reflected = dot(light_direction, normal);
                    float intensity = 0.4+0.6*clamp(inner_reflected, 0.0, 1.0);
                    f_color = vec4(intensity*v_color.xyz, 1.0);
                    // f_color = vec4(abs(normal), 1.0); // DEBUG
                } else {
                    f_color = vec4(v_color.xyz, 1.0);
                };
            }

        """

    ANGLENAMES = ["polar angle", "azimuthal angle", "energy density"]

    def __init__(
        self,
        coordinatesBuffer: Float3DBuffer = None,
        maskBuffer=None,
        indexBuffer=None,
        scalarMaskBuffer=None,
        **kwargs,
    ):

        super().__init__(**kwargs)

        assert self._system.dim == 3

        self._coordinatesBuffer = coordinatesBuffer
        self._idx = indexBuffer

        self.init()

    def init(self):
        self._coordinatesBuffer.upload(self._system.spin_positions())

        self.init_vao()

        self.lighting = True
        self.inverted = True
        self.negate = False
        self.color_shift = 0.81
        self._level = 0.0
        self.constant_theta = True
        self.axis = (0, 0, 1)
        self.nparts = 1
        self.neglect_z = False
        self._levels_number = 1.0
        self.cutx, self.cuty, self.cutz = -1.0, 0.0, 0.0
        self.cutphi, self.cuttheta = 0.0, 0.0
        self.levels = []

        self.update_levels()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self.update_levels()

    @property
    def levels_number(self):
        return self._levels_number

    @levels_number.setter
    def levels_number(self, value):
        self._levels_number = value
        self.update_levels()

    def update_levels(self):
        self.levels = list(
            (self.level + n + 0.5) * 2.0 / self._levels_number - 1.0
            for n in range(int(self._levels_number))
        )

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
        number_of_levels = int(self.levels_number)

        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())
        self.u_camera.value = tuple(camera_position)

        self.u_axis.value = self.axis
        self.u_constant_theta.value = self.constant_theta
        self.u_neglect_z.value = self.neglect_z  # or self.constant_theta
        self.u_color_shift.value = self.color_shift
        self.u_lighting.value = self.lighting
        self.u_negate.value = self.negate

        self._ctx.enable_only(mgl.DEPTH_TEST)

        nparts = int(self.nparts)
        assert nparts > 0
        self.u_nparts.value = nparts

        cutxyz = np.array([self.cutx, self.cuty, self.cutz])
        cutdir = np.array(
            [
                np.cos(np.pi * self.cutphi) * np.cos(np.pi * self.cuttheta),
                np.sin(np.pi * self.cutphi) * np.cos(np.pi * self.cuttheta),
                np.sin(np.pi * self.cuttheta),
            ]
        )
        self.u_clip.value = tuple(cutdir) + (-np.sum(cutdir * cutxyz),)

        for level in self.levels:
            # Render one surface level
            self.u_level.value = level
            for x in range(nparts):
                for y in range(nparts - x):
                    for z in range(nparts - x - y):
                        self.u_part_x.value = x
                        self.u_part_y.value = y
                        self.u_part_z.value = z
                        self._vao.render(mode=mgl.LINES_ADJACENCY, vertices=-1, first=0)

    def list_properties(self):
        maxxyz = self._system.center + self._system.lengths / 2
        minxyz = self._system.center - self._system.lengths / 2
        return [
            BooleanProperty(self, "lighting", title="Lighting"),
            BooleanProperty(self, "inverted", title="Invert colors"),
            BooleanProperty(self, "neglect_z", title="Ignore z-projection"),
            BooleanProperty(self, "negate", title="Negate spin"),
            ListProperty(self, "angle_name", title="Constant", values=self.ANGLENAMES),
            NumericProperty(
                self, "level", title="Level", min=-1.0, max=1.0, count=1000
            ),
            NumericProperty(
                self, "color_shift", title="Hue", min=0.0, max=1.0, count=360
            ),
            # NumericProperty(self, "nparts", title="Detalization", min=1.0, max=4.0, count=4),
            NumericProperty(
                self, "levels_number", title="#levels", min=1.0, max=10.0, count=10
            ),
            NumericProperty(
                self, "cutx", title="Cut X", min=minxyz[0], max=maxxyz[0], count=1000
            ),
            NumericProperty(
                self, "cuty", title="Cut Y", min=minxyz[1], max=maxxyz[1], count=1000
            ),
            NumericProperty(
                self, "cutz", title="Cut Z", min=minxyz[2], max=maxxyz[2], count=1000
            ),
            NumericProperty(
                self, "cutphi", title="Cut phi", min=0.0, max=2.0, count=1000
            ),
            NumericProperty(
                self, "cuttheta", title="Cut theta", min=-0.5, max=0.5, count=1000
            ),
        ]


####################################################################################################################


class AstraRender(FlowRender):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 0.7
        self.npetals = 2
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
        self.u_constant_theta.value = True
        self.u_color_shift.value = self.color_shift
        self.u_level.value = self.level
        self.u_lighting.value = self.lighting
        self.u_neglect_z.value = self.neglect_z

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
            BooleanProperty(self, "neglect_z", title="Ignore z-projection"),
            NumericProperty(
                self, "level", title="Thickness", min=1.0, max=0.5, count=1000
            ),
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
        ]
