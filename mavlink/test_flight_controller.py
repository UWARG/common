"""
Test for flight input device by printing to console.
"""
import sys
import time

import dronekit

from modules import flight_controller


ALTITUDE = 40  # metres
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

    commands = []

    result, home = controller.get_home_location(TIMEOUT)

    # Create and add go-to waypoint command
    commands.append(
        dronekit.Command(
            0,
            0,
            0,
            dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            0,
            0,  # param1
            10,
            0,
            0,
            home.latitude,
            home.longitude,
            ALTITUDE,
        )
    )

    # Create and add land command
    land_command = controller.create_land_command(home.latitude, home.longitude)
    commands.append(land_command)

    controller.write_mission(commands)

    print("Done!")
