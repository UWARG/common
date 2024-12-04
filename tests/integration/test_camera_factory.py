from modules.camera.camera_factory import PiCameraConfig, OpenCVCameraConfig


def test_picamera_config() -> None:
    config = PiCameraConfig(exposure_time=250, contrast=1.0)
    assert config.exposure_time == 250
    assert config.contrast == 1.0
    assert config.analogue_gain == 64.0
    assert config.lens_position is None


def test_opencv_camera_config() -> None:
    config = OpenCVCameraConfig()
    assert config is not None