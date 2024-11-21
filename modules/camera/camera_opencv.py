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

    __create_key = object()

    def create(cls, width: int, height: int) -> "tuple[True, CameraOpenCV] | tuple[False, None]":
        """
        OpenCV Camera.

        width: width of the camera.
        height: height of the camera.
        """
        camera = cv2.VideoCapture()
        if not camera.isOpened():
            return False, None

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not (
            camera.get(cv2.CAP_PROP_FRAME_WIDTH) == width
            and camera.get(cv2.CAP_PROP_FRAME_HEIGHT, height) == height
        ):
            return False, None

        return True, CameraOpenCV(cls.__create_key, camera)

    def __init__(self, class_private_create_key: object, camera: cv2.VideoCapture) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CameraOpenCV.__create_key, "Use create() method."

        self.__camera = camera

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
