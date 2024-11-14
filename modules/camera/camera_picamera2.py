"""
Picamera2 implementation of the camera wrapper
"""

try:
    import picamera2
except ImportError:
    pass
import numpy as np
from . import base_camera


class CameraPiCamera2(base_camera.BaseCameraDevice):
    """
    Class for the opencv implementation of the camera
    See camera_factory.py for instatiation
    """

    def __init__(self, width: int, height: int) -> None:
        """
        width: width of the camera
        height: height of the camera
        """
        self.__camera = picamera2.Picamera2()
        # maybe use create_still_configuration(), difference is speed
        # if format is bad, use 'RGB888' for [B, G, R] layout. 'BGR888' uses [R, G, B] layout
        # see section 4.2.2.2 bottom warning for explanation
        config = self.__camera.create_preview_configuation(
            {"size": (width, height), "format": "BGR888"}
        )

        self.__camera.configure(config)
        # TODO: review camera arguments
        self.__camera.start(show_previous=False)

    def __del__(self) -> None:
        """
        Destructor to clean up Picamera2 object
        """
        self.__camera.stop()  # stop Picamera2

    def get_camera_data(self) -> tuple[bool, np.ndarray | None]:
        """
        Take picture with picamera2 and return data
        """
        result, image_data = self.__camera.capture_array()
        # not sure what picamera2 does to fail the capture_array()
        # TODO: revisit and change to catch failure
        if not result:
            return False, None

        return result, image_data
