# import struct
from typing import Callable
import moderngl as mgl
from PIL import Image, ImageOps

# from .buffer import Field3DBuffer
# from ..core import System
from .scene import Scene


class ImageContainer(object):
    def __init__(self, size=(1024, 1024), scene: Callable[[mgl.Context], Scene] = None):
        self._ctx = mgl.create_standalone_context()
        self._size = size
        self._color_rbo = self._ctx.renderbuffer(self._size)
        self._depth_rbo = self._ctx.depth_renderbuffer(self._size)
        self._fbo = self._ctx.framebuffer(self._color_rbo, self._depth_rbo)
        self._scene = None
        if not scene is None:
            self.attach_scene(scene)

    @property
    def scene(self):
        return self._scene

    def attach_scene(self, scene: Callable[[mgl.Context], Scene]):
        self._scene = scene(self._ctx)
        return self

    def upload(self, state):
        if self._scene is None:
            raise Exception("Scene should be attached first")
        self._scene.upload(state)
        return self

    def _render(self):
        self._fbo.use()
        self._scene.render(aspectratio=self._size[0] / self._size[1])

    def save(self, filename=None, crop=False):
        self._render()

        img = Image.frombytes("RGB", self._size, self._fbo.read())
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        if crop:
            inverted = ImageOps.invert(img)
            imageBox = inverted.getbbox()
            img = img.crop(imageBox)

        if filename is not None:
            img.save(filename)
            return self
        else:
            return img
