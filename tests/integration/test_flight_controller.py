"""
Test for flight input device by printing to console.
"""

import time

from modules.mavlink import flight_controller


DELAY_TIME = 0.5  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
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
            print("lat: " + str(odometry.position.latitude))
            print("lon: " + str(odometry.position.longitude))
            print("alt: " + str(odometry.position.altitude))
            print("yaw: " + str(odometry.orientation.yaw))
            print("roll: " + str(odometry.orientation.roll))
            print("pitch: " + str(odometry.orientation.pitch))
            print("")
        else:
            print("Failed to get odometry")

        result, home = controller.get_home_location(TIMEOUT)
        if result:
            print("lat: " + str(home.latitude))
            print("lon: " + str(home.longitude))
            print("alt: " + str(home.altitude))
        else:
            print("Failed to get home location")

        time.sleep(DELAY_TIME)

    # Download and print commands
    success, commands = controller.download_commands()
    if success:
        print("Downloaded commands:")
        for command in commands:
            print(command)
    else:
        print("Failed to download commands.")

    result, next_waypoint = controller.get_next_waypoint()
    if result:
        print("next waypoint lat: " + str(next_waypoint.latitude))
        print("next waypoint lon: " + str(next_waypoint.longitude))
        print("next waypoint alt: " + str(next_waypoint.altitude))
    else:
        print("Failed to get next waypoint.")

    result, home = controller.get_home_location(TIMEOUT)
    if not result:
        print("Failed to get home location")
        return -1

    # Create and add land command
    result = controller.upload_land_command(home.latitude, home.longitude)
    if not result:
        print("Could not upload land command.")
        return -1

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
