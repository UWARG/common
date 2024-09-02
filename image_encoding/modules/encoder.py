"""
Decodes a numpy array and returns a JPEG encoded image
"""

import io

from PIL import Image
import numpy as np


QUALITY = 80  # Quality of JPEG encoding to use (0-100)


def encode(image_array: np.ndarray) -> "bytes":
    """
    Encodes an image in numpy array form into bytes of a JPEG.

    Args:
        image_array: numpy array of an RGB image with shape (Height, Width, 3)
    Returns:
        bytes which form the JPEG encoded image
    """
    img = Image.fromarray(image_array, mode="RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=QUALITY)

    return buffer.getvalue()
