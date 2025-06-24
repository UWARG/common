"""
Setup for HITL modules.
"""

from modules.hitl.position_emulator import PositionEmulator
from modules.hitl.camera_emulator import CameraEmulator
from ..mavlink import dronekit


class HITL:
    """
    Hardware In The Loop (HITL) setup for emulating drone hardware.
    Provides a way to emulate the drone's position and camera input
    for testing purposes without needing actual hardware.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        drone: dronekit.Vehicle,
        hitl_enabled: bool,
        position_module: bool,
        camera_module: bool,
        images_path: str | None = None,
    ) -> "tuple[True, HITL] | tuple[False, None]":
        """
        Factory method to create a HITL instance.

        Args:
            drone: The dronekit instance to use for sending MAVLink messages.
            hitl_enabled: Boolean indicating if HITL is enabled.
            position_module: Boolean indicating if the position module is enabled.
            camera_module: Boolean indicating if the camera module is enabled.
            images_path: Optional path to the images directory for the camera emulator.

        Returns:
            Success, HITL instance | None.
        """
        if not isinstance(drone, dronekit.Vehicle):
            return False, None

        if not hitl_enabled:
            return True, HITL(cls.__create_key, drone, None, None)

        if position_module:
            result, position_emulator = PositionEmulator.create(drone)
            position_emulator.inject_position()  # Inject initial position
            if not result:
                return False, None

        if camera_module:
            result, camera_emulator = CameraEmulator.create(images_path)
            if not result:
                return False, None

        hitl = HITL(
            cls.__create_key,
            position_emulator if position_emulator else None,
            camera_emulator if camera_module else None,
        )

        return True, hitl

    def __init__(
        self,
        class_private_create_key: object,
        drone: dronekit.Vehicle,
        position_emulator: "PositionEmulator | None" = None,
        camera_emulator: "CameraEmulator | None" = None,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is HITL.__create_key, "Use create() method"

        self.drone = drone
        self.position_emulator = position_emulator
        self.camera_emulator = camera_emulator
