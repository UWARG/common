"""
Wrapper for the flight controller.
"""

import time
import enum

from pymavlink import mavutil
from modules.hitl import hitl_base

from . import drone_odometry_global
from . import dronekit
from .. import orientation
from .. import position_global


class MAVLinkMessage(enum.Enum):
    """
    Possible MAVLink Message Types
    """

    DEBUG_VECT = 250
    NAMED_VALUE_FLOAT = 251
    NAMED_VALUE_INT = 252
    STATUSTEXT = 253


class MAVLinkMessager:
    """
    Wrapper for MAVLink
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        vehicle: mavutil.mavtcp,
    ) -> "tuple[bool, MAVLinkMessager] | tuple[False, None]":
        """
        Abstraction from MAVLink Message
        """
        if vehicle is None:
            return False, None

        return True, MAVLinkMessager(cls.__create_key, vehicle)

    def __init__(
        self,
        class_private_create_key: object,
        vehicle: mavutil.mavtcp,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is MAVLinkMessager.__create_key, "Use create() method."

        self.mav = vehicle.mav
        self.start_time = vehicle.start_time

    def status_text_send(
        self,
        data: dict,
        severity: int = mavutil.mavlink.MAV_SEVERITY_INFO,
    ) -> bool:
        """
        Sending a STATUSTEXT MavLink Message
        """
        if data["text"] is None:
            print("Text is required to send STATUSTEXT message")
            return False
        if not isinstance(data["text"], str):
            print("Text must be of type string to send STATUSTEXT message")
            return False
        text_bytes = data["text"].encode("utf-8")
        if len(text_bytes) > 50:
            print("Text too long, cannot send STATUSTEXT message")
            return False
        self.mav.statustext_send(severity, text_bytes)
        return True

    def debug_vect_send(
        self,
        data: dict,
    ) -> bool:
        """
        Sending a DEBUG_VECT MavLink Message
        """
        if data["name"] is None:
            print("Name is required to send DEBUG_VECT message")
            return False
        if not isinstance(data["name"], str):
            print("Name must be of type string to send DEBUG_VECT message")
            return False
        name_bytes = data["name"].encode("utf-8")
        if len(name_bytes) > 10:
            print("Name too long, cannot send DEBUG_VECT message")
            return False
        if data["x"] is None or data["y"] is None or data["z"] is None:
            print("Values x, y, z, are needed to send a DEBUG_VECT message")
            return False
        if (
            not isinstance(data["x"], float)
            or not isinstance(data["y"], float)
            or not isinstance(data["z"], float)
        ):
            print("Values x, y, z, must be of type float to send a DEBUG_VECT message")
            return False
        self.mav.debug_vect_send(
            x=data["x"],
            y=data["y"],
            z=data["z"],
            name=name_bytes,
            time_usec=int(time.time() * (10**6)),  # Convert s to us
        )
        return True

    def named_value_float_send(
        self,
        data: dict,
    ) -> bool:
        """
        Sending a NAMED_VALUE_FLOAT MavLink Message
        """
        if data["name"] is None:
            print("Name is required to send NAMED_VALUE_FLOAT message")
            return False
        if not isinstance(data["name"], str):
            print("Name must be of type string to send NAMED_VALUE_FLOAT message")
            return False
        name_bytes = data["name"].encode("utf-8")
        if len(name_bytes) > 10:
            print("Name too long, cannot send NAMED_VALUE_FLOAT message")
            return False
        if data["value"] is None:
            print("Value is required to send NAMED_VALUE_FLOAT message")
            return False
        if not isinstance(data["value"], float):
            print("Value must be of type float to send NAMED_VALUE_FLOAT message")
            return False
        self.mav.named_value_float_send(
            value=data["value"],
            name=name_bytes,
            time_boot_ms=int(time.time() - self.start_time) * (10**3),  # Convert s to ms
        )
        return True

    def named_value_int_send(
        self,
        data: dict,
    ) -> bool:
        """
        Sending a NAMED_VALUE_INT MavLink Message
        """
        if data["name"] is None:
            print("Name is required to send NAMED_VALUE_INT message")
            return False
        if not isinstance(data["name"], str):
            print("Name must be of type string to send NAMED_VALUE_INT message")
            return False
        name_bytes = data["name"].encode("utf-8")
        if len(name_bytes) > 10:
            print("Name too long, cannot send NAMED_VALUE_INT message")
            return False
        if data["value"] is None:
            print("Value is required to send NAMED_VALUE_INT message")
            return False
        if not isinstance(data["value"], int):
            print("Value must be of type int to send NAMED_VALUE_INT message")
            return False
        self.mav.named_value_int_send(
            value=data["value"],
            name=name_bytes,
            time_boot_ms=int(time.time() - self.start_time) * (10**3),  # Convert s to ms
        )
        return True

    def send_message(self, data: dict, message_type: MAVLinkMessage) -> bool:
        """
        Sending a General MavLink Message
        """
        if message_type == MAVLinkMessage.DEBUG_VECT:
            return self.debug_vect_send(data)
        if message_type == MAVLinkMessage.NAMED_VALUE_FLOAT:
            return self.named_value_float_send(data)
        if message_type == MAVLinkMessage.NAMED_VALUE_INT:
            return self.named_value_int_send(data)
        if message_type == MAVLinkMessage.STATUSTEXT:
            return self.status_text_send(data)
        print("Invalid MAVLinkMessage Value. Could not send MAVLink Message.")
        return False


class FlightController:
    """
    Wrapper for DroneKit-Python and MAVLink.
    """

    __create_key = object()

    __MAVLINK_LANDING_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL
    __MAVLINK_LANDING_COMMAND = mavutil.mavlink.MAV_CMD_NAV_LAND
    __MAVLINK_WAYPOINT_COMMAND = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

    @classmethod
    def create(
        cls,
        address: str,
        baud: int = 57600,
        hitl_enabled: bool = False,
        position_module: bool = False,
        camera_module: bool = False,
        images_path: str | None = None,
    ) -> "tuple[bool, FlightController | None]":
        """
        address: TCP address or serial port of the drone (e.g. "tcp:127.0.0.1:14550").
        baud: Baud rate for the connection (default is 57600).
        mode: True to enable HITL mode, False or None to disable it.
        Establishes connection to drone through provided address
        and stores the DroneKit object.
        """

        try:
            # Wait ready is false as the drone may be on the ground
            drone = dronekit.connect(
                address, wait_ready=False, baud=baud, source_component=0, source_system=1
            )
            # Enable/disable HITL based on mode
            success, hitl_instance = hitl_base.HITL.create(
                drone, hitl_enabled, position_module, camera_module, images_path
            )
            if success:
                if hitl_enabled and hitl_instance is not None:
                    hitl_instance.start()
            else:
                print("Error creating HITL module")

        except dronekit.TimeoutError:
            print("No messages are being received. Make sure address/port is a host address/port.")
            return False, None
        except ConnectionRefusedError:
            print("Cannot connect to drone! Make sure the address/port is correct.")
            return False, None

        return True, FlightController(cls.__create_key, drone, hitl_enabled, hitl_instance)

    def __init__(
        self,
        class_private_create_key: object,
        vehicle: dronekit.Vehicle,
        hitl: bool,
        hitl_instance: hitl_base.HITL | None = None,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is FlightController.__create_key, "Use create() method"

        self.drone = vehicle
        self.hitl = hitl
        self.hitl_instance = hitl_instance

    def get_odometry(self) -> "tuple[bool, drone_odometry_global.DroneOdometryGlobal | None]":
        """
        Returns odometry data from the drone.
        """
        attitude_info = self.drone.attitude
        if attitude_info is None:
            return False, None

        if attitude_info.yaw is None or attitude_info.pitch is None or attitude_info.roll is None:
            return False, None

        result, orientation_data = orientation.Orientation.create(
            attitude_info.yaw,
            attitude_info.pitch,
            attitude_info.roll,
        )
        if not result:
            return False, None

        location_info = self.drone.location
        if location_info is None:
            return False, None

        location_info_global = location_info.global_frame
        if location_info_global is None:
            return False, None

        if (
            location_info_global.lat is None
            or location_info_global.lon is None
            or location_info_global.alt is None
        ):
            return False, None

        result, position_data = position_global.PositionGlobal.create(
            location_info.global_frame.lat,
            location_info.global_frame.lon,
            location_info.global_frame.alt,
        )
        if not result:
            return False, None

        result, flight_mode = self.get_flight_mode()
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert position_data is not None
        assert orientation_data is not None
        assert flight_mode is not None

        result, odometry_data = drone_odometry_global.DroneOdometryGlobal.create(
            position_data, orientation_data, flight_mode
        )
        if not result:
            return False, None

        return True, odometry_data

    def get_location(self) -> "tuple[bool, tuple[float, float, float] | None]":
        """Return (lat, lon, alt) if available via the drone, otherwise (False, None)."""
        try:
            loc = self.drone.location
        except Exception:  # pylint: disable=broad-except
            print("get_location: could not complete request")
            return False, None

        if loc is None or loc.global_frame is None:
            return False, None

        gf = loc.global_frame
        if gf.lat is None or gf.lon is None or gf.alt is None:
            return False, None

        return True, (gf.lat, gf.lon, gf.alt)

    def get_home_position(
        self, timeout: float
    ) -> "tuple[bool, position_global.PositionGlobal | None]":
        """
        Attempts to get the drone's home position until timeout.
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

        result, position = position_global.PositionGlobal.create(
            self.drone.home_location.lat,
            self.drone.home_location.lon,
            self.drone.home_location.alt,
        )
        if not result:
            return False, None

        return True, position

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

    def move_to_position(self, position: position_global.PositionGlobal) -> bool:
        """
        Commands the drone to move to a specified position in 3D space.
        There is no check to verify that the specified altitude is above ground.
        """
        try:
            self.drone.mode = dronekit.VehicleMode("GUIDED")
            # Create a LocationGlobal object with the specified latitude,
            # longitude, and altitude from the target destination
            target_location = dronekit.LocationGlobal(
                position.latitude, position.longitude, position.altitude
            )
            self.drone.simple_goto(target_location)

            return True
        except KeyError:
            print("ERROR: an unsupported flight mode is set by dronekit.VehicleMode()")
            return False
        except dronekit.APIException as e:
            print(f"ERROR in move_to_position() method: {e}")
            return False

    def set_flight_mode(self, mode: str) -> bool:
        """
        Changes the flight mode of the drone.
        https://ardupilot.org/copter/docs/flight-modes.html
        """
        try:
            self.drone.mode = dronekit.VehicleMode(mode)
        except KeyError:
            print("ERROR: an unsupported flight mode is set by dronekit.VehicleMode()")
            return False
        return True

    def get_flight_mode(self) -> "tuple[bool, drone_odometry_global.FlightMode | None]":
        """
        Gets the current flight mode of the drone.
        """
        flight_mode = self.drone.mode.name

        if flight_mode is None:
            return False, None
        if flight_mode == "LOITER":
            return True, drone_odometry_global.FlightMode.STOPPED
        if flight_mode == "AUTO":
            return True, drone_odometry_global.FlightMode.MOVING
        return True, drone_odometry_global.FlightMode.MANUAL

    def download_commands(self) -> "tuple[bool, list[dronekit.Command]]":
        """
        Downloads the current list of commands from the drone.

        Returns
        -------
        tuple[bool, list[dronekit.Command]]
        A tuple where the first element is a boolean indicating success or failure,
        and the second element is the list of commands currently held by the drone.
        """
        try:
            command_sequence = self.drone.commands
            command_sequence.download()
            command_sequence.wait_ready()
            commands = list(command_sequence)
            return True, commands
        except dronekit.TimeoutError:
            print("ERROR: Download timeout, commands are not being received.")
            return False, []
        except ConnectionResetError:
            print("ERROR: Connection with drone reset. Unable to download commands.")
            return False, []

    def get_next_waypoint(self) -> "tuple[bool, position_global.PositionGlobal | None]":
        """
        Gets the next waypoint.

        Return: Success, waypoint position.
        """
        result, commands = self.download_commands()
        if not result:
            return False, None

        next_command_index = self.drone.commands.next
        if next_command_index >= len(commands):
            return False, None

        for command in commands[next_command_index:]:
            if command.command == self.__MAVLINK_WAYPOINT_COMMAND:
                return position_global.PositionGlobal.create(command.x, command.y, command.z)

        return False, None

    def insert_waypoint(
        self, index: int, latitude: float, longitude: float, altitude: float
    ) -> bool:
        """
        Insert a waypoint into the current list of commands at a certain index and reupload the list to the drone.
        """
        result, commands = self.download_commands()
        if not result:
            return False

        new_waypoint = dronekit.Command(
            0,
            0,
            0,
            self.__MAVLINK_LANDING_FRAME,
            self.__MAVLINK_WAYPOINT_COMMAND,
            0,
            0,
            0,  # param1
            0,
            0,
            0,
            latitude,
            longitude,
            altitude,
        )

        commands.insert(index, new_waypoint)

        return self.upload_commands(commands)

    def send_statustext_msg(
        self,
        message: str,
        severity: int = mavutil.mavlink.MAV_SEVERITY_INFO,
    ) -> bool:
        """
        Sends a STATUSTEXT message to the vehicle.
        """
        message_bytes = message.encode("utf-8")
        if len(message_bytes) > 50:
            print("Message too long, cannot send STATUSTEXT message")
            return False
        msg = self.drone.message_factory.statustext_encode(severity, message_bytes)
        self.drone.send_mavlink(msg)
        return True
