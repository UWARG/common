"""
Camera device using OpenCV
"""

import cv2
import numpy as np


class CameraDevice:
    """
    Wrapper for camera
    """

    def __init__(self, name):
        """
        name: Device name or index (e.g. /dev/video0 )
        """
        self.camera = cv2.VideoCapture(name)

    def __del__(self):
        self.camera.release()

    def get_image(self) -> "tuple[bool, np.ndarray]":
        """
        Take a picture with the camera
        """
        return self.camera.read()
