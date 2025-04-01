"""
Factory pattern for constructing camera device class at runtime.
"""

import enum

from . import base_camera
from . import camera_opencv
from . import camera_picamera2
from . import camera_arducamir


class CameraOption(enum.Enum):
    """
    enum for type of camera object to create.
    """

    OPENCV = 0
    PICAM2 = 1
    ARDUCAMIR = 2


def create_camera(
    camera_option: CameraOption,
    width: int,
    height: int,
    config: camera_opencv.ConfigOpenCV | camera_picamera2.ConfigPiCamera2 | None,
) -> tuple[True, base_camera.BaseCameraDevice] | tuple[False, None]:
    """
    Create a camera object based off of given parameters.

    Return: Success, camera device object.
    """
    match camera_option:
        case CameraOption.OPENCV:
            return camera_opencv.CameraOpenCV.create(width, height, config)
        case CameraOption.PICAM2:
            return camera_picamera2.CameraPiCamera2.create(width, height, config)
        case CameraOption.ARDUCAMIR:
            return camera_arducamir.CameraArducamIR.create(width, height, config)

    return False, None
