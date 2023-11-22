"""
Test for flight input device by printing to console.
"""
import sys
import time

from mavlink.modules import flight_controller


DELAY_TIME = 0.5  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds


if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("failed")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    for i in range(5):
        result, odometry = controller.get_odometry()
        if result:
            print("lat: " + str(odometry.position.latitude))
            print("lon: " + str(odometry.position.longitude))
            print("alt: " + str(odometry.position.altitude))
            print("yaw: " + str(odometry.orientation.yaw))
            print("roll: " + str(odometry.orientation.roll))
            print("pitch: " + str(odometry.orientation.pitch))
            print("")
        else:
            print("failed")

        result, home = controller.get_home_location(TIMEOUT)
        if result:
            print("lat: " + str(home.latitude))
            print("lon: " + str(home.longitude))
            print("alt: " + str(home.altitude))

        time.sleep(DELAY_TIME)

    print("Done!")
