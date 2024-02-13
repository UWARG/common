"""
Test for drone's destination at final waypoint by uploading mission and monitoring it.
"""
import sys
import time

import dronekit

from mavlink.modules import flight_controller


DELAY_TIME = 1.0  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds

MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

ALTITUDE = 10  # metres
ACCEPT_RADIUS = 10  # metres


# TODO: This function is to be removed when Dronekit-Python interfaces are
# moved from pathing repository.
def upload_mission(controller: flight_controller.FlightController,
                   waypoints: "list[tuple[float, float, float]]") -> bool:
    """
    Add a takeoff command and waypoint following commands to the drone's
    command sequence, and upload them.

    Parameters
    ----------
    controller: "flight_controller.FlightController"
    waypoints: "list[tuple[float, float, float]]"

    Returns
    -------
    bool
    """
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
    try:
        controller.drone.commands.upload()
        return True
    except dronekit.TimeoutError:
        return False


if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Failed to create flight controller.")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    # List of waypoints for the drone to travel
    waypoints = [
        (43.4731, -80.5419, ALTITUDE),
        (43.4723, -80.5380, ALTITUDE),
        (43.4735, -80.5371, ALTITUDE),
        (43.4743, -80.5400, ALTITUDE),
    ]

    # Upload mission
    result = upload_mission(controller, waypoints)
    if not result:
        print("Failed to upload mission.")
        sys.exit()

    while True:
        result, is_drone_destination_final_waypoint \
            = controller.is_drone_destination_final_waypoint()
        if not result:
            print("Failed to get if the drone's destination is the final waypoint.")
            sys.exit()

        # Get Pylance to stop complaining
        assert is_drone_destination_final_waypoint is not None

        if is_drone_destination_final_waypoint:
            break

        print("Drone's destination is not final waypoint.")

        time.sleep(DELAY_TIME)

    print("Drone's destination is final waypoint.")
    print("Done!")
