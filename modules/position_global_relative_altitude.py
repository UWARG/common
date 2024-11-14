"""
3D position in WGS 84.

Class with name also available.
"""


class PositionGlobalRelativeAltitude:
    """
    WGS 84 following ISO 6709 (latitude before longitude).

    Relative altitude to home position.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: float, longitude: float, relative_altitude: float
    ) -> "tuple[True, PositionGlobalRelativeAltitude] | tuple[False, None]":
        """
        latitude: Decimal degrees.
        longitude: Decimal degrees.
        relative_altitude: Metres above home position. Can be negative.

        Return: Success, object.
        """
        return True, PositionGlobalRelativeAltitude(
            cls.__create_key, latitude, longitude, relative_altitude
        )

    def __init__(
        self,
        class_private_create_key: object,
        latitude: float,
        longitude: float,
        relative_altitude: float,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert (
            class_private_create_key is PositionGlobalRelativeAltitude.__create_key
        ), "Use create() method."

        self.latitude = latitude
        self.longitude = longitude
        self.relative_altitude = relative_altitude

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: latitude: {self.latitude}, longitude: {self.longitude}, relative altitude: {self.relative_altitude}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)


class NamedPositionGlobalRelativeAltitude(PositionGlobalRelativeAltitude):
    """
    Named PositionGlobalRelativeAltitude.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls,
        name: str,
        latitude: float,
        longitude: float,
        relative_altitude: float,
    ) -> "tuple[True, NamedPositionGlobalRelativeAltitude] | tuple[False, None]":
        """
        name: Can be empty.
        latitude: Decimal degrees.
        longitude: Decimal degrees.
        relative_altitude: Metres above home position. Can be negative.

        Return: Success, object.
        """
        return True, NamedPositionGlobalRelativeAltitude(
            cls.__create_key, name, latitude, longitude, relative_altitude
        )

    def __init__(
        self,
        class_private_create_key: object,
        name: str,
        latitude: float,
        longitude: float,
        relative_altitude: float,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert (
            class_private_create_key is NamedPositionGlobalRelativeAltitude.__create_key
        ), "Use create() method."

        super().__init__(
            super()._PositionGlobalRelativeAltitude__create_key,
            latitude,
            longitude,
            relative_altitude,
        )

        self.name = name

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}, relative_altitude: {self.relative_altitude}"
