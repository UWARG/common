"""
Wrapper for the flight controller.
"""

import time

import dronekit

from . import drone_odometry


class FlightController:
    """
    Wrapper for DroneKit-Python and MAVLink.
    """

    __create_key = object()

    __MAVLINK_LANDING_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
    __MAVLINK_LANDING_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_LAND

    @classmethod
    def create(cls, address: str) -> "tuple[bool, FlightController | None]":
        """
        address: TCP address or serial port of the drone (e.g. "tcp:127.0.0.1:14550").
        Establishes connection to drone through provided address
        and stores the DroneKit object.
        """
        try:
            # Wait ready is false as the drone may be on the ground
            drone = dronekit.connect(address, wait_ready=False)
        except dronekit.TimeoutError:
            print("No messages are being received. Make sure address/port is a host address/port.")
            return False, None
        except ConnectionRefusedError:
            print("Cannot connect to drone! Make sure the address/port is correct.")
            return False, None

        return True, FlightController(cls.__create_key, drone)

    def __init__(self, class_private_create_key: object, vehicle: dronekit.Vehicle) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is FlightController.__create_key, "Use create() method"

        self.drone = vehicle

    def get_odometry(self) -> "tuple[bool, drone_odometry.DroneOdometry | None]":
        """
        Returns odometry data from the drone.
        """
        attitude_info = self.drone.attitude
        result, orientation_data = drone_odometry.DroneOrientation.create(
            attitude_info.yaw,
            attitude_info.pitch,
            attitude_info.roll,
        )
        if not result:
            return False, None

        location_info = self.drone.location
        result, position_data = drone_odometry.DronePosition.create(
            location_info.global_frame.lat,
            location_info.global_frame.lon,
            location_info.global_frame.alt,
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert position_data is not None
        assert orientation_data is not None

        result, odometry_data = drone_odometry.DroneOdometry.create(
            position_data,
            orientation_data,
        )
        if not result:
            return False, None

        return True, odometry_data

    def get_home_location(
        self, timeout: float
    ) -> "tuple[bool, drone_odometry.DronePosition | None]":
        """
        Attempts to get the drone's home location until timeout.
        timeout: Seconds.
        """
        start_time = time.time()
        while self.drone.home_location is None and time.time() - start_time < timeout:
            commands = self.drone.commands
            commands.download()
            commands.wait_ready()

        # Timeout
        if self.drone.home_location is None:
            return False, None

        result, location = drone_odometry.DronePosition.create(
            self.drone.home_location.lat,
            self.drone.home_location.lon,
            self.drone.home_location.alt,
        )
        if not result:
            return False, None

        return True, location

    def upload_commands(self, commands: "list[dronekit.Command]") -> bool:
        """
        Writes a mission to the drone from a list of commands (will overwrite any previous missions).

        Parameters
        ----------
        commands: List of commands.

        Returns
        -------
        bool: Whether the upload is successful.
        """
        if len(commands) == 0:
            return False

        try:
            command_sequence = self.drone.commands
            command_sequence.download()
            command_sequence.wait_ready()
            command_sequence.clear()
            for command in commands:
                command_sequence.add(command)

            # Upload commands to drone
            command_sequence.upload()
        except dronekit.TimeoutError:
            print("Upload timeout, commands are not being sent.")
            return False
        except ConnectionResetError:
            print("Connection with drone reset. Unable to upload commands.")
            return False

        return True

    def upload_land_command(self, latitude: float, longitude: float) -> bool:
        """
        Given a target latitude and longitude, overwrite the drone's current mission
        with a corresponding land command.

        Parameters
        ----------
        latitude: Decimal degrees.
        longitude: Decimal degrees.

        Returns
        -------
        bool: Whether the upload is successful.
        """
        # TODO: DroneKit-Python's Command uses floating point value, which is not accurate enough for WARG. Investigate using MAVLink's integer command.
        landing_command = dronekit.Command(
            0,
            0,
            0,
            self.__MAVLINK_LANDING_FRAME,
            self.__MAVLINK_LANDING_COMMAND,
            0,
            0,
            0,  # param1
            0,
            0,
            0,
            latitude,
            longitude,
            0,
        )

        return self.upload_commands([landing_command])

    def is_drone_destination_final_waypoint(self) -> "tuple[bool, bool | None]":
        """
        Returns if the drone's destination is the final waypoint in the mission.

        Returns
        -------
        tuple[bool, bool | None]
            The first boolean in the tuple represents if retrieving the mission
            information is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be a boolean
              indicating if the drone's destination is set to the final
              waypoint in the mission.
        """
        waypoint_count = self.drone.commands.count
        current_waypoint = self.drone.commands.next

        if waypoint_count < 0 or current_waypoint < 0:
            return False, None

        if waypoint_count == 0:
            return True, False

        return True, (current_waypoint == waypoint_count)
