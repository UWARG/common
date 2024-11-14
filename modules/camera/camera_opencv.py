"""
OpenCV implementation of the camera wrapper
"""

from . import base_camera
import cv2
import numpy as np


class CameraOpenCV(base_camera.BaseCameraDevice):
    """
    Class for the opencv implementation of the camera
    See camera_factory.py for instatiation
    """

    def __init__(self, width: int, height: int) -> None:
        """
        width: width of the camera
        height: height of the camera

        TODO: How do we know the camera would support this resolution?
        """
        self.__camera = cv2.VideoCapture()
        assert self.__camera.isOpened()  # not sure if this is proper
        # ^ shouldn't the init function somehow result in factory returning (False, None)?
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def __del__(self) -> None:
        """
        Destructor to clean up VideoCapture object
        """
        self.__camera.release()  # stop VideoCapture

    def get_camera_data(self) -> tuple[bool, np.ndarray | None]:
        """
        Take picture and return data with opencv
        """
        # capture data from "main" (the stream name)
        # straight up don't know if this is faillible, so hardcoding True for now
        result, image_data = self.__camera.read()

        if not result:
            return False, None

        return result, image_data
