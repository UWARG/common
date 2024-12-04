"""
Test for drone's destination at final waypoint by uploading mission and monitoring it.
"""

import time

from pymavlink import mavutil

from modules import position_global_relative_altitude
from modules.mavlink import dronekit
from modules.mavlink import flight_controller


DELAY_TIME = 1.0  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds

MAVLINK_TAKEOFF_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_TAKEOFF_COMMAND = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

ALTITUDE = 10  # metres
ACCEPT_RADIUS = 10  # metres


# TODO: This function is to be removed when Dronekit-Python interfaces are
# moved from pathing repository.
def upload_mission(
    controller: flight_controller.FlightController,
    waypoints: list[position_global_relative_altitude.PositionGlobalRelativeAltitude],
) -> bool:
    """
    Add a takeoff command and waypoint following commands to the drone's
    command sequence, and upload them.

    controller: Flight controller.
    waypoints: List of waypoints.

    Return: If the mission is successfully uploaded or not.
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
    for waypoint in waypoints:
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
            waypoint.latitude,
            waypoint.longitude,
            waypoint.relative_altitude,
        )

        controller.drone.commands.add(command)

    # Upload the mission to the drone
    try:
        controller.drone.commands.upload()
    except dronekit.TimeoutError:
        return False

    print("Mission uploaded.")

    return True


def main() -> int:
    """
    Main function.
    """
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Failed to create flight controller.")
        return -1

    # Get Pylance to stop complaining
    assert controller is not None

    # List of waypoints for the drone to travel
    result, waypoint_1 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        43.4731, -80.5419, ALTITUDE
    )
    if not result:
        print("Failed to create waypoint.")
        return -1

    # Get Pylance to stop complaining
    assert waypoint_1 is not None

    result, waypoint_2 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        43.4723, -80.5380, ALTITUDE
    )
    if not result:
        print("Failed to create waypoint.")
        return -1

    # Get Pylance to stop complaining
    assert waypoint_2 is not None

    result, waypoint_3 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        43.4735, -80.5371, ALTITUDE
    )
    if not result:
        print("Failed to create waypoint.")
        return -1

    # Get Pylance to stop complaining
    assert waypoint_3 is not None

    result, waypoint_4 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        43.4743, -80.5400, ALTITUDE
    )
    if not result:
        print("Failed to create waypoint.")
        return -1

    # Get Pylance to stop complaining
    assert waypoint_4 is not None

    waypoints = [waypoint_1, waypoint_2, waypoint_3, waypoint_4]

    # Upload mission
    result = upload_mission(controller, waypoints)
    if not result:
        print("Failed to upload mission.")
        return -1

    while True:
        result, is_drone_destination_final_waypoint = (
            controller.is_drone_destination_final_waypoint()
        )
        if not result:
            print("Failed to get if the drone's destination is the final waypoint.")
            return -1

        # Get Pylance to stop complaining
        assert is_drone_destination_final_waypoint is not None

        if is_drone_destination_final_waypoint:
            break

        print("Drone's destination is not final waypoint.")

        time.sleep(DELAY_TIME)

    print("Drone's destination is final waypoint.")
    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
