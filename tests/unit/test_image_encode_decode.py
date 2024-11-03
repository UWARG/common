"""
Test image encode and decode.
"""

import pathlib

from PIL import Image
import numpy as np

from modules.image_encoding import decoder
from modules.image_encoding import encoder


PARENT_DIRECTORY = pathlib.Path("tests", "unit", "image_encoding_images")
TEST_IMAGE_NAME = "test.png"

RESULT_DIRECTORY = pathlib.Path("logs")
RESULT_IMAGE_NAME = "test_result.jpg"


def test_image_encode_decode() -> None:
    """
    Main testing sequence of encoding and decoding an image.
    Note that JPEG is a lossy compression algorithm, so data cannot be recovered.
    """
    RESULT_DIRECTORY.mkdir(exist_ok=True)

    # Get test image in numpy form
    im = Image.open(pathlib.Path(PARENT_DIRECTORY, TEST_IMAGE_NAME))
    raw_data = np.asarray(im)

    # Encode image into JPEG
    jpeg_bytes = encoder.encode(raw_data)

    # Decode JPEG image back to numpy
    img_array = decoder.decode(jpeg_bytes)

    # Reconstruct the image (for human viewing/comparison)
    result = Image.fromarray(img_array, mode="RGB")
    result.save(pathlib.Path(RESULT_DIRECTORY, RESULT_IMAGE_NAME), quality=80)

    # Check output shape
    assert img_array.shape == raw_data.shape
