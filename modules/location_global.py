"""
Location on ground in WGS 84.

Class with name also available.
"""


class LocationGlobal:
    """
    WGS 84 following ISO 6709 (latitude before longitude).
    """

    __create_key = object()

    @classmethod
    def create(
        cls, latitude: float, longitude: float
    ) -> "tuple[True, LocationGlobal] | tuple[False, None]":
        """
        latitude: Decimal degrees.
        longitude: Decimal degrees.

        Return: Success, object.
        """
        return True, LocationGlobal(cls.__create_key, latitude, longitude)

    def __init__(self, class_private_create_key: object, latitude: float, longitude: float) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is LocationGlobal.__create_key, "Use create() method."

        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: latitude: {self.latitude}, longitude: {self.longitude}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)


class NamedLocationGlobal(LocationGlobal):
    """
    Named LocationGlobal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls, name: str, latitude: float, longitude: float
    ) -> "tuple[True, NamedLocationGlobal] | tuple[False, None]":
        """
        name: Can be empty.
        latitude: Decimal degrees.
        longitude: Decimal degrees.

        Return: Success, object.
        """
        return True, NamedLocationGlobal(cls.__create_key, name, latitude, longitude)

    def __init__(self, class_private_create_key: object, name: str, latitude: float, longitude: float) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is NamedLocationGlobal.__create_key, "Use create() method."

        super().__init__(super()._LocationGlobal__create_key, latitude, longitude)

        self.name = name

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}"
