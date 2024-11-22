"""
Picamera2 implementation of the camera wrapper.
"""

import numpy as np

from . import base_camera

# The picamera2 module might not exist on the machine
try:
    import picamera2

except ImportError:
    pass


class CameraPiCamera2(base_camera.BaseCameraDevice):
    """
    Class for the picamera2 implementation of the camera.
    """

    __create_key = object()

    @classmethod
    def create(cls, width: int, height: int) -> "tuple[True, CameraPiCamera2] | tuple[False, None]":
        """
        Picamera2 Camera.

        width: width of the camera.
        height: height of the camera.
        """
        try:
            camera = picamera2.Picamera2()
            # Unintuitively, "RGB888" is layout BGR
            # See section 4.2.2.2 of the manual
            config = camera.create_still_configuration(
                {"size": (width, height), "format": "BGR888"}
            )
            camera.configure(config)
            camera.start()
            return True, CameraPiCamera2(cls.__create_key, camera)
        except RuntimeError:
            return False, None

    def __init__(self, class_private_create_key: object, camera: "picamera2.Picamera2") -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CameraPiCamera2.__create_key, "Use create() method."

        self.__camera = camera

    def __del__(self) -> None:
        """
        Destructor to clean up Picamera2 object.
        """
        self.__camera.close()

    def run(self) -> tuple[bool, np.ndarray | None]:
        """
        Takes a picture with picamera2 camera.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        result, image_data = self.__camera.capture_array()
        if not result:
            return False, None

        return True, image_data
