"""
Decodes images from JPEG bytes to numpy array.
"""

import io

from PIL import Image
import numpy as np


def decode(data: "io.BytesIO | bytes") -> np.ndarray:
    """
    Decodes a JPEG encoded image and returns it as a numpy array.

    Args:
        data: bytes object containing the JPEG encoded image
    Returns:
        NDArray with in RGB format (Height, Width, 3)
    """
    image = Image.open(data, formats=['JPEG'])
    
    return np.asarray(image)
