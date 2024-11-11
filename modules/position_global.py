"""
3D position in WGS 84.

Class with name also available.
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


class NamedPositionGlobal(PositionGlobal):
    """
    Named PositionGlobal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls, name: str, latitude: float, longitude: float, altitude: float,
    ) -> "tuple[True, NamedPositionGlobal] | tuple[False, None]":
        """
        name: Can be empty.
        latitude: Decimal degrees.
        longitude: Decimal degrees.
        altitude: Metres above mean sea level (MSL). Can be negative.

        Return: Success, object.
        """
        return True, NamedPositionGlobal(cls.__create_key, name, latitude, longitude, altitude)

    def __init__(self, class_private_create_key: object, name: str, latitude: float, longitude: float, altitude: float) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is NamedPositionGlobal.__create_key, "Use create() method."

        super().__init__(super()._PositionGlobal__create_key, latitude, longitude, altitude)

        self.name = name

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}, altitude: {self.altitude}"
