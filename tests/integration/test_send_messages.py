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

    messages = [
        "System startup",  # Regular message (success)
        "A" * 50,  # Exactly 50 characters (success)
        "B" * 51,  # 51 characters (fail)
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
