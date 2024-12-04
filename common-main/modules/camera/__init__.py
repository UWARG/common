"""
__init__ for camera
"""

from .camera_factory import (
    create_camera,
    CameraOption,
)

from .camera_config import PiCameraConfig, OpenCVCameraConfig
from .camera_opencv import CameraOpenCV
from .camera_picamera2 import CameraPiCamera2

__all__ = [
    "create_camera",
    "CameraOption",
    "PiCameraConfig",
    "OpenCVCameraConfig",
    "CameraOpenCV",
    "CameraPiCamera2",
]
