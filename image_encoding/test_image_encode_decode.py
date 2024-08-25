"""
Test image encode and decode.
"""

import pathlib

from PIL import Image
import numpy as np

from .modules import decoder
from .modules import encoder


ROOT_DIR = "image_encoding"
TEST_IMG = "test.png"
RESULT_IMG = "result.jpg"


def test_image_encode_decode() -> int:
    """
    Main testing sequence of encoding and decoding an image.
    Note that JPEG is a lossy compression algorithm, so data cannot be recovered.
    """
    # Get test image in numpy form
    im = Image.open(pathlib.Path(ROOT_DIR, TEST_IMG))
    raw_data = np.asarray(im)

    # Encode image into JPEG
    jpeg_bytes = encoder.encode(raw_data)

    # Decode JPEG image back to numpy
    img_array = decoder.decode(jpeg_bytes)

    # Reconstruct the image (for human viewing/comparison)
    result = Image.fromarray(img_array, mode="RGB")
    result.save(pathlib.Path(ROOT_DIR, RESULT_IMG), quality=80)

    # Check output shape
    assert img_array.shape == raw_data.shape
