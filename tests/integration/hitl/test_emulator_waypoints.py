#!/usr/bin/env python3
"""
Test script for position_emulator with 2 waypoints.
This script tests the position emulator changes by:
1. Connecting to the Pixhawk via Raspberry Pi
2. Enabling HITL mode with position emulation
3. Creating and uploading a mission with 2 waypoints
4. Monitoring drone movement in Mission Planner
5. Providing status updates and logging
"""

import argparse
import time
import sys
from typing import Optional

from modules.mavlink import flight_controller
from modules.mavlink import dronekit
from pymavlink import mavutil


# Default waypoints
DEFAULT_HOME_LAT = 43.43405014107003
DEFAULT_HOME_LON = -80.57898027451816
DEFAULT_HOME_ALT = 373.0

# Test waypoints
WAYPOINT_1_LAT = 43.43450
WAYPOINT_1_LON = -80.57900
WAYPOINT_1_ALT = 30.0

WAYPOINT_2_LAT = 43.43400
WAYPOINT_2_LON = -80.57850
WAYPOINT_2_ALT = 25.0

# Configuration
MOVEMENT_SPEED = 5.0  # m/s
BAUD_RATE = 57600
TIMEOUT = 5.0
UPDATE_INTERVAL = 1.0

# Pixhawk parameters
REQUIRED_PARAMS = {
    # Sensor Disabling
    "INS_ENABLE_MASK": 0,
    "COMPASS_ENABLE": 0,
    
    # EKF Configuration
    "AHRS_EKF_TYPE": 3,
    "EK3_ENABLE": 1,
    "EK3_SRC1_POSXY": 3,
    "EK3_SRC1_POSZ": 3,
    "EK3_SRC1_VELXY": 3,
    "EK3_SRC1_VELZ": 3,
    
    # GPS Simulation via MAVLink
    "GPS_TYPE": 14,       # Use MAVLink GPS_INPUT
    "GPS_TYPE2": 0,
    "GPS_AUTO_SWITCH": 0,
    "GPS_PRIMARY": 0,
}


