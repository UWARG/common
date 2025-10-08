#!/usr/bin/env python3
"""
Test script for position_emulator with 2 waypoints.

"""

import argparse
import time
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


class PositionEmulatorTest:
    """Test class for position emulator with waypoints."""

    def __init__(self, connection_string: str) -> None:
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
                movement_speed=MOVEMENT_SPEED,
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
                print(
                    f"Manually injecting initial GPS position: {DEFAULT_HOME_LAT:.6f}, {DEFAULT_HOME_LON:.6f}, {DEFAULT_HOME_ALT}"
                )
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
                if hasattr(self.controller.drone, "version") and self.controller.drone.version:
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
                0,
                0,
                0,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0,
                0,
                0,
                0,
                0,
                0,  # param1-4
                0,
                0,
                20.0,  # takeoff altitude
            )
            self.controller.drone.commands.add(takeoff_command)
            time.sleep(0.5)  # Wait for add to complete

            # Upload the takeoff command first
            print("Uploading takeoff command...")
            self.controller.drone.commands.upload()
            time.sleep(2.0)  # Wait for upload to complete

            # Now use FlightController's insert_waypoint method for waypoints
            print("Adding waypoint 1...")
            result1 = self.controller.insert_waypoint(
                1, WAYPOINT_1_LAT, WAYPOINT_1_LON, WAYPOINT_1_ALT
            )
            if not result1:
                print("Failed to insert waypoint 1")
                return False
            time.sleep(1.5)  # Wait between waypoint insertions

            print("Adding waypoint 2...")
            result2 = self.controller.insert_waypoint(
                2, WAYPOINT_2_LAT, WAYPOINT_2_LON, WAYPOINT_2_ALT
            )
            if not result2:
                print("Failed to insert waypoint 2")
                return False
            time.sleep(1.0)  # Wait for final waypoint insertion to complete

            print(" Mission uploaded successfully!")
            print(f"   Takeoff altitude: ")
            print(f"   Waypoint 1: {WAYPOINT_1_LAT:.6f}, {WAYPOINT_1_LON:.6f}, {WAYPOINT_1_ALT}m")
            print(f"   Waypoint 2: {WAYPOINT_2_LAT:.6f}, {WAYPOINT_2_LON:.6f}, {WAYPOINT_2_ALT}m")
            return True

        except Exception as e:
            print(f" Error creating mission: {e}")
            return False

    def test_manual_waypoints(self) -> None:
        """
        Test manual waypoint movement
        """
        print("\n Testing manual waypoint movement...")

        if not (self.controller.hitl_instance and self.controller.hitl_instance.position_emulator):
            print(" Position emulator not available")
            return

        pos_emu = self.controller.hitl_instance.position_emulator

        # Test sequence: Move to waypoint 1, then waypoint 2
        waypoints = [
            (WAYPOINT_1_LAT, WAYPOINT_1_LON, WAYPOINT_1_ALT, "Waypoint 1"),
            (WAYPOINT_2_LAT, WAYPOINT_2_LON, WAYPOINT_2_ALT, "Waypoint 2"),
        ]

        for lat, lon, alt, name in waypoints:
            print(f"\n📍 Setting {name}: {lat:.6f}, {lon:.6f}, {alt:.1f}m")
            pos_emu.set_waypoint_position(lat, lon, alt)

            # Monitor movement to this waypoint
            print(f"🚁 Moving to {name}...")
            start_time = time.time()
            timeout = 120.0

            while time.time() - start_time < timeout:
                current_pos = pos_emu.current_position
                target_pos = pos_emu.waypoint_position

                if target_pos is None:
                    print(f" Reached {name}!")
                    break

                distance = pos_emu.calculate_distance(current_pos, target_pos)
                elapsed = time.time() - start_time

                print(
                    f"[{elapsed:5.1f}s] Current: {current_pos[0]:.6f}, {current_pos[1]:.6f}, {current_pos[2]:.1f}m | Distance: {distance:.2f}m"
                )

                # Send status to Mission Planner
                status_msg = f"HITL Moving to {name} - {distance:.1f}m remaining"
                self.controller.send_statustext_msg(status_msg)

                time.sleep(2.0)

            if pos_emu.waypoint_position is not None:
                print(f" Timeout reaching {name}")

            time.sleep(2.0)  # Pause between waypoints

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

            time.sleep(0.1)  # Small sleep

        print("\n Monitoring completed")

    def print_status_update(self) -> None:
        """Print current drone status and position."""
        try:
            elapsed_time = time.time() - self.test_start_time

            if self.controller.hitl_instance and self.controller.hitl_instance.position_emulator:
                pos_emu = self.controller.hitl_instance.position_emulator
                current_pos = pos_emu.current_position
                target_pos = pos_emu.target_position
                waypoint_pos = pos_emu.waypoint_position

                # Send status to Mission Planner
                status_msg = f"HITL Test - Lat:{current_pos[0]:.6f} Lon:{current_pos[1]:.6f} Alt:{current_pos[2]:.1f}m"
                self.controller.send_statustext_msg(status_msg)

                print(
                    f"[{elapsed_time:6.1f}s] HITL Position: {current_pos[0]:.6f}, {current_pos[1]:.6f}, {current_pos[2]:.1f}m"
                )
                print(
                    f"         Target: {target_pos[0]:.6f}, {target_pos[1]:.6f}, {target_pos[2]:.1f}m"
                )

                if waypoint_pos:
                    distance = pos_emu.calculate_distance(current_pos, waypoint_pos)
                    print(
                        f"         Waypoint: {waypoint_pos[0]:.6f}, {waypoint_pos[1]:.6f}, {waypoint_pos[2]:.1f}m (dist: {distance:.2f}m)"
                    )
                else:
                    print(f"         No active waypoint")

            # Get next waypoint info
            result, next_wp = self.controller.get_next_waypoint()
            if result and next_wp:
                print(
                    f"         Next WP: {next_wp.latitude:.6f}, {next_wp.longitude:.6f}, {next_wp.altitude:.1f}m"
                )

            # Get flight mode
            try:
                mode = (
                    self.controller.drone.mode.name
                    if hasattr(self.controller.drone, "mode")
                    else "Unknown"
                )
                armed = (
                    self.controller.drone.armed
                    if hasattr(self.controller.drone, "armed")
                    else False
                )
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

        # Connect to drone
        if not self.connect_to_drone():
            return 1

        # Wait for heartbeat
        if not self.wait_for_heartbeat():
            print("⚠️  Continuing without confirmed heartbeat...")

        self.test_manual_waypoints()  # Test manual waypoint movement

        # Step 5: Optional - Create and upload mission for Mission Planner visualization
        print("\n📋 Creating mission for Mission Planner visualization (optional)...")
        if self.create_test_mission():
            print("✅ Mission created successfully - you can see waypoints in Mission Planner")

        #  Monitor position updates
        self.monitor_position_updates(duration=120.0)  # 2 minutes

        return 0

    def cleanup(self) -> None:
        """Clean up resources."""
        if self.controller and hasattr(self.controller, "drone"):
            try:
                print("\n🧹 Cleaning up...")
                # Send final status message
                self.controller.send_statustext_msg("HITL Position Test Completed")
                time.sleep(1)
            except Exception as e:
                print(f"Cleanup warning: {e}")


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Test position emulator with 2 waypoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--connection",
        "-c",
        default="/dev/ttyAMA0",
        help="Connection string for the drone (default: /dev/ttyAMA0 for RPi+Pixhawk)",
    )

    parser.add_argument(
        "--duration",
        "-d",
        type=float,
        default=120.0,
        help="How long to monitor position updates in seconds (default: 120)",
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
