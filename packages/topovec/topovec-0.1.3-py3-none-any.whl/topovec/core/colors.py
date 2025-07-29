import numpy as np


# Copy of Matplotlib implementation.
def hsv_to_rgb(hsv):
    """
    Convert hsv values to rgb.

    Parameters
    ----------
    hsv : (..., 3) array-like
       All values assumed to be in range [0, 1]

    Returns
    -------
    rgb : (..., 3) ndarray
       Colors converted to RGB values in range [0, 1]
    """
    hsv = np.asarray(hsv)

    # check length of the last dimension, should be _some_ sort of rgb
    if hsv.shape[-1] != 3:
        raise ValueError(
            f"Last dimension of input array must be 3; shape {hsv.shape} was found."
        )

    in_shape = hsv.shape
    hsv = np.array(
        hsv,
        copy=False,
        dtype=np.promote_types(hsv.dtype, np.float32),  # Don't work on ints.
        ndmin=2,  # In case input was 1D.
    )

    h = hsv[..., 0]
    s = hsv[..., 1]
    v = hsv[..., 2]

    r = np.empty_like(h)
    g = np.empty_like(h)
    b = np.empty_like(h)

    i = (h * 6.0).astype(int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    idx = i % 6 == 0
    r[idx] = v[idx]
    g[idx] = t[idx]
    b[idx] = p[idx]

    idx = i == 1
    r[idx] = q[idx]
    g[idx] = v[idx]
    b[idx] = p[idx]

    idx = i == 2
    r[idx] = p[idx]
    g[idx] = v[idx]
    b[idx] = t[idx]

    idx = i == 3
    r[idx] = p[idx]
    g[idx] = q[idx]
    b[idx] = v[idx]

    idx = i == 4
    r[idx] = t[idx]
    g[idx] = p[idx]
    b[idx] = v[idx]

    idx = i == 5
    r[idx] = v[idx]
    g[idx] = p[idx]
    b[idx] = q[idx]

    idx = s == 0
    r[idx] = v[idx]
    g[idx] = v[idx]
    b[idx] = v[idx]

    rgb = np.stack([r, g, b], axis=-1)

    return rgb.reshape(in_shape)


###


def vector_to_rgb(S, axis=(0, 0, 1), invert=False, shift=0.81):
    """
    Convert 3d vectors of unit length to corresponding colors in RGB.
    """
    C = np.empty_like(S)
    axis = np.array(axis, dtype=np.float32)
    axis_norm = np.linalg.norm(axis)
    axis /= axis_norm
    C[..., 0] = (np.arctan2(S[..., 1], S[..., 0]) / np.pi + 1) / 2 + shift
    C[..., 0] -= np.floor(C[..., 0])
    s = np.sum(S * axis, axis=-1)
    C[..., 1 if invert else 2] = np.maximum(0, np.minimum(1 + s, 1))
    C[..., 2 if invert else 1] = np.maximum(0, np.minimum(1 - s, 1))
    return hsv_to_rgb(C)
