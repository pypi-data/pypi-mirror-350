import moderngl as mgl
import numpy as np

from .render import StateRender
from .buffer import Float3DBuffer, IntBuffer
from ..core import NumericProperty, ListProperty, BooleanProperty
from .solid import ConicMesh, CylinderMesh, DoubleConeMesh, ArrowMesh


######################################################################################################


class VectorRender(StateRender):
    VERTEX = """
                #version 330

                const float M_PI = 3.1415926535897932384626433832795;

                uniform mat4 u_view;
                uniform mat4 u_projection;
                uniform bool u_negate;

                uniform vec3 u_camera; // camera position in world coordinates
                // uniform vec3 u_light_direction; // directed light source in world coordinates
                uniform bool u_use_mask; // false to display all spins
                uniform bool u_use_scalar_mask; // true to use in_scalar

                uniform float u_min_size;
                uniform float u_max_size;
                uniform float u_power_size;
                uniform float u_min_threshold;
                uniform ivec3 u_size;
                uniform ivec3 u_clip_min;
                uniform ivec3 u_clip_max; 
                uniform bool u_clip_invert; 
                uniform float u_min_scalar;
                uniform float u_max_scalar;
                uniform float u_color_shift;
                uniform bool u_director_mode;
                uniform float u_width;
                uniform float u_saturation_mag;

                in vec3 in_center; // center of atom
                in vec3 in_pos; // mesh point in mesh coordinates
                in vec3 in_normal; // normal to mesh at in_pos in mesh coordinates
                in vec3 in_spin; // spin direction
                in vec3 in_mask; // invisible direction
                in float in_scalar; // invisible direction

                out vec3 v_pos; // vertex position in world coordiantes
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

                vec3 hsv2rgb(vec3 c) {
                    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
                }

                vec3 spin_to_color(vec3 spin) {
                    if(u_director_mode) {
                        vec3 pr = spin.yzx*spin.zxy;
                        // pr /= max( max(abs(pr.x),abs(pr.y)), abs(pr.z));
                        pr /= length(pr);
                        vec3 rgb = 0.5-0.5*pr;
                        return rgb;
                    } else {
                        float s = spin.z;
                        if (u_saturation_mag!=1.0) {
                            // s = 1+(s-1)*u_saturation_mag;
                            s = cos(u_saturation_mag*acos(s));
                        };
                        float phi = (atan(spin.y, spin.x)/M_PI+1)/2;
                        vec3 hsv = vec3( phi, clamp(1-s, 0, 1), clamp(1+s, 0, 1) );
                        hsv.x += u_color_shift;                        
                        return hsv2rgb(hsv);
                    };
                }
 
                void main() {
                    float len = length(in_spin);
                    vec3 spin = u_negate?-in_spin/len:in_spin/len;
                    float scale;
                    if(u_use_mask) {
                        vec3 mask = u_negate?-in_mask:in_mask;
                        scale = u_use_scalar_mask ? (in_scalar-u_min_scalar) / (u_max_scalar-u_min_scalar) : (1 - dot(mask, spin)) / 2;
                    } else {
                        scale = 1.0;
                    };
                    scale *= len;
                    if (scale<u_min_threshold) { 
                        scale = 0;
                    } else {
                        scale = u_min_size + pow(scale, u_power_size) * (u_max_size-u_min_size);
                    };

                    int i = gl_InstanceID; int iz = i % u_size.z;
                    i /= u_size.z; int iy = i % u_size.y;
                    i /= u_size.y; int ix = i % u_size.x;
                    bool inbox = (ix<u_clip_min.x || ix>u_clip_max.x 
                        || iy<u_clip_min.y || iy>u_clip_max.y 
                        || iz<u_clip_min.z || iz>u_clip_max.z);
                    if (inbox != u_clip_invert) scale = 0;

                    mat3 mesh = rotmat(spin);
                    vec3 pos = scale*in_pos;
                    pos.xy *= u_width;
                    v_pos = in_center + mesh * pos;
                    gl_Position = u_projection * u_view * vec4(v_pos, 1.0);
                    v_normal = mesh * in_normal;

                    v_camera = u_camera; // * mat3(u_view);
                    // vec3 light_direction = u_light_direction;
                    // vec3 light_direction = - u_camera + v_pos;
                    // v_light_direction = normalize(light_direction * mat3(u_view));
                    v_light_direction = - normalize(v_pos-v_camera);

                    v_color = vec4( spin_to_color(spin), 1.0 );
                } 
            """
    GEOMETRY = None
    FRAGMENT = """
                #version 330

                uniform bool u_lighting;

                in vec3 v_normal;
                in vec3 v_pos;
                in vec4 v_color;

                in vec3 v_camera;
                in vec3 v_light_direction;

                out vec4 f_color;

                void main() {
                    if (u_lighting) {
                        vec3 normal = normalize(v_normal);
                        float inner_reflected = dot(reflect(normalize(v_pos-v_camera), normal), v_light_direction);
                        float inner_disperse = dot(normal, v_light_direction);
                        float intensity = 0.4+0.6*clamp(inner_disperse, 0.0, 1.0) + 0.3*clamp(inner_reflected, 0.0, 1.0);
                        f_color = vec4(intensity*v_color.xyz, v_color.t);
                    } else {
                        f_color = v_color;
                    };
                }
            """

    def __init__(
        self,
        _light=(1, 2, -3),
        coordinatesBuffer=None,
        maskBuffer=None,
        scalarMaskBuffer=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._coordinatesBuffer = coordinatesBuffer
        self._coordinatesBuffer.upload(self._system.spin_positions())

        self._maskBuffer = maskBuffer
        self._scalarMaskBuffer = scalarMaskBuffer

        # self.mesh = ConicMesh(mglctx=self._ctx)

        self._detalization = 1
        self._mesh_shape = "Cone"
        self.init_vao()

        self.use_mask = False
        self.use_scalar_mask = False
        self.director_mode = False
        self.base_size = 1.0
        self.min_size = 0.0
        self.max_size = 1.2
        self.min_scalar = 0.0
        self.max_scalar = 1.0
        self.power_size = 1.0
        self.min_threshold = 0.75
        assert self._system.dim == 3
        self.size = self._system.size
        self.clip_min = (0, 0, 0)
        self.clip_max = tuple(self.size)
        self.clip_invert = False
        self.color_shift = 0.81
        self.width = 0.75
        self.saturation_mag = 1.0
        self.lighting = True
        self.negate = False

    def init_vao(self):
        self.mesh = self.MESH_NAMES[self._mesh_shape](
            mglctx=self._ctx, count=int(10 * self._detalization)
        )
        self._vao = self._ctx.vertex_array(
            self._prog,
            [
                (self.mesh.pos.vbo, "3f", "in_pos"),
                (self.mesh.normal.vbo, "3f", "in_normal"),
                (self._state.vbo, "3f/i", "in_spin"),
                (self._coordinatesBuffer.vbo, "3f/i", "in_center"),
                (self._maskBuffer.vbo, "3f/i", "in_mask"),
                (self._scalarMaskBuffer.vbo, "f/i", "in_scalar"),
            ],
            self.mesh.idx.ibo,
        )

    MESH_NAMES = {
        "Cone": ConicMesh,
        "Double cone": DoubleConeMesh,
        "Cylinder": CylinderMesh,
        "Arrow": ArrowMesh,
    }

    @property
    def mesh_shape(self):
        for n, t in self.MESH_NAMES.items():
            if isinstance(self.mesh, t):
                return n
        raise NotImplementedError

    @mesh_shape.setter
    def mesh_shape(self, name):
        self._mesh_shape = name
        self.init_vao()

    @property
    def detalization(self):
        return self._detalization

    @detalization.setter
    def detalization(self, value):
        print(f"{self._detalization = },\t {value = }")
        self._detalization = value
        self.init_vao()

    def render(
        self, scales=None, modelview=None, projection=None, camera_position=None
    ):
        self.u_view.value = tuple(modelview.T.flatten())
        self.u_projection.value = tuple(projection.T.flatten())
        self.u_camera.value = tuple(camera_position)
        # self.u_light_direction.value = tuple(self._light)
        self.u_use_mask.value = self.use_mask
        self.u_min_size.value = self.min_size * self.base_size
        self.u_max_size.value = self.max_size * self.base_size
        self.u_use_scalar_mask.value = self.use_scalar_mask
        self.u_min_scalar.value = self.min_scalar
        self.u_max_scalar.value = self.max_scalar
        self.u_power_size.value = self.power_size
        self.u_min_threshold.value = self.min_threshold
        self.u_size.value = tuple(self.size)
        self.u_clip_min.value = tuple(np.array(self.clip_min, dtype=np.int32))
        self.u_clip_max.value = tuple(np.array(self.clip_max, dtype=np.int32))
        self.u_clip_invert.value = self.clip_invert
        self.u_color_shift.value = self.color_shift
        self.u_director_mode.value = self.director_mode
        self.u_width.value = self.width
        self.u_saturation_mag.value = self.saturation_mag
        self.u_lighting.value = self.lighting
        self.u_negate.value = self.negate

        self._vao.render(
            mode=mgl.TRIANGLES,
            instances=self._system.number_of_spins,
            vertices=-1,
            first=0,
        )

        # print(self.u_min_scalar.value, self.u_max_scalar.value, self.u_use_scalar_mask.value, self.u_use_mask.value,)

    def list_properties(self):
        return [
            BooleanProperty(self, "lighting", title="Lighting"),
            ListProperty(
                self, "mesh_shape", title="Shape", values=sorted(self.MESH_NAMES.keys())
            ),
            BooleanProperty(self, "director_mode", title="Director mode"),
            BooleanProperty(self, "negate", title="Negate spin"),
            NumericProperty(self, "width", title="Width", min=0.01, max=2.0, count=100),
            NumericProperty(
                self, "color_shift", title="Hue", min=0.0, max=1.0, count=360
            ),
            NumericProperty(
                self, "saturation_mag", title="Saturation", min=1.0, max=10.0, count=500
            ),
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
                count=500,
            ),
            NumericProperty(
                self, "detalization", title="Detalization", min=1.0, max=10.0, count=10
            ),
        ]
