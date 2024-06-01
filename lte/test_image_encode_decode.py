"""
Test image encode and decode.
TODO: finish image encode and then write this test
"""

from lte.modules import image_decode


def main() -> int:
    # TODO: Get test images and Encode
    raw_data = 0

    # Decode
    img_array = image_decode.decode(raw_data)

    # Do checks
    # eg. check output shape
    return 0


if __name__ == "__main__":
    result_main = main()

    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
