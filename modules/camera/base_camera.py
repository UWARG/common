"""
Base class for camera device.
"""

import abc

import numpy as np


class BaseCameraDevice(abc.ABC):
    """
    Abstract class for camera device implementations.
    """

    @classmethod
    @abc.abstractmethod
    def create(
        cls, width: int, height: int, config: object
    ) -> "tuple[True, BaseCameraDevice] | tuple[False, None]":
        """
        Abstract create method.

        width: Width of the camera.
        height: Height of the camera.

        Return: Success, camera object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __init__(self, class_private_create_key: object, camera: object) -> None:
        """
        Abstract private constructor.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def run(self) -> tuple[True, np.ndarray] | tuple[False, None]:
        """
        Takes a picture with camera device.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        raise NotImplementedError