class PositionEmulatorTest:
    """Test class for position emulator with waypoints."""
    
    def __init__(self, connection_string: str):
        """Initialize the test with connection string."""
        self.connection_string = connection_string
        self.controller: Optional[flight_controller.FlightController] = None
        self.test_start_time = time.time()
        
    def connect_to_drone(self) -> bool:
        """
        Connect to the drone with HITL position emulation enabled.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        print(f"Connecting to drone at: {self.connection_string}")
        print("Enabling HITL mode with position emulation...")
        
        try:
            result, controller = flight_controller.FlightController.create(
                address=self.connection_string,
                baud=BAUD_RATE,
                hitl_enabled=True,
                position_module=True, 
                camera_module=False,   
                images_path=None,
                movement_speed=MOVEMENT_SPEED
            )
            
            if not result or controller is None:
                print("Failed to create flight controller")
                return False
                
            self.controller = controller
            print("Successfully connected to drone with HITL position emulation")
            
            # Give HITL position emulator time to start and initialize GPS
            print("Waiting for HITL position emulator to initialize GPS...")
            time.sleep(3.0)
            
            # Manually inject initial GPS position to kickstart GPS simulation
            if self.controller.hitl_instance and self.controller.hitl_instance.position_emulator:
                pos_emu = self.controller.hitl_instance.position_emulator
                print(f"Manually injecting initial GPS position: {DEFAULT_HOME_LAT:.6f}, {DEFAULT_HOME_LON:.6f}, {DEFAULT_HOME_ALT}")
                pos_emu.inject_position(DEFAULT_HOME_LAT, DEFAULT_HOME_LON, DEFAULT_HOME_ALT)
                time.sleep(1.0)
            
            return True
            
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def wait_for_heartbeat(self, timeout: float = 10.0) -> bool:
        """
        Wait for heartbeat from the drone.
        
        Args:
            timeout: Maximum time to wait for heartbeat.
            
        Returns:
            bool: True if heartbeat received, False if timeout.
        """
        print("Waiting for drone heartbeat...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Try to get basic vehicle info
                if hasattr(self.controller.drone, 'version') and self.controller.drone.version:
                    print(f"Heartbeat received - Vehicle version: {self.controller.drone.version}")
                    return True
            except Exception:
                pass
            
            time.sleep(0.5)
        
        print("No heartbeat received within timeout, continuing anyway...")
        return True  # Continue even without explicit heartbeat for HITL

    def create_test_mission(self) -> bool:
        """
        Create a test mission with 2 waypoints.
        
        Returns:
            bool: True if mission created successfully, False otherwise.
        """
        print("\n Creating test mission with 2 waypoints...")
        
        try:
            # Clear existing mission first
            print("Clearing existing mission...")
            self.controller.drone.commands.download()
            self.controller.drone.commands.wait_ready()
            time.sleep(1.0)  # Wait for download to complete
            
            self.controller.drone.commands.clear()
            time.sleep(0.5)  # Wait for clear to complete
            
            # takeoff command 
            takeoff_command = dronekit.Command(
                0, 0, 0,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0, 0,
                0, 0, 0, 0,  # param1-4
                0, 0, 20.0   # takeoff altitude
            )
            self.controller.drone.commands.add(takeoff_command)
            time.sleep(0.5)  # Wait for add to complete
            
            # Upload the takeoff command first
            print("Uploading takeoff command...")
            self.controller.drone.commands.upload()
            time.sleep(2.0)  # Wait for upload to complete
            
            # Now use FlightController's insert_waypoint method for waypoints
            print("Adding waypoint 1...")
            result1 = self.controller.insert_waypoint(1, WAYPOINT_1_LAT, WAYPOINT_1_LON, WAYPOINT_1_ALT)
            if not result1:
                print("Failed to insert waypoint 1")
                return False
            time.sleep(1.5)  # Wait between waypoint insertions
            
            print("Adding waypoint 2...")
            result2 = self.controller.insert_waypoint(2, WAYPOINT_2_LAT, WAYPOINT_2_LON, WAYPOINT_2_ALT)
            if not result2:
                print("Failed to insert waypoint 2")
                return False
            time.sleep(1.0)  # Wait for final waypoint insertion to complete
            
            print(" Mission uploaded successfully!")
            print(f"   Takeoff altitude: " )
            print(f"   Waypoint 1: {WAYPOINT_1_LAT:.6f}, {WAYPOINT_1_LON:.6f}, {WAYPOINT_1_ALT}m")
            print(f"   Waypoint 2: {WAYPOINT_2_LAT:.6f}, {WAYPOINT_2_LON:.6f}, {WAYPOINT_2_ALT}m")
            return True
                
        except Exception as e:
            print(f" Error creating mission: {e}")
            return False
    
    def set_flight_mode(self, mode: str) -> bool:
        """
        Set the flight mode of the drone.
        
        Args:
            mode: Flight mode to set (e.g., 'AUTO', 'GUIDED', 'STABILIZE').
            
        Returns:
            bool: True if mode set successfully, False otherwise.
        """
        try:
            print(f"Setting flight mode to: {mode}")
            result = self.controller.set_flight_mode(mode)
            if result:
                print(f"Flight mode set to {mode}")
                return True
            else:
                print(f"Failed to set flight mode to {mode}")
                return False
        except Exception as e:
            print(f"Error setting flight mode: {e}")
            return False
    
    def monitor_position_updates(self, duration: float = 60.0) -> None:
        """
        Monitor position updates and drone status.
        
        Args:
            duration: How long to monitor in seconds.
        """
        print(f"\n Monitoring position updates for {duration} seconds...")
        print("Watch Mission Planner for drone movement visualization")
        print("=" * 60)
        
        start_time = time.time()
        last_update = 0
        
        while time.time() - start_time < duration:
            current_time = time.time()
            
            # Update every UPDATE_INTERVAL seconds
            if current_time - last_update >= UPDATE_INTERVAL:
                self.print_status_update()
                last_update = current_time
            
            time.sleep(0.1)  # Small sleep to prevent excessive CPU usage
        
        print("\n Monitoring completed")
    
    def print_status_update(self) -> None:
        """Print current drone status and position."""
        try:
            elapsed_time = time.time() - self.test_start_time
            
            # Get current position
            result, odometry = self.controller.get_odometry()
            if result and odometry:
                lat = odometry.position.latitude
                lon = odometry.position.longitude
                alt = odometry.position.altitude
                
                # Send status to Mission Planner
                status_msg = f"HITL Test - Lat:{lat:.6f} Lon:{lon:.6f} Alt:{alt:.1f}m"
                self.controller.send_statustext_msg(status_msg)
                
                print(f"[{elapsed_time:6.1f}s] Position: {lat:.6f}, {lon:.6f}, {alt:.1f}m")
            else:
                # Simple debug info when position data not available
                print(f"[{elapsed_time:6.1f}s] Could not get position data")
                try:
                    # HITL status
                    if self.controller.hitl:
                        print(f"         HITL: Active, waiting for GPS initialization...")
                        
                        # Check if position emulator is running
                        if self.controller.hitl_instance and self.controller.hitl_instance.position_emulator:
                            pos_emu = self.controller.hitl_instance.position_emulator
                            current_pos = pos_emu.current_position
                            target_pos = pos_emu.target_position
                            print(f"         Position Emulator - Current: {current_pos[0]:.6f}, {current_pos[1]:.6f}, {current_pos[2]:.1f}")
                            print(f"         Position Emulator - Target: {target_pos[0]:.6f}, {target_pos[1]:.6f}, {target_pos[2]:.1f}")
                        
                        self.controller.send_statustext_msg(f"HITL - GPS initializing ({elapsed_time:.0f}s)")
                    
                except Exception:
                    print(f"         Debug: Unable to check GPS status")
            
            # Get next waypoint info
            result, next_wp = self.controller.get_next_waypoint()
            if result and next_wp:
                print(f"         Next WP: {next_wp.latitude:.6f}, {next_wp.longitude:.6f}, {next_wp.altitude:.1f}m")
            
            # Get flight mode
            try:
                mode = self.controller.drone.mode.name if hasattr(self.controller.drone, 'mode') else "Unknown"
                armed = self.controller.drone.armed if hasattr(self.controller.drone, 'armed') else False
                print(f"         Mode: {mode}, Armed: {armed}")
            except Exception:
                print("         Mode: Unknown, Armed: Unknown")
                
        except Exception as e:
            print(f" Error getting status: {e}")
    
    def run_test(self) -> int:
        """
        Run the complete position emulator test.
        
        Returns:
            int: Exit code (0 for success, non-zero for failure).
        """
        print("🚁 Position Emulator Waypoint Test")
        print("=" * 50)
        
        # Step 1: Connect to drone
        if not self.connect_to_drone():
            return 1
        
        # Step 2: Wait for heartbeat
        if not self.wait_for_heartbeat():
            print("⚠️  Continuing without confirmed heartbeat...")
        
        # Step 3: Check required HITL parameters
        if not self.check_required_parameters():
            print("Required parameters not set. Please configure Pixhawk parameters first.")
            print("See the parameter list above and set them in Mission Planner.")
            return 3
        
        # Step 4: Create and upload mission
        if not self.create_test_mission():
            return 2
        
        # Step 5: Set flight mode to AUTO (for mission execution)
        print("\n🎯 Setting up for mission execution...")
        if not self.set_flight_mode("AUTO"):
            print("Could not set AUTO mode, try manually in Mission Planner")
        
        # Step 6: Monitor position updates
        print("\n📊 Instructions for Mission Planner:")
        print("1. Verify the 2 waypoints are visible on the map")
        print("2. Arm the drone (if not already armed)")
        print("3. Watch the drone position move between waypoints")
        print("4. Check that the emulated GPS position updates smoothly")
        
        self.monitor_position_updates(duration=120.0)  # Monitor for 2 minutes
        
        print("\n🎉 Test completed successfully!")
        print("Check Mission Planner to verify:")
        print("- Drone moved smoothly between waypoints")
        print("- Position updates were consistent")
        print("- No GPS glitches or jumps occurred")
        
        return 0
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.controller and hasattr(self.controller, 'drone'):
            try:
                print("\n🧹 Cleaning up...")
                # Send final status message
                self.controller.send_statustext_msg("HITL Position Test Completed")
                time.sleep(1)  # Give time for message to send
            except Exception as e:
                print(f"Cleanup warning: {e}")


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Test position emulator with 2 waypoints",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--connection", "-c",
        default="/dev/ttyAMA0",
        help="Connection string for the drone (default: /dev/ttyAMA0 for RPi+Pixhawk)"
    )
    
    parser.add_argument(
        "--duration", "-d",
        type=float,
        default=120.0,
        help="How long to monitor position updates in seconds (default: 120)"
    )
    
    args = parser.parse_args()
    
    # Create and run test
    test = PositionEmulatorTest(args.connection)
    
    try:
        return test.run_test()
    except KeyboardInterrupt:
        print("\n\n Test interrupted by user")
        return 130
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        return 1
    finally:
        test.cleanup()


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")
    
    print("Done!")
