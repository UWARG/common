"""
Test camera physically.
"""

import pathlib

import cv2

from camera.modules.camera_device import CameraDevice


IMAGE_LOG_PREFIX = pathlib.Path("logs", "log_image")


def main() -> int:
    """
    Main function.
    """
    device = CameraDevice(0, 100, IMAGE_LOG_PREFIX)

    while True:
        result, image = device.get_image()
        if not result:
            print("ERROR")
            continue

        print(image.shape)

        cv2.imshow("Camera", image)

        # Delay for 1 ms
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
