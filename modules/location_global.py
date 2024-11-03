"""
Location on ground in WGS 84.
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
