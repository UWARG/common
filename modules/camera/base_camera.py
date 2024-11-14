"""
Base class for camera device
"""

from abc import ABC, abstractmethod
import numpy as np


class BaseCameraDevice(ABC):
    """
    Abstract class for camera device implementations.
    TODO: could leverage the abc library's tags more (required properties/methods/etc.)
    """

    @abstractmethod
    def __del__(self) -> None:
        """
        Destructor, make sure to stop the camera object e.g. for opencv, VideoCapture.stop()
        """
        return NotImplementedError

    @abstractmethod
    def get_camera_data(self) -> tuple[bool, np.ndarray | None]:
        """
        Takes a picture with the camera and returns an numpy ndarray
        Should not save the data
        """
        return NotImplementedError
