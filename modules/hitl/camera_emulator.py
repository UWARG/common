"""
Emulates camera input to PI.
"""


class CameraEmulator:
    """
    Setup for camera emulator.
    """

    def create(self) -> "tuple[True, CameraEmulator] | tuple[False, None]":
        """
        Setup camera emulator.

        Returns:
            Success, CameraEmulator instance.
        """
        return True, self
