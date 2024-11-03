"""
Decodes images from JPEG bytes to numpy array.
"""

import io

import numpy as np
from PIL import Image


def decode(data: "bytes") -> np.ndarray:
    """
    Decodes a JPEG encoded image and returns it as a numpy array.

    Args:
        data: bytes object containing the JPEG encoded image
    Returns:
        NDArray with in RGB format. Shape is (Height, Width, 3)
    """
    image = Image.open(io.BytesIO(data), formats=["JPEG"])

    return np.asarray(image)
