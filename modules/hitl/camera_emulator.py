"""
Emulates camera input to PI.
"""


class CameraEmulator:
    """
    Setup for camera emulator.
    """

    __create_key = object()

    @classmethod
    def create(cls, images_path: str) -> "tuple[True, CameraEmulator] | tuple[False, None]":
        """
        Setup camera emulator.

        Args:
            images_path: Path to the directory containing images for the camera emulator. Cycles through these images to simulate camera input (every 1 second).

        Returns:
            Success, CameraEmulator instance.
        """

        if not isinstance(images_path, str):
            return False, None

        return True, CameraEmulator(cls.__create_key, images_path)

    def __init__(self, class_private_create_key: object, images_path: str) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CameraEmulator.__create_key, "Use create() method"

        self._images_path = images_path
