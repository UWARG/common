"""
Position and orientation of drone.
"""

import enum
import math


class DronePosition:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: "float | None", longitude: "float | None", altitude: "float | None"
    ) -> "tuple[bool, DronePosition | None]":
        """
        latitude, longitude in decimal degrees.
        altitude in metres.
        """
        if latitude is None:
            return False, None

        if longitude is None:
            return False, None

        if altitude is None:
            return False, None

        if altitude <= 0.0:
            return False, None

        return True, DronePosition(cls.__create_key, latitude, longitude, altitude)

    def __init__(
        self, class_private_create_key: object, latitude: float, longitude: float, altitude: float
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DronePosition.__create_key, "Use create() method"

        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}, latitude: {self.latitude}, longitude: {self.longitude}, altitude: {self.altitude}"


class DroneOrientation:
    """
    Yaw, pitch, roll following NED system (x forward, y right, z down).
    Specifically, intrinsic (Tait-Bryan) rotations in the zyx/3-2-1 order.
    """

    __create_key = object()

    @classmethod
    # Required for checks
    # pylint: disable-next=too-many-return-statements
    def create(
        cls, yaw: "float | None", pitch: "float | None", roll: "float | None"
    ) -> "tuple[bool, DroneOrientation | None]":
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
        assert class_private_create_key is DroneOrientation.__create_key, "Use create() method"

        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}, yaw: {self.yaw}, pitch: {self.pitch}, roll: {self.roll}"


class DroneWaypoint:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: "float | None", longitude: "float | None", altitude: "float | None"
    ) -> "tuple[bool, DronePosition | None]":
        """
        latitude, longitude in decimal degrees.
        altitude in metres.
        """
        if latitude is None:
            return False, None

        if longitude is None:
            return False, None

        if altitude is None:
            return False, None

        if altitude <= 0.0:
            return False, None

        return True, DroneWaypoint(cls.__create_key, latitude, longitude, altitude)

    def __init__(
        self, class_private_create_key: object, latitude: float, longitude: float, altitude: float
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneWaypoint.__create_key, "Use create() method"

        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__.__name__}, latitude: {self.latitude}, longitude: {self.longitude}, altitude: {self.altitude}"


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
        cls, position: DronePosition, orientation: DroneOrientation, flight_mode: FlightMode
    ) -> "tuple[bool, DroneOdometry | None]":
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
        position: DronePosition,
        orientation: DroneOrientation,
        flight_mode: FlightMode,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOdometry.__create_key, "Use create() method"

        self.position = position
        self.orientation = orientation
        self.flight_mode = flight_mode

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}, position: {self.position}, orientation: {self.orientation}, flight mode: {self.flight_mode}"
