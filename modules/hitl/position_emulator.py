"""
Emulates position and attitude to Pixhawk.
"""

import json
import time
from ..mavlink import dronekit


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, drone: dronekit.Vehicle, json_file_path: str | None = None, update_interval: float = 1.0
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Args:
            drone: Dronekit vehicle instance.
            json_file_path: Optional path to JSON file containing coordinates.
            update_interval: Interval (seconds) between switching JSON coordinates.

        Returns:
            Success, PositionEmulator instance.
        """
        return True, PositionEmulator(cls.__create_key, drone, json_file_path, update_interval)

    def __init__(
        self,
        class_private_create_key: object,
        drone: dronekit.Vehicle,
        json_file_path: str | None = None,
        update_interval: float = 1.0,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self.target_position = (43.43405014107003, -80.57898027451816, 373.0)  # lat, lon, alt
        self.drone = drone
        self.json_file_path = json_file_path
        self.json_coordinates: list[list[float]] = []
        self.current_coordinate_index = 0
        self.update_interval = update_interval
        self.next_coordinate_time = time.time() + self.update_interval

        if self.json_file_path:
            self._load_json_coordinates()

    def _load_json_coordinates(self) -> None:
        """
        Loads coordinates from the JSON file and validates them.
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                self.json_coordinates = json.load(file)

            if not isinstance(self.json_coordinates, list) or not all(
                isinstance(coord, list) and len(coord) >= 3 for coord in self.json_coordinates
            ):
                raise ValueError("JSON must be a list of [lat, lon, alt] lists")

            print(f"HITL loaded {len(self.json_coordinates)} coordinates from {self.json_file_path}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"HITL JSON coordinate loading error: {exc}")
            self.json_coordinates = []

    def _next_json_coordinate(self) -> None:
        """
        Cycles to the next JSON coordinate and sets it as target position.
        """
        if not self.json_coordinates:
            return

        coordinate = self.json_coordinates[self.current_coordinate_index]
        latitude, longitude, altitude = coordinate[0], coordinate[1], coordinate[2]
        self.set_target_position(latitude, longitude, altitude)
        print(
            f"HITL set JSON coordinate {self.current_coordinate_index + 1}/{len(self.json_coordinates)}: "
            f"({latitude}, {longitude}, {altitude})"
        )

        # Cycle to next coordinate
        self.current_coordinate_index = (self.current_coordinate_index + 1) % len(self.json_coordinates)

<<<<<<< HEAD
=======
    def set_target_position(self, latitude: float, longitude: float, altitude: float) -> None:
        """
        Sets the target position manually.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            altitude: Altitude in meters.
        """
        self.target_position = (latitude, longitude, altitude)

    def get_target_position(self) -> tuple[float, float, float]:
        """
        Gets the target position from the Ardupilot target if available.

        Returns:
            Target position as (latitude, longitude, altitude).
        """
        # pylint: disable=protected-access
        try:
            position_target = self.drone._master.recv_match(
                type="POSITION_TARGET_GLOBAL_INT", blocking=False
            )
        except Exception as exc:  # pylint: disable=broad-except
            print(f"HITL get_target_position recv_match error: {exc}")
            return self.target_position
        # pylint: enable=protected-access

        if position_target:
            latitude = position_target.lat_int / 1e7
            longitude = position_target.lon_int / 1e7
            altitude = position_target.alt
            return (latitude, longitude, altitude)

        return self.target_position

    def periodic(self) -> None:
        """
        Periodic function. Updates target position either from JSON coordinates or Ardupilot.
        """
        now = time.time()

        if self.json_coordinates:
            # JSON has priority
            if now >= self.next_coordinate_time:
                try:
                    self._next_json_coordinate()
                except Exception as exc:  # pylint: disable=broad-except
                    print(f"HITL JSON coordinate update error: {exc}")
                self.next_coordinate_time = now + self.update_interval
        else:
            # Fallback: use Ardupilot position target
            self.target_position = self.get_target_position()

        self.inject_position(
            self.target_position[0], self.target_position[1], self.target_position[2]
        )

    def inject_position(
        self,
        latitude: float = 43.43405014107003,
        longitude: float = -80.57898027451816,
        altitude: float = 373.0,
    ) -> None:
        """
        Simulates gps coordinates by injecting the desired position of the drone.
        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            altitude: Altitude in meters.
        """
        values = [
            int(time.time() * 1e6),  # time_usec
            0,  # gps_id
            0b111111,  # ignore_flags (all fields valid)
            0,  # time_week_ms
            0,  # time_week
            3,  # fix_type (3D fix)
            int(latitude * 1e7),  # lat
            int(longitude * 1e7),  # lon
            int(altitude * 1000),  # alt (mm)
            100,  # hdop (x100)
            100,  # vdop (x100)
            0,  # vn (cm/s)
            0,  # ve (cm/s)
            0,  # vd (cm/s)
            100,  # speed_accuracy (cm/s)
            100,  # horiz_accuracy (cm)
            100,  # vert_accuracy (cm)
            10,  # satellites_visible
            0,  # yaw (deg*100)
        ]
        gps_input_msg = self.drone.message_factory.gps_input_encode(*values)
        self.drone.send_mavlink(gps_input_msg)
        self.drone.flush()