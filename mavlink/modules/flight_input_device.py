from dronekit import connect 

class FlightInputDevice: 

    def __init__(self, address: "str"):
        """
        address: tcp address (e.g. "tcp:127.0.0.1:14550")
        """
        self.drone = connect(address, wait_ready = True)
        assert self.drone is not None

    def get_data(self) -> "dict": 
        """
        For now since the only output is to odometry worker,
        will only get odometry data.
        """
        data = {}
        attitude_info = self.drone.attitude
        #in radians 
        data['pitch'] = attitude_info.pitch
        data['yaw'] = attitude_info.yaw
        data['roll'] = attitude_info.roll 
        
        location_info = self.drone.location
        data['alt'] = location_info.global_frame.alt
        data['lat'] = location_info.global_frame.lat
        data['lon'] = location_info.global_frame.lon

        #if needed, distance from range finder can be added as well

        if not data:
            return None

        return data