"""
Test camera physically
"""

from modules.camera_device import CameraDevice


if __name__ == "__main__":
    device = CameraDevice(0, 100, "test_camera")

    while True:
        result, frame = device.get_image()
        if not result:
            continue

        print(frame.shape)
