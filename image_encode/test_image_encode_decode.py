"""
Test image encode and decode.
"""

import pathlib

from PIL import Image
import numpy as np

from image_encode.modules import decoder
from image_encode.modules import encoder


def main() -> int:
    """
    Main testing sequence of encoding and decoding an image.
    """
    # Get test image in numpy form
    im = Image.open(pathlib.Path("lte", "test.png"))
    raw_data = np.asarray(im)

    # Encode image into JPEG
    jpeg_bytes = encoder.encode(raw_data)

    # Decode JPEG image back to numpy
    img_array = decoder.decode(jpeg_bytes)

    # Reconstruct the image (for human viewing/comparison)
    result = Image.fromarray(img_array, mode="RGB")
    result.save(pathlib.Path("lte", "result.jpg"), quality=80)

    # Check output shape
    assert img_array.shape == raw_data.shape

    # Note: the following fail since JPEG encoding is lossy
    # assert (raw_data == img_array).all()

    return 0


if __name__ == "__main__":
    result_main = main()

    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
