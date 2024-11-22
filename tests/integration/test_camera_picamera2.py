"""
Test picamera2 camera physically.
"""

import pathlib

import cv2

from modules.camera import camera_factory


IMAGE_LOG_PREFIX = pathlib.Path("logs", "test_log_image")


def main() -> int:
    """
    Main function.
    """
    result, device = camera_factory.create_camera(camera_factory.CameraOption.PICAM2, 640, 480)

    if not result:
        print("Picamera2 camera creation error.")
        return -1

    IMAGE_LOG_PREFIX.parent.mkdir(parents=True, exist_ok=True)

    while True:
        result, image = device.run()
        if not result:
            print("ERROR")
            continue

        print(image.shape)

        cv2.imshow("Picamera2 camera", image)

        # Delay for 1 ms
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
