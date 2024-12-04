"""
Camera to QR scanner example
"""

import cv2

from modules.camera import camera_factory
from modules.camera import camera_configurations
from modules.qr import qr_scanner


def main() -> int:
    """
    Main function.
    """
    config = camera_configurations.OpenCVCameraConfig()
    result, camera = camera_factory.create_camera(
        camera_factory.CameraOption.OPENCV, 640, 480, config=config
    )
    if not result:
        print("OpenCV camera creation error.")
        return -1

    text = ""
    while True:
        result, image = camera.run()
        if not result:
            continue

        cv2.imshow("Camera", image)

        result, text = qr_scanner.QrScanner.get_qr_text(image)
        if result:
            break

        # Required for image display
        # Delay for 100 ms
        cv2.waitKey(100)

    print(text)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
