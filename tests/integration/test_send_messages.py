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

    valid_messages = [  # 10 random valid messages
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

    invalid_messages = [  # 10 random invalid messages over 50 characters
        "Warning: The current altitude exceeds the safe operating limit by a significant margin.",
        "Critical error detected in navigation system — immediate manual override recommended.",
        "Battery voltage has dropped below the minimum threshold required for safe flight operations.",
        "GPS signal lost; attempting to reacquire connection. Flight path stability compromised.",
        "Obstacle detected in the projected flight path. Automatic avoidance maneuver failed.",
        "Telemetry link unstable. Real-time data transmission may be delayed or incomplete.",
        "Motor synchronization fault detected. Recommend performing pre-flight diagnostics.",
        "Excessive wind speeds detected at current altitude. Adjusting flight parameters.",
        "Payload imbalance identified. Autonomous compensation may affect flight stability.",
        "Firmware mismatch between flight controller and companion computer detected.",
    ]

    for msg in valid_messages:
        controller.send_statustext_msg(msg, mavutil.mavlink.MAV_SEVERITY_INFO)
        time.sleep(DELAY_TIME)

    for msg in invalid_messages:
        controller.send_statustext_msg(msg, mavutil.mavlink.MAV_SEVERITY_INFO)
        time.sleep(DELAY_TIME)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
