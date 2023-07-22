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
        Connection address: tcp address or serial port (e.g. "tcp:127.0.0.1:14550").
        Establishes address to host and stores inside instance self.drone.
        """
        drone = dronekit.connect(address, wait_ready = True)
        
        if drone is not None:
            return True, FlightInputDevice(cls.__create_key, drone) 
        
    def __init__(self, class_private_create_key, vehicle):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is FlightInputDevice.__create_key, "Use create() method"
        
        self.drone = vehicle

    def get_data(self) -> "tuple[bool, drone_odometry.DroneOdometry | None]":
        """
        For now since the only output is to odometry worker, will only get odometry data.
        Returns odometry data in dictionary from the drone or None if missing either orientation or position.
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
    