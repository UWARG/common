"""
Position and orientation of drone.
"""
import math


# Basically a struct
# pylint: disable=too-few-public-methods
class DronePosition:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """
    __create_key = object()

    @classmethod
    def create(cls,
               latitude: "float | None",
               longitude: "float | None",
               altitude: "float | None") -> "tuple[bool, DronePosition | None]":
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

    def __init__(self,
                 class_private_create_key,
                 latitude: float,
                 longitude: float,
                 altitude: float):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DronePosition.__create_key, "Use create() method"

        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

# pylint: enable=too-few-public-methods


# Basically a struct
# pylint: disable=too-few-public-methods
class DroneOrientation:
    """
    Yaw, pitch, roll following NED system (x forward, y right, z down).
    Specifically, intrinsic (Tait-Bryan) rotations in the zyx/3-2-1 order.
    """
    __create_key = object()

    @classmethod
    # Required for checks
    # pylint: disable-next=too-many-return-statements
    def create(cls,
               yaw: "float | None",
               pitch: "float | None",
               roll: "float | None") -> "tuple[bool, DroneOrientation | None]":
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

    def __init__(self, class_private_create_key, yaw: float, pitch: float, roll: float):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOrientation.__create_key, "Use create() method"

        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

# pylint: enable=too-few-public-methods


# Basically a struct
# pylint: disable=too-few-public-methods
class DroneOdometry:
    """
    Wrapper for DronePosition and DroneOrientation.
    """
    __create_key = object()

    @classmethod
    def create(cls,
               position: DronePosition,
               orientation: DroneOrientation) -> "tuple[bool, DroneOdometry | None]":
        """
        Position and orientation in one class.
        """
        if position is None:
            return False, None

        if orientation is None:
            return False, None

        return True, DroneOdometry(cls.__create_key, position, orientation)

    def __init__(self,
                 class_private_create_key,
                 position: DronePosition,
                 orientation: DroneOrientation):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOdometry.__create_key, "Use create() method"

        self.position = position
        self.orientation = orientation
