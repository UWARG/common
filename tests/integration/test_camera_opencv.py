"""
Test OpenCV camera physically.
"""

import pathlib

import cv2

from modules.camera import camera_factory
from modules.camera import camera_opencv


# TODO: Add camera logging
IMAGE_LOG_PREFIX = pathlib.Path("logs", "test_log_image")


def main() -> int:
    """
    Main function.
    """
    config = camera_opencv.ConfigOpenCV(0)
    assert config is not None

    result, device = camera_factory.create_camera(
        camera_factory.CameraOption.OPENCV, 640, 480, config
    )
    if not result:
        print("OpenCV camera creation error.")
        return -1

    IMAGE_LOG_PREFIX.parent.mkdir(parents=True, exist_ok=True)

    while True:
        result, image = device.run()
        if not result:
            print("ERROR")
            continue

        print(image.shape)

        cv2.imshow("OpenCV camera", image)

        # Delay for 1 ms
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
