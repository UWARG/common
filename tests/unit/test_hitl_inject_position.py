"""
Test on random coordinate injection into HITL by printing to console.
"""

import random

from modules.mavlink import flight_controller


MISSION_PLANNER_ADDRESS = "tcp:localhost:5762"


def main() -> int:
    """
    Main function.
    """
    result, controller = flight_controller.FlightController.create(
        MISSION_PLANNER_ADDRESS, 57600, True, True, False, None
    )
    if not result:
        print("Failed to create flight controller")
        return -1

    controller.set_flight_mode("AUTO")

    # Generate random coordinates
    latitude = random.uniform(43.0, 44.0)
    longitude = random.uniform(-81.0, -80.0)
    altitude = random.uniform(370.0, 380.0)

    controller.insert_waypoint(0, 40, -40, 300)
    controller.insert_waypoint(1, 50, -50, 300)
    controller.insert_waypoint(2, latitude, longitude, altitude)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
