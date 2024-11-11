"""
Location on the ground in local Euclidean space (origin at home position global).

Class with name also available.
"""


class LocationLocal:
    """
    Location in NED system relative to home position, with down = 0.0 .
    """

    __create_key = object()

    @classmethod
    def create(cls, north: float, east: float) -> "tuple[True, LocationLocal] | tuple[False, None]":
        """
        north: Metres.
        east: Metres.

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


class NamedLocationLocal(LocationLocal):
    """
    Named LocationLocal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls, name: str, north: float, east: float
    ) -> "tuple[True, NamedLocationLocal] | tuple[False, None]":
        """
        name: Can be empty.
        north: Metres.
        east: Metres.

        Return: Success, object.
        """
        return True, NamedLocationLocal(cls.__create_key, name, north, east)

    def __init__(self, class_private_create_key: object, name: str, north: float, east: float) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is NamedLocationLocal.__create_key, "Use create() method."

        super().__init__(super()._LocationLocal__create_key, north, east)

        self.name = name

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: name: {self.name}, north: {self.north}, east: {self.east}"
