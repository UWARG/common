"""
Drone odometry in local space (origin at home position global).
"""

from . import drone_odometry
from .. import position_local


class DroneOrientationLocal:
    """
    Wrapper for DroneOrientation as it is the same in both local and global space.
    """

    __create_key = object()

    @classmethod
    def create_new(
        cls, yaw: float, pitch: float, roll: float
    ) -> "tuple[True, DroneOrientationLocal] | tuple[False, None]":
        """
        Yaw, pitch, roll in radians.
        """
        result, orientation = drone_odometry.DroneOrientation.create(yaw, pitch, roll)
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert orientation is not None

        return True, DroneOrientationLocal(cls.__create_key, orientation)

    @classmethod
    def create_wrap(
        cls, orientation: drone_odometry.DroneOrientation
    ) -> "tuple[True, DroneOrientationLocal] | tuple[False, None]":
        """
        Wrap existing orientation.
        """
        return True, DroneOrientationLocal(cls.__create_key, orientation)

    def __init__(
        self, class_private_create_key: object, orientation: drone_odometry.DroneOrientation
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert (
            class_private_create_key is DroneOrientationLocal.__create_key
        ), "Use create() method."

        self.orientation = orientation

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: {self.orientation}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)


class DroneOdometryLocal:
    """
    Wrapper for DronePositionLocal and DroneOrientationLocal.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, position: position_local.PositionLocal, orientation: DroneOrientationLocal
    ) -> "tuple[True, DroneOdometryLocal] | tuple[False, None]":
        """
        Position and orientation in one class.
        """
        if position is None:
            return False, None

        if orientation is None:
            return False, None

        return True, DroneOdometryLocal(cls.__create_key, position, orientation)

    def __init__(
        self,
        class_private_create_key: object,
        position: position_local.PositionLocal,
        orientation: DroneOrientationLocal,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneOdometryLocal.__create_key, "Use create() method."

        self.position = position
        self.orientation = orientation

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: {self.position}, {self.orientation}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
