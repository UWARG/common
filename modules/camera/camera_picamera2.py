"""
Picamera2 implementation of the camera wrapper.
"""

import numpy as np

from . import camera_config

# Picamera2 library only exists on Raspberry Pi
try:
    import picamera2
except ImportError:
    pass

from . import base_camera

# TODO: pass in as constructor parameter
CAMERA_TIMEOUT = 1


class CameraPiCamera2(base_camera.BaseCameraDevice):
    """
    Class for the Picamera2 implementation of the camera.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, width: int, height: int, config: camera_config.PiCameraConfig = None
    ) -> "tuple[True, CameraPiCamera2] | tuple[False, None]":
        """
        Picamera2 Camera.

        width: Width of the camera.
        height: Height of the camera.
        config (PiCameraConfig): Configuration object
        Return: Success, camera object.
        """
        try:
            camera = picamera2.Picamera2()

            camera_configuration = camera.create_preview_configuration(
                {"size": (width, height), "format": "RGB888"}
            )
            camera.configure(camera_configuration)
            camera.start()
            if config:
                controls = config.to_dict()
                camera.set_controls(controls)
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
        Destructor. Release hardware resources.
        """
        self.__camera.close()

    def run(self) -> tuple[True, np.ndarray] | tuple[False, None]:
        """
        Takes a picture with Picamera2 camera.

        Return: Success, image with shape (height, width, channels in BGR).
        """
        try:
            # CAMERA_TIMEOUT seconds before raising TimeoutError
            image_data = self.__camera.capture_array(wait=CAMERA_TIMEOUT)
        except TimeoutError:
            return False, None

        return True, image_data
