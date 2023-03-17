"""
Camera device using OpenCV
"""

import cv2
import numpy as np


class CameraDevice:
    """
    Wrapper for camera
    """

    def __init__(self, name: "int | str", save_nth_image: int = 0, save_name: str = ""):
        """
        name: Device name or index (e.g. /dev/video0 )
        (optional) save_nth_image: For debugging, saves every nth image. A value of 0 indicates no images should be saved
        (optional) save_name: For debugging, file name for saved images
        """
        self.camera = cv2.VideoCapture(name)

        self.divisor = save_nth_image
        self.counter = 0
        self.filename_prefix = save_name

    def __del__(self):
        self.camera.release()

    def get_image(self) -> "tuple[bool, np.ndarray]":
        """
        Take a picture with the camera
        """
        result, image = self.camera.read()
        if not result:
            return result, image

        if self.divisor != 0:
            if self.counter % self.divisor == 0:
                filename = self.filename_prefix + str(self.counter) + ".png"
                cv2.imwrite(filename, image)

            self.counter += 1

        return result, image
