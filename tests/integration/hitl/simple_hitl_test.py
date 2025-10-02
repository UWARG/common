#!/usr/bin/env python3
import argparse
import time
import sys
from modules.mavlink import flight_controller

BAUD_RATE = 57600
MOVEMENT_SPEED = 5.0
DEFAULT_HOME_LAT = 43.43405014107003
DEFAULT_HOME_LON = -80.57898027451816
DEFAULT_HOME_ALT = 373.0


def main() -> int:
    print(f"Home Position: {DEFAULT_HOME_LAT:.6f}, {DEFAULT_HOME_LON:.6f}, {DEFAULT_HOME_ALT}m")
    print()
    
    print("Connecting to drone with HITL position emulation...")
    try:
        result, controller = flight_controller.FlightController.create(
            address="/dev/ttyAMA0",
            baud=BAUD_RATE,
            hitl_enabled=True,
            position_module=True,
            camera_module=False,
            images_path=None,
            movement_speed=MOVEMENT_SPEED
        )
        
        if not result or controller is None:
            print("Failed to create flight controller")
            return 1
            
        print("Successfully connected to drone with HITL position emulation")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return 1
    
    print("\n🛰️ Initializing GPS position...")
    if controller.hitl_instance and controller.hitl_instance.position_emulator:
        pos_emu = controller.hitl_instance.position_emulator
        print(f"Injecting initial GPS position: {DEFAULT_HOME_LAT:.6f}, {DEFAULT_HOME_LON:.6f}, {DEFAULT_HOME_ALT}m")
        pos_emu.inject_position(DEFAULT_HOME_LAT, DEFAULT_HOME_LON, DEFAULT_HOME_ALT)
        time.sleep(2.0)
        print(" GPS position initialized")
    else:
        print(" Position emulator not available")

    try:
        last_status_time = 0
        status_interval = 5.0
        
        while True:
            current_time = time.time()
            if current_time - last_status_time >= status_interval:
                print_status(controller)
                last_status_time = current_time
            
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("\n\n Stopping HITL Position Emulator...")
        return 0
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        return 1
    finally:
        cleanup(controller)


def print_status(controller) -> None:
    try:
        # Try to get odometry
        result, odometry = controller.get_odometry()
        if result and odometry:
            lat = odometry.position.latitude
            lon = odometry.position.longitude
            alt = odometry.position.altitude
            print(f"Position: {lat:.6f}, {lon:.6f}, {alt:.1f}m")
            
            # Send status to Mission Planner
            controller.send_statustext_msg(f"HITL: {lat:.6f}, {lon:.6f}, {alt:.1f}m")
        else:
            print(" Waiting for GPS data to become available...")
            
            # Check position emulator status
            if controller.hitl_instance and controller.hitl_instance.position_emulator:
                pos_emu = controller.hitl_instance.position_emulator
                current_pos = pos_emu.current_position
                print(f"   Emulator Position: {current_pos[0]:.6f}, {current_pos[1]:.6f}, {current_pos[2]:.1f}m")
                controller.send_statustext_msg("HITL: GPS initializing...")
        try:
            mode = controller.drone.mode.name if hasattr(controller.drone, 'mode') else "Unknown"
            armed = controller.drone.armed if hasattr(controller.drone, 'armed') else False
            print(f"   Mode: {mode}, Armed: {armed}")
        except Exception:
            print("   Mode: Unknown, Armed: Unknown")
            
    except Exception as e:
        print(f"Status error: {e}")


def cleanup(controller) -> None:
    """Clean up resources."""
    try:
        print("🧹 Cleaning up...")
        if controller and hasattr(controller, 'drone'):
            controller.send_statustext_msg("HITL Position Emulator Stopped")
            time.sleep(1)
    except Exception as e:
        print(f"Cleanup warning: {e}")


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")
    
    print("Done!")
