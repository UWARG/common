import sys
import time

import dronekit

from modules import flight_controller

DELAY_TIME = 10.0  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds

MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_LANDING_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_LANDING_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def upload_mission_to_drone(controller: "flight_controller.FlightController"):
    waypoints = [
        (42.3521, -71.0550, 10),
        (42.3601, -71.0589, 20),
        (42.3681, -71.0610, 30),
    ]

    # Clear existing mission
    controller.drone.commands.clear()

    # Add takeoff command to the mission
    takeoff_cmd = dronekit.Command(
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
    )
    controller.drone.commands.add(takeoff_cmd)

    # Add waypoints to the mission
    for waypoint in waypoints:
        cmd = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_TAKEOFF_FRAME,
            0,
            0,
            0,
            0,
            waypoint[0],
            waypoint[1],
            waypoint[2]
        )
        controller.drone.commands.add(cmd)

    # Add landing command to the mission
    landing_cmd = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_LANDING_FRAME,
        MAVLINK_LANDING_COMMAND,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    controller.drone.commands.add(landing_cmd)

    # Upload the mission to the vehicle
    controller.drone.commands.upload()


if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("failed")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    # Check mission completed returns empty and result is false if no mission is uploaded
    result, mission_is_completed = controller.get_mission_status_completed()
    assert result is False and mission_is_completed is None

    # Start Mission
    upload_mission_to_drone(controller)

    # Check mission completed returns not empty
    result, mission_is_completed = controller.get_mission_status_completed()
    assert mission_is_completed is not None

    # Check mission completed returns false
    assert mission_is_completed is False

    # Check mission completed returns false
    while mission_is_completed is False:
        time.sleep(1)
        status, retrieved = controller.get_mission_status_completed()

    # Check mission completed returns true
    assert mission_is_completed is True

    print("Done!")
