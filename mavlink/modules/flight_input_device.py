"""
Creates a FlightInputDevice using dronekit which abstracts MavLink data
Formats odometry data to dictionary 
"""

import dronekit
import modules.drone_odometry as drone_odometry

class FlightInputDevice: 
    """
    Wrapper for flight input
    """

    def __init__(self, address: "str"):
        """
        Connection address: tcp address (e.g. "tcp:127.0.0.1:14550")
        Establishes address to host and stores inside instance self.drone
        """
        self.drone = dronekit.connect(address, wait_ready = True)
        assert self.drone is not None

    def get_data(self) -> "drone_odometry.DroneOdometry | None":
        """
        For now since the only output is to odometry worker,
        will only get odometry data.

        Returns odometry data in dictionary from the drone or None if missing either orientation or position 
        """

        attitude_info = self.drone.attitude
        recieved_orientation, orientation_data = drone_odometry.DroneOrientation.create(attitude_info.yaw, attitude_info.pitch, attitude_info.roll)
        
        location_info = self.drone.location
        recieved_position, position_data = drone_odometry.DronePosition.create(location_info.global_frame.lat, location_info.global_frame.lon, location_info.global_frame.alt)

        if not recieved_orientation or recieved_position:
            return None

        recieved_odometry, odometry_data = drone_odometry.DroneOdometry.create(position_data, orientation_data)

        if not recieved_odometry:
            return None

        return odometry_data