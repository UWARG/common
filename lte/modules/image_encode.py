"""
Decodes a numpy array and returns a JPEG encoded image, filtering out A channel if PNG
"""

import io

from PIL import Image
import numpy as np

def encode(image_array: np.ndarray) -> "io.BytesIO | bytes":
    img = Image.fromarray(image_array)

    buffer = io.BytesIO()
    img.save(buffer, format = 'JPEG', quality=100)
    return buffer.getvalue()
