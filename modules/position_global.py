"""
3D position in WGS 84.
"""


class PositionGlobal:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: float, longitude: float, altitude: float
    ) -> "tuple[True, PositionGlobal] | tuple[False, None]":
        """
        latitude: Decimal degrees.
        longitude: Decimal degrees.
        altitude: Metres above mean sea level (MSL). Can be negative.

        Return: Success, object.
        """
        return True, PositionGlobal(cls.__create_key, latitude, longitude, altitude)

    def __init__(
        self, class_private_create_key: object, latitude: float, longitude: float, altitude: float
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionGlobal.__create_key, "Use create() method."

        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: latitude: {self.latitude}, longitude: {self.longitude}, altitude: {self.altitude}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
