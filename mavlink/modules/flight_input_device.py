"""
Creates a FlightInputDevice using dronekit which abstracts MavLink data
Formats odometry data to dictionary 
"""

import dronekit
from modules import drone_odometry


class FlightInputDevice: 
    """
    Wrapper for flight input.
    """
    __create_key = object()

    @classmethod
    def create(cls, address: str) -> "tuple[bool, FlightInputDevice | None]":
        """
        address: tcp address or serial port of the drone (e.g. "tcp:127.0.0.1:14550").
        Establishes address to drone and stores dronekit object inside instance drone.
        """
        try:
            drone = dronekit.connect(address, wait_ready = True)
        except dronekit.TimeoutError:
            print("No messages are being recieved. Make sure address/port is a host address/port.")
            print("")
            return False, None
        except ConnectionRefusedError: 
            print("Cannot connect to drone! Make sure the address/port is correct.")
            print("")
            return False, None
        return True, FlightInputDevice(cls.__create_key, drone)
        
    def __init__(self, class_private_create_key, vehicle: dronekit.Vehicle):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is FlightInputDevice.__create_key, "Use create() method"
        
        self.drone = vehicle

    def get_odometry(self) -> "tuple[bool, drone_odometry.DroneOdometry | None]":
        """
        Returns odometry data as an instance of DroneOdometry from the drone or None if missing either orientation or position.
        """
        attitude_info = self.drone.attitude
        result, orientation_data = drone_odometry.DroneOrientation.create(attitude_info.yaw, attitude_info.pitch, attitude_info.roll)
        if not result:
            return False, None
        location_info = self.drone.location
        result, position_data = drone_odometry.DronePosition.create(location_info.global_frame.lat, location_info.global_frame.lon, location_info.global_frame.alt)
        if not result:
            return False, None
        result, odometry_data = drone_odometry.DroneOdometry.create(position_data, orientation_data)
        if not result:
            return False, None
        return True, odometry_data
