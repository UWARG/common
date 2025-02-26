"""
Position, orientation, and flight mode of drone.
"""

import enum

from .. import orientation
from .. import position_global


class FlightMode(enum.Enum):
    """
    Possible drone flight modes.
    """

    STOPPED = 0
    MOVING = 1
    MANUAL = 2


class DroneOdometryGlobal:
    """
    Wrapper for position, orientation, and flight mode.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        drone_position: position_global.PositionGlobal,
        drone_orientation: orientation.Orientation,
        flight_mode: FlightMode,
    ) -> "tuple[bool, DroneOdometryGlobal] | tuple[False, None]":
        """
        Position and orientation in one class.
        """
        if drone_position is None:
            return False, None

        if drone_orientation is None:
            return False, None

        if flight_mode is None:
            return False, None

        return True, DroneOdometryGlobal(
            cls.__create_key, drone_position, drone_orientation, flight_mode
        )

    def __init__(
        self,
        class_private_create_key: object,
        drone_position: position_global.PositionGlobal,
        drone_orientation: orientation.Orientation,
        flight_mode: FlightMode,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOdometryGlobal.__create_key, "Use create() method."

        self.position = drone_position
        self.orientation = drone_orientation
        self.flight_mode = flight_mode

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: Position: {self.position}, orientation: {self.orientation}, flight mode: {self.flight_mode.name}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
