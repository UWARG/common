"""
OpenCV implementation of the camera wrapper.
"""

import cv2
import numpy as np

from . import base_camera


class CameraOpenCV(base_camera.BaseCameraDevice):
    """
    Class for the opencv implementation of the camera.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        width: width of the camera.
        height: height of the camera.

        TODO: How do we know the camera would support this resolution?
        """
        self.__camera = cv2.VideoCapture()
        assert self.__camera.isOpened()  # not sure if this is proper
        # ^ shouldn't the init function somehow result in factory returning (False, None)?
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        self.__camera.release()

    def get_camera_data(self) -> tuple[bool, np.ndarray | None]:
        """
        Takes a picture with opencv camera.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        result, image_data = self.__camera.read()
        if not result:
            return False, None

        return True, image_data
