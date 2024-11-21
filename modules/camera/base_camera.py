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
        cls, width: int, height: int
    ) -> "tuple[True, BaseCameraDevice] | tuple[False, None]":
        pass

    @abc.abstractmethod
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        return NotImplementedError

    @abc.abstractmethod
    def run(self) -> tuple[True, np.ndarray] | tuple[False, None]:
        """
        Takes a picture with camera device.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        return NotImplementedError
