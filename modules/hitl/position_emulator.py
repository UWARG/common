"""
Emulates position and attitude to Pixhawk.
"""

import time
import math
from ..mavlink import dronekit


class PositionEmulator:
    """
    Setup for position emulator.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, drone: dronekit.Vehicle, movement_speed: float = 5.0
    ) -> "tuple[True, PositionEmulator] | tuple[False, None]":
        """
        Setup position emulator.

        Args:
            drone: The dronekit instance to use for sending MAVLink messages.
            movement_speed: Speed of drone movement in m/s, default is 5.0.

        Returns:
            Success, PositionEmulator instance.
        """

        return True, PositionEmulator(cls.__create_key, drone, movement_speed)

    def __init__(self, class_private_create_key: object, drone: dronekit.Vehicle, movement_speed: float = 5.0) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is PositionEmulator.__create_key, "Use create() method"

        self.target_position = (43.43405014107003, -80.57898027451816, 373.0)  # lat, lon, alt
        self.current_position = (43.43405014107003, -80.57898027451816, 373.0)  # lat, lon, alt
        self.movement_speed = movement_speed  # m/s
        self.last_update_time = time.time()
        self.waypoint_position = None  # Target waypoint from POSITION_TARGET_GLOBAL_INT

        self.drone = drone

    def set_target_position(self, latitude: float, longitude: float, altitude: float) -> None:
        """
        Sets the target position manually (currently a fallback if Ardupilot target doesnt work).

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            altitude: Altitude in meters.
        """
        self.target_position = (latitude, longitude, altitude)

    def set_waypoint_position(self, latitude: float, longitude: float, altitude: float) -> None:
        """
        Manually sets a waypoint for the emulator to move towards.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.
            altitude: Altitude in meters.
        """
        self.waypoint_position = (latitude, longitude, altitude)
        print(f"HITL Position: Manual waypoint set to {latitude:.6f}, {longitude:.6f}, {altitude:.1f}m")

    def get_target_position(self) -> tuple[float, float, float]:
        """
        Gets the target position from the Ardupilot target and stores it as waypoint.

        Returns:
            Current target position (not the waypoint).
        """
        # pylint: disable=protected-access
        position_target = None
        try:
            position_target = self.drone._master.recv_match(
                type="POSITION_TARGET_GLOBAL_INT", blocking=False
            )
        except Exception as exc:  # pylint: disable=broad-except
            print(f"HITL get_target_position recv_match error: {exc}")
            position_target = None
        # pylint: enable=protected-access

        if position_target:
            latitude = position_target.lat_int / 1e7
            longitude = position_target.lon_int / 1e7
            altitude = position_target.alt
            # Store as waypoint target instead of immediately using it
            self.waypoint_position = (latitude, longitude, altitude)

        # Return current target position for compatibility
        return self.target_position

    def calculate_distance(self, pos1: tuple[float, float, float], pos2: tuple[float, float, float]) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula.
        
        Args:
            pos1: First position (lat, lon, alt)
            pos2: Second position (lat, lon, alt)
            
        Returns:
            Distance in meters
        """
        lat1, lon1, alt1 = pos1
        lat2, lon2, alt2 = pos2
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula for horizontal distance
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in meters
        earth_radius = 6371000
        horizontal_distance = earth_radius * c
        
        # Add vertical distance
        vertical_distance = abs(alt2 - alt1)
        
        return math.sqrt(horizontal_distance**2 + vertical_distance**2)

    def interpolate_position(self, start: tuple[float, float, float], end: tuple[float, float, float], progress: float) -> tuple[float, float, float]:
        """
        Interpolate between two positions.
        
        Args:
            start: Starting position (lat, lon, alt)
            end: Ending position (lat, lon, alt)
            progress: Progress from 0.0 to 1.0
            
        Returns:
            Interpolated position (lat, lon, alt)
        """
        if progress >= 1.0:
            return end
        if progress <= 0.0:
            return start
            
        lat = start[0] + (end[0] - start[0]) * progress
        lon = start[1] + (end[1] - start[1]) * progress
        alt = start[2] + (end[2] - start[2]) * progress
        
        return (lat, lon, alt)

    def periodic(self) -> None:
        """
        Periodic function that handles gradual movement to waypoints.
        """
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Check for new waypoint from POSITION_TARGET_GLOBAL_INT
        self.get_target_position()

        # If we have a waypoint and we're not already there
        if self.waypoint_position is not None:
            distance_to_waypoint = self.calculate_distance(self.current_position, self.waypoint_position)
            
            # If we're close enough to the waypoint, consider it reached
            if distance_to_waypoint < 1.0:  # 1 meter tolerance
                print(f"HITL Position: Reached waypoint {self.waypoint_position[0]:.6f}, {self.waypoint_position[1]:.6f}, {self.waypoint_position[2]:.1f}m")
                self.current_position = self.waypoint_position
                self.target_position = self.waypoint_position
                self.waypoint_position = None  # Clear waypoint
            else:
                # Move towards the waypoint
                distance_to_move = self.movement_speed * dt
                progress = min(distance_to_move / distance_to_waypoint, 1.0)
                
                self.current_position = self.interpolate_position(
                    self.current_position, self.waypoint_position, progress
                )
                self.target_position = self.current_position

        # Inject the current interpolated position
        self.inject_position(
            self.current_position[0], self.current_position[1], self.current_position[2]
        )

        time.sleep(0.1) # 10 Hz

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
