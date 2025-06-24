"""
Emulates position and attitude to Pixhawk.
"""

import time
from ..mavlink import dronekit


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, drone: dronekit.Vehicle
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Returns:
            Success, PositionEmulator instance.
        """

        return True, PositionEmulator(cls.__create_key, drone)

    def __init__(self, class_private_create_key: object, drone: dronekit.Vehicle) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self.drone = drone

    def inject_position(
        self,
        latitude: float = 43.43405014107003,
        longitude: float = -80.57898027451816,
        altitude: float = 373.0,
    ) -> None:
        """
        Inject fake GPS position into the drone via MAVLink GPS_INPUT.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            altitude: Altitude in meters.
        """
        gps_input_msg = self.drone.message_factory.gps_input_encode(
            int(time.time() * 1e6),  # timestamp (microseconds)
            0,  # gps_id
            0b111111,  # flags (all fields valid)
            0,
            0,  # week, week_ms (optional)
            int(latitude * 1e7),  # lat
            int(longitude * 1e7),  # lon
            int(altitude * 1000),  # alt in mm
            100,
            100,  # HDOP, VDOP (x100)
            0,
            0,
            0,  # velocity components
            0,
            0,
            0,  # speed_acc, horiz_acc, vert_acc
            10,  # satellites_visible
            3,  # fix_type (3D fix)
        )
        self.drone.send_mavlink(gps_input_msg)
        self.drone.flush()
