"""
Encodes image from original format to JPEG, filtering out A channel if PNG
"""

import io

from PIL import Image

def encode(png_image):
    img = Image.open(png_image)

    if img.mode == 'RGBA' and img.format == 'PNG':
        img = img.convert('RGB')

    buffer = io.BytesIO()
    img.save(buffer, format = 'JPEG', quality=100)
    return buffer.getvalue()
