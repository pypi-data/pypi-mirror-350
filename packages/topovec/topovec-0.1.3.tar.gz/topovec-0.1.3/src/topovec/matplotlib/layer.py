import numpy as np
import matplotlib.pyplot as plt

from ..core import vector_to_rgb


def render_layer(
    director: np.ndarray,
    axis: int = 2,
    layer: int = 0,
    colormap=None,
    gridstep: float = 1,
    imagewidth_inch: float = 15,
    interpolation="none",
    length_unit="μm",
):
    if colormap is None:
        colormap = vector_to_rgb

    m = director[:, :, :, 0, :]

    if axis == 0:  # x-axis
        section = m[layer, :, :]
        axes = ["y", "z"]
    elif axis == 1:  # y-axis
        section = m[:, layer, :]
        axes = ["x", "z"]
    elif axis == 2:  # z-axis
        section = m[:, :, layer]
        axes = ["x", "y"]
    else:
        raise ValueError(f"Unsupported axis {axis}.")

    rgb = colormap(section)
    width, height, _ = section.shape
    aspectratio = width / height

    fig, ax = plt.subplots(figsize=(imagewidth_inch, imagewidth_inch / aspectratio))
    ax.imshow(
        rgb.transpose(1, 0, 2),
        origin="lower",
        extent=(0, gridstep * width, 0, gridstep * height),
        interpolation=interpolation,
        aspect="equal",
    )

    ax.set_xlabel(f"{axes[0]} [{length_unit}]")
    ax.set_ylabel(f"{axes[1]} [{length_unit}]")

    return fig, ax


#########################################################################################################################################


def plot_bloch_sphere(
    axis=2, colormap=None, size: int = 1024, imagewidth_inch: float = 5
):
    if colormap is None:
        colormap = vector_to_rgb

    # Bloch sphere plot.
    a = np.linspace(-1, 1, size)

    if axis == 0:  # x-axis
        y, z = np.meshgrid(a, a, indexing="ij")
        x = -np.sqrt(1 - y**2 - z**2)
        axes = ["y", "z"]
        yorigin = "lower"
    elif axis == 1:  # y-axis
        x, z = np.meshgrid(a, a, indexing="ij")
        y = -np.sqrt(1 - x**2 - z**2)
        axes = ["x", "z"]
        yorigin = "lower"
    elif axis == 2:  # z-axis
        x, y = np.meshgrid(a, a, indexing="ij")
        z = np.sqrt(1 - x**2 - y**2)
        axes = ["x", "y"]
        yorigin = "lower"
    else:
        raise ValueError(f"Unsupported axis {axis}.")

    xyz = np.stack([x, y, z], axis=-1)
    rgb = colormap(xyz)
    fig, ax = plt.subplots(figsize=(imagewidth_inch,) * 2, layout="compressed")
    ax.imshow(
        rgb.transpose(1, 0, 2),
        extent=[-1, 1, -1, 1] if yorigin == "lower" else [-1, 1, 1, -1],
        origin=yorigin,
    )
    ax.set_xlabel(axes[0])
    ax.set_ylabel(axes[1])
    return fig, ax
