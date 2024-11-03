"""
Location local with name.
"""

from .. import location_global


class NamedLocationGlobal:
    """
    Location local with name.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, name: str, latitude: float, longitude: float
    ) -> "tuple[True, NamedLocationGlobal] | tuple[False, None]":
        """
        Name: Name of location. Cannot be empty.
        Latitude: Decimal degrees.
        Longitude: Decimal degrees.

        Return: Success, object.
        """
        if name == "":
            return False, None

        result, location = location_global.LocationGlobal.create(latitude, longitude)
        if not result:
            return False, None

        return True, NamedLocationGlobal(cls.__create_key, name, location)

    def __init__(
        self, class_private_create_key: object, name: str, location: location_global.LocationGlobal
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is NamedLocationGlobal.__create_key, "Use create() method."

        self.name = name
        self.location = location

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: {self.name}, location: {self.location}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)
