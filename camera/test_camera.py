"""
Test camera physically.
"""

import cv2

from camera.modules.camera_device import CameraDevice


IMAGE_LOG_PREFIX = "log_image"


if __name__ == "__main__":
    device = CameraDevice(0, 100, IMAGE_LOG_PREFIX)

    while True:
        result, image = device.get_image()
        if not result:
            print("ERROR")
            continue

        print(image.shape)

        cv2.imshow("Camera", image)

        # Delay for 1 ms
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Done!")
