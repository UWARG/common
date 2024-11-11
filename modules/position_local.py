"""
Position in local Euclidean space (origin at home position global).
"""


class PositionLocal:
    """
    Position in NED system relative to home position.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, north: float, east: float, down: float
    ) -> "tuple[True, PositionLocal] | tuple[False, None]":
        """
        north: Metres.
        east: Metres.
        down: Metres. Allowed to be positive, which is below the home position.

        Return: Success, object.
        """
        return True, PositionLocal(cls.__create_key, north, east, down)

    def __init__(
        self, class_private_create_key: object, north: float, east: float, down: float
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionLocal.__create_key, "Use create() method."

        self.north = north
        self.east = east
        self.down = down

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: north: {self.north}, east: {self.east}, down: {self.down}"

    def __repr__(self) -> str:
        """
        For collections (e.g. list).
        """
        return str(self)


class NamedPositionLocal(PositionLocal):
    """
    Named PositionLocal.
    """

    __create_key = object()

    @classmethod
    # Additional argument for name
    # pylint: disable-next=arguments-differ
    def create(
        cls, name: str, north: float, east: float, down: float,
    ) -> "tuple[True, NamedPositionLocal] | tuple[False, None]":
        """
        name: Can be empty.
        north: Metres.
        east: Metres.
        down: Metres. Allowed to be positive, which is below the home position.

        Return: Success, object.
        """
        return True, NamedPositionLocal(cls.__create_key, name, north, east, down)

    def __init__(self, class_private_create_key: object, name: str, north: float, east: float, down: float) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is NamedPositionLocal.__create_key, "Use create() method."

        super().__init__(super()._PositionLocal__create_key, north, east, down)

        self.name = name

    def __str__(self) -> str:
        """
        To string.
        """
        return f"{self.__class__}: name: {self.name}, north: {self.north}, east: {self.east}, down: {self.down}"
