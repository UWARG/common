"""
Position and orientation of drone.
"""

import enum
import math

from .. import position_global


class DroneOrientation:
    """
    Yaw, pitch, roll following NED system (x forward, y right, z down).
    Specifically, intrinsic (Tait-Bryan) rotations in the zyx/3-2-1 order.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, yaw: "float | None", pitch: "float | None", roll: "float | None"
    ) -> "tuple[bool, DroneOrientation] | tuple[False, None]":
        """
        yaw, pitch, roll in radians.
        """
        if yaw is None:
            return False, None

        if pitch is None:
            return False, None

        if roll is None:
            return False, None

        if yaw < -math.pi or yaw > math.pi:
            return False, None

        if pitch < -math.pi or pitch > math.pi:
            return False, None

        if roll < -math.pi or roll > math.pi:
            return False, None

        return True, DroneOrientation(cls.__create_key, yaw, pitch, roll)

    def __init__(
        self, class_private_create_key: object, yaw: float, pitch: float, roll: float
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOrientation.__create_key, "Use create() method."

        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__} YPR radians: {self.yaw}, {self.pitch}, {self.roll}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)


class FlightMode(enum.Enum):
    """
    Possible drone flight modes.
    """

    STOPPED = 0
    MOVING = 1
    MANUAL = 2


class DroneOdometry:
    """
    Wrapper for DronePosition, DroneOrientation, and FlightMode.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        position: position_global.PositionGlobal,
        orientation: DroneOrientation,
        flight_mode: FlightMode,
    ) -> "tuple[bool, DroneOdometry] | tuple[False, None]":
        """
        Position and orientation in one class.
        """
        if position is None:
            return False, None

        if orientation is None:
            return False, None

        if flight_mode is None:
            return False, None

        return True, DroneOdometry(cls.__create_key, position, orientation, flight_mode)

    def __init__(
        self,
        class_private_create_key: object,
        position: position_global.PositionGlobal,
        orientation: DroneOrientation,
        flight_mode: FlightMode,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOdometry.__create_key, "Use create() method."

        self.position = position
        self.orientation = orientation
        self.flight_mode = flight_mode

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}, position: {self.position}, orientation: {self.orientation}, flight mode: {self.flight_mode}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
