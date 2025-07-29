import numpy as np

from ..core import System, log
from .image import ImageContainer
from .camera import Camera
from .scene import LayerScene, FlowScene, IsolinesScene, SCENES


def render_prepare(
    scenecls: str,
    system: System,
    camera_preset: int = 2,
    scalex: bool = False,
    imgsize: int = 1024,
):
    """Prepare scene to offscreen render. single layer render.

    Arguments:
        scenecls: scene class to instantiate. Can be defined by name according to `mgl.print_scenes()`.

    Example:

    ic = render_layer(system) # Create render.
    ic.upload(director) # Specify director field to render.
    ic.save() # Render.
    """

    # Setup camera.
    camera = Camera()
    # Preset 0-2 define axis to look along.
    aspectratio = (
        camera.set_predefined_direction(preset=camera_preset)
        .adjust_fov(system)
        .adjust_scale(system)
    )

    # Define image size
    size = (
        (int(imgsize * aspectratio), imgsize)
        if scalex
        else (imgsize, int(imgsize / aspectratio))
    )

    # Select scene to render.
    if isinstance(scenecls, str):
        scenecls = SCENES[scenecls]

    # Initialize image to render to.
    ic = ImageContainer(
        size=size,
        scene=lambda mglctx: scenecls(mglctx=mglctx, system=system, camera=camera),
    )

    return ic


#############################################################################################################


def render_layer(
    system: System,
    scalex: bool = False,
    imgsize: int = 1024,
    show_axes: bool = False,
    layer: int = 0,
    axis: int = 2,
    mesh: str = "Cylinder",
):
    """Prepare single layer render.

    Example:

    ic = render_layer(system) # Create render.
    ic.upload(director) # Specify director field to render.
    ic.save() # Render.
    """

    # Check parameters.
    if not 0 <= axis < 3:
        raise ValueError(f"Axis should be 0 (x-axis), 1 (y-axis) or 2 (z-axis).")

    if not 0 <= layer < system.size[axis]:
        raise ValueError(
            f"Layer {layer} is outside of allowed range 0 .. {system.size[axis]}"
        )

    # Setup camera.
    camera = Camera()
    # Preset 0-2 define axis to look along.
    aspectratio = (
        camera.set_predefined_direction(preset=axis)
        .adjust_fov(system)
        .adjust_scale(system)
    )
    # log.debug(f"Aspect ratio {aspectratio:.2f}")

    # Define image size
    size = (
        (int(imgsize * aspectratio), imgsize)
        if scalex
        else (imgsize, int(imgsize / aspectratio))
    )

    # Select scene to render.
    scenecls = LayerScene  # Render single layer.

    # Initialize image to render to.
    ic = ImageContainer(
        size=size,
        scene=lambda mglctx: scenecls(mglctx=mglctx, system=system, camera=camera),
    )

    # Tune system parameters if needed.
    ic.scene.axis = axis
    ic.scene.layer = layer

    ic.scene.vector_render.mesh_shape = mesh
    # ic.scene.vector_render.base_size = thinning*0.9
    # ic.scene.vector_render.saturation_mag = mag

    return ic


################################################################################################################################


def render_isosurface(
    system: System,
    scalex: bool = False,
    imgsize: int = 1024,
    show_axes: bool = False,
    preset: int = 2,
    levels: list[float] = [0],
    lighting: bool = True,
    neglect_z: bool = True,
):
    """Prepare iso-surface render.

    Example:

    ic = render_layer(system) # Create render.
    ic.upload(director) # Specify director field to render.
    ic.save() # Render.
    """

    # Setup camera.
    camera = Camera()
    # Preset 0-2 define axis to look along.
    aspectratio = (
        camera.set_predefined_direction(preset=preset)
        .adjust_fov(system)
        .adjust_scale(system)
    )

    # Define image size
    size = (
        (int(imgsize * aspectratio), imgsize)
        if scalex
        else (imgsize, int(imgsize / aspectratio))
    )

    # Select scene to render.
    scenecls = FlowScene  # Render single layer.

    # Initialize image to render to.
    ic = ImageContainer(
        size=size,
        scene=lambda mglctx: scenecls(mglctx=mglctx, system=system, camera=camera),
    )

    ic.scene.surface_render.neglect_z = False
    ic.scene.surface_render.levels = levels
    # ic.scene.surface_render.cutx = lx
    # ic.scene.surface_render.cuty = ly
    # ic.scene.surface_render.cutphi = np.pi/2
    ic.scene.surface_render.lighting = lighting
    ic.scene.surface_render.neglect_z = neglect_z

    return ic


################################################################################################################################


def render_isolines(
    system: System,
    scalex: bool = False,
    imgsize: int = 1024,
    show_axes: bool = False,
    preset: int = 2,
    levels: list[float] = [0],
    lighting: bool = True,
    neglect_z: bool = True,
    thickness: float = 0.002,
    nlines: int = 5,
    z0: float = 0.0,
    phi0: float = 0.0,
):
    """Prepare iso-lines render.

    Arguments:
        thickness # Isoline thickness
        nlines # Number of isolines
        phi0   # Orientation of xy-projection of projector for isolines:
        z0     # z-projection of director for isolines.
               # S=(sqrt(1-z0^2) cos phi0, sqrt(1-z0^2) sin phi0, z0)

    Example:

    ic = render_layer(system) # Create render.
    ic.upload(director) # Specify director field to render.
    ic.save() # Render.
    """

    # Setup camera.
    camera = Camera()
    # Preset 0-2 define axis to look along.
    aspectratio = (
        camera.set_predefined_direction(preset=preset)
        .adjust_fov(system)
        .adjust_scale(system)
    )

    # Define image size
    size = (
        (int(imgsize * aspectratio), imgsize)
        if scalex
        else (imgsize, int(imgsize / aspectratio))
    )

    # Select scene to render.
    scenecls = IsolinesScene  # Render single layer.

    # Initialize image to render to.
    ic = ImageContainer(
        size=size,
        scene=lambda mglctx: scenecls(mglctx=mglctx, system=system, camera=camera),
    )

    ic.scene.isolines_render.neglect_z = False
    ic.scene.isolines_render.levels = levels
    ic.scene.isolines_render.lighting = lighting
    ic.scene.isolines_render.neglect_z = neglect_z
    ic.scene.isolines_render.width = thickness
    # k = np.round( (nlines-1) )#/np.sqrt(1-z0**2) )
    ic.scene.isolines_render.npetals = nlines - 1
    ic.scene.isolines_render.phi_shift = phi0 / (2 * np.pi) * nlines
    ic.scene.isolines_render.theta_shift = np.arcsin(z0)

    ic.scene.show_axes = show_axes
    ic.scene.axes_render.location = (-0.9, -0.6)

    return ic
