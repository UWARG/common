"""
Decodes images from JPEG bytes to numpy array.
"""

from PIL import Image
import numpy as np


def decode(data: "io.BytesIO | bytes") -> np.ndarray:
    """
    Decodes a JPEG encoded image and returns it as a numpy array.

    Args:
        data: bytes object containing the JPEG encoded image
        TODO: When encoding JPEG, make sure the input image only has 3 channels,
              if original picture was a PNG (filter out A channel)
    Returns:
        NDArray with in RGB format. Shape is (Height, Width, 3)
    """
    image = Image.open(data, formats=["JPEG"])

    return np.asarray(image)
