"""
Emulates position and attitude to Pixhawk.
"""

from modules.mavlink.flight_controller import FlightController


class PositionEmulator:
    """
    Setup for position emulator.
    """

    def create(
        self, drone: FlightController
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Returns:
            Success, PositionEmulator instance.
        """
        return True, self
