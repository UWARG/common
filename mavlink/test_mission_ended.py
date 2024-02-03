import sys
import time

import dronekit

from modules import flight_controller

DELAY_TIME = 10.0  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds

MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

ALTITUDE = 10
ACCEPT_RADIUS = 10


def upload_mission(
        waypoints: "list[tuple[float, float, float]]",
        controller: "flight_controller.FlightController",
) -> bool:
    # Clear existing mission
    controller.drone.commands.download()
    controller.drone.commands.wait_ready()
    controller.drone.commands.clear()

    # Add takeoff command to the mission
    takeoff_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_TAKEOFF_FRAME,
        MAVLINK_TAKEOFF_COMMAND,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        ALTITUDE,
    )

    controller.drone.commands.add(takeoff_command)

    # Add waypoints to the mission
    for point in waypoints:
        command = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_FRAME,
            MAVLINK_COMMAND,
            0,
            0,
            0,
            ACCEPT_RADIUS,
            0,
            0,
            point[0],
            point[1],
            point[2],
        )

        controller.drone.commands.add(command)

    # Upload the mission to the drone
    controller.drone.commands.upload()


if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("failed")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    # Set the home location of the drone to E5
    # Set extra command line to `--home=43.472978,-80.540103,336,0`
    waypoints = [
        (43.4731, -80.5419, ALTITUDE),
        (43.4723, -80.5380, ALTITUDE),
        (43.4735, -80.5371, ALTITUDE),
        (43.4743, -80.5400, ALTITUDE),
    ]

    # Upload Mission
    upload_mission(waypoints, controller)

    result, drone_is_approaching_final_waypoint = controller.drone_travelling_to_final_waypoint()

    while not drone_is_approaching_final_waypoint:
        time.sleep(1)
        result, drone_is_approaching_final_waypoint = controller.drone_travelling_to_final_waypoint()

    print("Done")
