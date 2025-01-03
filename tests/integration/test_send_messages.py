"""
Test script to send messages to the drone using the FlightController class.
"""

import time

from pymavlink import mavutil

from modules.mavlink.flight_controller import FlightController


DELAY_TIME = 0.5  # seconds
MISSION_PLANNER_ADDRESS = "tcp:localhost:5672"


def main() -> int:
    """
    Main function.
    """
    # Connect to the vehicle
    success, controller = FlightController.create(MISSION_PLANNER_ADDRESS)
    if not success:
        print("Failed to connect")
        return -1

    messages = [  # 10 random messages
        "System startup",
        "Initializing sensors",
        "GPS lock acquired",
        "Motors armed",
        "Taking off",
        "Reaching altitude",
        "Mission started",
        "Waypoint reached",
        "Returning home",
        "Landing sequence initiated",
    ]

    for msg in messages:
        controller.send_statustext_msg(msg, mavutil.mavlink.MAV_SEVERITY_INFO)
        time.sleep(DELAY_TIME)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
