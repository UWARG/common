"""
Emulates position and attitude to Pixhawk.
"""

from modules.mavlink.flight_controller import FlightController


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, drone: FlightController
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Returns:
            Success, PositionEmulator instance.
        """

        if not isinstance(drone, FlightController):
            return False, None

        return True, PositionEmulator(cls.__create_key, drone)

    def __init__(self, class_private_create_key: object, drone: FlightController) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self._drone = drone
