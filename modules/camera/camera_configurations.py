"""
Camera configuration
"""

try:
    from libcamera import controls  # This is a pre-installed library on the Rpi5
except ImportError:
    pass


class PiCameraConfig:
    """
    Configuration for the PiCamera.
    This class allows specifying parameters such as exposure time, gain, and contrast.
    """

    def __init__(
        self,
        exposure_time: int = 250,
        analogue_gain: float = 64.0,
        contrast: float = 1.0,
        lens_position: float = None,
    ) -> None:
        """
        Args:
            exposure_time (int)
            analogue_gain (float)
            contrast (float)
            lens_position (float)
        """
        self.exposure_time = exposure_time
        self.analogue_gain = analogue_gain
        self.contrast = contrast
        self.lens_position = lens_position

    def to_dict(self) -> dict[str, int | float | None]:
        """
        Dictionary containing camera controls.
        """
        camera_controls: dict[str, int | float] = {}
        if self.exposure_time is not None:
            camera_controls["ExposureTime"] = self.exposure_time
        if self.analogue_gain is not None:
            camera_controls["AnalogueGain"] = self.analogue_gain
        if self.contrast is not None:
            camera_controls["Contrast"] = self.contrast
        if self.lens_position is not None:
            camera_controls["LensPosition"] = self.lens_position
            camera_controls["AfMode"] = controls.AfModeEnum.Manual
        else:
            camera_controls["LensPosition"] = 0.0
            camera_controls["AfMode"] = controls.AfModeEnum.Auto

        return camera_controls


class OpenCVCameraConfig:
    """
    Placeholder
    """

    pass  # pylint: disable=unnecessary-pass
