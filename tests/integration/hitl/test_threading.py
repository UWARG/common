"""
Tests the threading behavior of the HITL module (gps and camera modules).
"""

PIXHAWK_ADDRESS = "tcp:localhost:5762"

import os
import time
from modules.mavlink import flight_controller

def main() -> int:
    """
    Main function.
    """
    images_folder_path = os.path.join("tests", "integration", "camera_emulator", "images")

    result, controller = flight_controller.FlightController.create(
        PIXHAWK_ADDRESS, 57600, True, True # True, images_folder_path
    )
    if not result:
        print("Failed to create flight controller")
        return -1

    time.sleep(1)

    controller.set_flight_mode("AUTO")

    controller.insert_waypoint(0, 40, -40, 300)

    time.sleep(10)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
