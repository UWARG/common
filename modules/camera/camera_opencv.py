"""
OpenCV implementation of the camera wrapper.
"""

import cv2
import numpy as np

from . import base_camera


class ConfigOpenCV:
    """
    Configuration for the OpenCV camera.
    """

    def __init__(self, device_index: int) -> None:
        """
        index: Index of the device.
        """
        self.device_index = device_index


class CameraOpenCV(base_camera.BaseCameraDevice):
    """
    Class for the OpenCV implementation of the camera.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, width: int, height: int, config: ConfigOpenCV
    ) -> "tuple[True, CameraOpenCV] | tuple[False, None]":
        """
        OpenCV Camera.

        width: Width of the camera.
        height: Height of the camera.
        config: Configuration of for OpenCV camera.

        Return: Success, camera object.
        """
        if width <= 0:
            return False, None

        if height <= 0:
            return False, None

        camera = cv2.VideoCapture(config.device_index)
        if not camera.isOpened():
            return False, None

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        set_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        set_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if set_width != width or set_height != height:
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

    def run(self) -> tuple[True, np.ndarray] | tuple[False, None]:
        """
        Takes a picture with OpenCV camera.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        result, image_data = self.__camera.read()
        if not result:
            return False, None

        return True, image_data
