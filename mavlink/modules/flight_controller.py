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
    LOITER_ALTITUDE = 10.0  # Example altitude, adjust as necessary

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

    def __init__(self, class_private_create_key, vehicle: dronekit.Vehicle):
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

    def get_home_location(self,
                          timeout: float) -> "tuple[bool, drone_odometry.DronePosition | None]":
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

    def hover_above_location(self, latitude: float, longitude: float) -> bool:
            self.drone.mode = dronekit.VehicleMode("GUIDED")
            loiter_location = dronekit.LocationGlobal(latitude, longitude, self.LOITER_ALTITUDE)
            self.drone.simple_goto(loiter_location)
            return True

    def move_to_position(self, position: drone_odometry.DronePosition) -> bool:
        """
        Commands the drone to move to a specified position in 3D space.
        """
        try:
            self.drone.mode = dronekit.VehicleMode("GUIDED")
            # Create a LocationGlobal object with the specified latitude,
            # longitude, and altitude from the target destination
            target_location = dronekit.LocationGlobal(position.latitude, position.longitude, position.altitude)
            self.drone.simple_goto(target_location)
            
            return True
        except Exception as e:
            print(f"ERROR in move_to_position() method: {e}")
            return False