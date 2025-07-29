import moderngl as mgl
import numpy as np

from ..core import System


class Render:
    """
    Abstract class to run ModernGL based render.
    """

    VERTEX = """
                #version 330
                in vec3 in_spin;
                void main() {
                    gl_Position = vec4(in_spin, 1.0);
                }
            """
    GEOMETRY = None
    FRAGMENT = """
                #version 330
                out vec4 f_color;
                void main() {
                    f_color = vec4(1.0,1.0,1.0,1.0);
                }
            """

    def __init__(self, mglctx: mgl.Context = None):
        self._ctx = mglctx

        self._prog = self._ctx.program(
            vertex_shader=self.VERTEX,
            geometry_shader=self.GEOMETRY,
            fragment_shader=self.FRAGMENT,
        )

        self.populate_uniforms()

    def populate_uniforms(self):
        for u in self._prog:
            obj = self._prog[u]
            if isinstance(obj, mgl.Uniform):
                self.__dict__[u] = obj

    def render(self, **kwargs):
        self._ctx.clear(0.60, 0.60, 0.60)

    def list_properties(self):
        return []


####################################################################################


class StateRender(Render):
    """
    Abstract class for magnetization render.
    """

    def __init__(
        self,
        mglctx: mgl.Context = None,
        system: System = None,
        stateBuffer: np.ndarray = None,
    ):
        super().__init__(mglctx=mglctx)
        self._system = system
        self._state = stateBuffer

        self._vao = self._ctx.vertex_array(
            self._prog,
            [
                (self._state.vbo, "3f", "in_spin"),
            ],
        )
