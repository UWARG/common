"""
Emulates position and attitude to Pixhawk.
"""


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, position_callback: callable
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Returns:
            Success, PositionEmulator instance.
        """

        return True, PositionEmulator(cls.__create_key, position_callback)

    def __init__(self, class_private_create_key: object, position_callback: callable) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self.position_callback = position_callback
