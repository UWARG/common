"""
Test for the hitl camera emulator

INSTRUCTIONS:
- Using a windows environemnt with OBS installed,
run this script (this will create a virtual camera and start streaming images to it)

- Run test_camera_read (will open the virtual camera using opencv and display the images)
Note: may need to mess around with camera index
(usually will be # of cameras connected to computer + 1)
"""

import time
import os
from modules.hitl.camera_emulator import CameraEmulator


def main() -> None:
    """
    Runs camera emulator
    """
    images_folder_path = os.path.join("tests", "integration", "camera_emulator", "images")
    has_cam, cam_emulator = CameraEmulator.create(images_folder_path)
    if has_cam:
        print("CAMERA EMULATOR RUNNING")
        start = time.perf_counter()
        while True:
            cam_emulator.send_frame()
            cam_emulator.sleep_until_next_frame()
            if time.perf_counter() - start > 1:
                cam_emulator.next_image()
                cam_emulator.update_current_image()
                start = time.perf_counter()


if __name__ == "__main__":
    main()
    print("CAMERA EMULATOR STOPPED")
