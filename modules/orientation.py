"""
Orientation of object in 3D space.
"""

import math


class Orientation:
    """
    Yaw, pitch, roll following NED system (x forward, y right, z down).
    Specifically, intrinsic (Tait-Bryan) rotations in the zyx/3-2-1 order.

    Orientation is identical in local and global space.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        yaw: float,
        pitch: float,
        roll: float,
    ) -> "tuple[bool, Orientation] | tuple[False, None]":
        """
        yaw: Radians of [-pi, pi].
        pitch: Radians of [-pi, pi].
        roll: Radians of [-pi, pi].

        Return: Success, object.
        """
        if yaw < -math.pi or yaw > math.pi:
            return False, None

        if pitch < -math.pi or pitch > math.pi:
            return False, None

        if roll < -math.pi or roll > math.pi:
            return False, None

        return True, Orientation(cls.__create_key, yaw, pitch, roll)

    def __init__(
        self, class_private_create_key: object, yaw: float, pitch: float, roll: float
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Orientation.__create_key, "Use create() method."

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
