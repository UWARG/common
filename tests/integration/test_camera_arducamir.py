"""
Test ArducamIR camera physically and verifies configuration
"""

import time
import cv2

from modules.camera import camera_factory
from modules.camera import camera_arducamir


def main() -> int:
    """
    Main function
    """

    result, device = camera_factory.create_camera(
        camera_factory.CameraOption.ARDUCAMIR,
        100,
        200,
        None,
    )
    if not result:
        print("ArducamIR camera creation error.")
        return -1

    while True:
        result, image = device.run()
        if not result:
            print("ERROR, image not captured.\n")
            continue

        if image.seq % 50 == 0:  # Avoiding too many prints, 50 is an arbitrary number
            print(f"Timestamp: [{0:s}]", time.ctime(float(image.timestamp / 10**3)))
            print("Bit Depth: {0:2d}", image.format.bit_depth)
            print("Format Code: {0:2d}", image.format.format_code)
            print("Height: {0:3d}", image.format.height)
            print("Width: {0:3d}\n", image.format.width)

            # Assertions for Arducam cfg config values
            assert image.format.bit_depth == 12
            assert image.format.format_code == 2307
            assert image.format.width == 640
            assert image.format.height == 480

        color_frame = device.demosaic(image, camera_arducamir.ArducamOutput.IR)

        if image.data is not None:
            cv2.imshow("ArducamIR Test", color_frame)
        cv2.setWindowTitle("ArducamIR Test", "ArducamIR Test " + str(image.seq))

        # 1ms delay between next picture
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
