"""
Factory pattern for constructing camera device class at runtime
"""

import enum

from . import base_camera, camera_opencv, camera_picamera2


class CameraOption(enum.Enum):
    """
    enum for type of camera object to create
    as of 11/14/2024 opencv and picamera2 implementation
    """

    CAM_OPENCV = 0
    CAM_PICAM2 = 1


def create_camera(
    camera_option: CameraOption, width: int = 1920, height: int = 1080
) -> tuple[bool | base_camera.BaseCameraDevice]:
    """
    Create a camera object based off of given parameters
    returns [False, None] for invalid camera_option
    TODO: object creation is not faillable, will return true even if constructor fails
    e.g. no camera attached?
    """
    match camera_option:
        case CameraOption.CAM_OPENCV:
            return True, camera_opencv.CameraOpenCV(width, height)
        case CameraOption.CAM_PICAM2:
            return True, camera_picamera2.CameraPiCamera2(width, height)
    return False, None
