"""
Location on the ground in local Euclidean space (origin at home position global).
"""


class LocationLocal:
    """
    Location in NED system, with down = 0.0 .
    """

    __create_key = object()

    @classmethod
    def create(cls, north: float, east: float) -> "tuple[True, LocationLocal] | tuple[False, None]":
        """
        North: Metres.
        East: Metres.

        Return: Success, object.
        """
        return True, LocationLocal(cls.__create_key, north, east)

    def __init__(self, class_private_create_key: object, north: float, east: float) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is LocationLocal.__create_key, "Use create() method."

        self.north = north
        self.east = east

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: north: {self.north}, east: {self.east}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
