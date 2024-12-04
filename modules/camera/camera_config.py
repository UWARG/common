"""
Camera configuration
"""


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
        controls: dict[str, int | float] = {}
        if self.exposure_time is not None:
            controls["ExposureTime"] = self.exposure_time
        if self.analogue_gain is not None:
            controls["AnalogueGain"] = self.analogue_gain
        if self.contrast is not None:
            controls["Contrast"] = self.contrast
        if self.lens_position is not None:
            controls["LensPosition"] = self.lens_position
            controls["AfMode"] = controls.AfModeEnum.Manual
        else:
            controls["LensPosition"] = 0.0
            controls["AfMode"] = controls.AfModeEnum.Auto

        return controls


class OpenCVCameraConfig:
    """
    Placeholder
    """

    pass
