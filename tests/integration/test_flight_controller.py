"""
Test for flight input device by printing to console.
"""

import time

from modules.mavlink import flight_controller


DELAY_TIME = 0.5  # seconds
MISSION_PLANNER_ADDRESS = "tcp:localhost:5762"
TIMEOUT = 1.0  # seconds


def main() -> int:
    """
    Main function.
    """
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Failed to open flight controller")
        return -1

    # Get Pylance to stop complaining
    assert controller is not None

    for _ in range(5):
        result, odometry = controller.get_odometry()
        if result:
            controller.send_statustext_msg("lat: " + str(odometry.position.latitude))
            controller.send_statustext_msg("lat: " + str(odometry.position.latitude))
            controller.send_statustext_msg("lon: " + str(odometry.position.longitude))
            controller.send_statustext_msg("alt: " + str(odometry.position.altitude))
            controller.send_statustext_msg("yaw: " + str(odometry.orientation.yaw))
            controller.send_statustext_msg("roll: " + str(odometry.orientation.roll))
            controller.send_statustext_msg("pitch: " + str(odometry.orientation.pitch))
            controller.send_statustext_msg("")
        else:
            print("Failed to get odometry")

        result, home = controller.get_home_position(TIMEOUT)
        if result:
            controller.send_statustext_msg("lat: " + str(home.latitude))
            controller.send_statustext_msg("lon: " + str(home.longitude))
            controller.send_statustext_msg("alt: " + str(home.altitude))
        else:
            print("Failed to get home position")

        time.sleep(DELAY_TIME)

    # Download and print commands
    success, commands = controller.download_commands()
    if success:
        print("Downloaded commands:")
        for command in commands:
            print(str(command))
    else:
        print("Failed to download commands.")

    result, next_waypoint = controller.get_next_waypoint()
    if result:
        controller.send_statustext_msg("next waypoint lat: " + str(next_waypoint.latitude))
        controller.send_statustext_msg("next waypoint lon: " + str(next_waypoint.longitude))
        controller.send_statustext_msg("next waypoint alt: " + str(next_waypoint.altitude))
    else:
        print("Failed to get next waypoint.")

    result, home = controller.get_home_position(TIMEOUT)
    if not result:
        print("Failed to get home position")
        return -1

    # Create and add land command
    result = controller.upload_land_command(home.latitude, home.longitude)
    if not result:
        print("Could not upload land command.")
        return -1

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
