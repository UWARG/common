"""
Picamera2 implementation of the camera wrapper.
"""

import numpy as np

# Picamera2 library only exists on Raspberry Pi
try:
    import libcamera
    import picamera2
except ImportError:
    picamera2 = None

from . import base_camera


class ConfigPiCamera2:
    """
    Configuration for the PiCamera.
    """

    def __init__(
        self,
        timeout: float = 1.0,
        exposure_time: int = 250,
        analogue_gain: float = 64.0,
        contrast: float = 1.0,
        maybe_lens_position: float | None = None,
    ) -> None:
        """
        timeout: Getting image timeout in seconds.

        exposure_time: Microseconds.
        analogue_gain: 0.0 to 64.0 . ISO = Analogue gain * Digital gain * 100 .
        contrast: 0.0 to 32.0 . 0.0 is no contrast, 1.0 is normal contrast, higher is more contrast.
        lens_position: Position of the lens is dioptres (reciprocal of metres: 1/m ) (0 means infinite distance).
        """
        self.timeout = timeout

        self.exposure_time = exposure_time
        self.analogue_gain = analogue_gain
        self.contrast = contrast
        self.maybe_lens_position = maybe_lens_position

    def to_dict(self) -> dict[str, int | float]:
        """
        Dictionary containing camera controls.
        """
        camera_controls = {
            "ExposureTime": self.exposure_time,
            "AnalogueGain": self.analogue_gain,
            "Contrast": self.contrast,
        }

        if self.maybe_lens_position is not None:
            camera_controls["LensPosition"] = self.maybe_lens_position
            camera_controls["AfMode"] = libcamera.controls.AfModeEnum.Manual
        else:
            camera_controls["LensPosition"] = 0.0
            camera_controls["AfMode"] = libcamera.controls.AfModeEnum.Auto

        return camera_controls


if picamera2 is None:

    class CameraPiCamera2(base_camera.BaseCameraDevice):
        """
        Class for the Picamera2 import failure.
        """

        __create_key = object()

        @classmethod
        def create(cls, width: int, height: int, config: ConfigPiCamera2) -> "tuple[False, None]":
            return False, None

        def __init__(self) -> None:
            pass

else:

    class CameraPiCamera2(base_camera.BaseCameraDevice):
        """
        Class for the Picamera2 implementation of the camera.
        """

        __create_key = object()

        @classmethod
        def create(
            cls, width: int, height: int, config: ConfigPiCamera2
        ) -> "tuple[True, CameraPiCamera2] | tuple[False, None]":
            """
            Picamera2 Camera.

            width: Width of the camera.
            height: Height of the camera.
            config: Configuration for PiCamera2 camera.

            Return: Success, camera object.
            """

            if width <= 0:
                return False, None

            if height <= 0:
                return False, None

            try:
                camera = picamera2.Picamera2()

                camera_config = camera.create_preview_configuration(
                    {"size": (width, height), "format": "RGB888"}
                )
                camera.configure(camera_config)
                camera.start()
                controls = config.to_dict()
                camera.set_controls(controls)

                return True, CameraPiCamera2(cls.__create_key, camera, config)
            except RuntimeError:
                return False, None

        def __init__(
            self,
            class_private_create_key: object,
            camera: picamera2.Picamera2,  # type: ignore
            config: ConfigPiCamera2,
        ) -> None:
            """
            Private constructor, use create() method.
            """
            assert class_private_create_key is CameraPiCamera2.__create_key, "Use create() method."

            self.__camera = camera
            self.__config = config

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
                image_data = self.__camera.capture_array(wait=self.__config.timeout)
            except TimeoutError:
                return False, None

            return True, image_data
