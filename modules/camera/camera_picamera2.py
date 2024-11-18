"""
Picamera2 implementation of the camera wrapper.
"""

try:
    import picamera2
except ImportError:
    pass
import numpy as np

from . import base_camera


class CameraPiCamera2(base_camera.BaseCameraDevice):
    """
    Class for the opencv implementation of the camera.
    TODO: ADD LINK TO MANUAL HERE
    """

    def __init__(self, width: int, height: int) -> None:
        """
        width: width of the camera.
        height: height of the camera.
        """
        self.__camera = picamera2.Picamera2()
        # Unintuitively, "RGB888" is layout BGR
        # See section 4.2.2.2 of the manual
        config = self.__camera.create_preview_configuation(
            {"size": (width, height), "format": "BGR888"}
        )

        self.__camera.configure(config)
        # TODO: review camera arguments
        self.__camera.start(show_previous=False)

    def __del__(self) -> None:
        """
        Destructor to clean up Picamera2 object.
        """
        self.__camera.stop()

    def get_camera_data(self) -> tuple[bool, np.ndarray | None]:
        """
        Takes a picture with picamera2 camera.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        result, image_data = self.__camera.capture_array()
        # not sure what picamera2 does to fail the capture_array()
        # TODO: revisit and change to catch failure
        if not result:
            return False, None

        return True, image_data
