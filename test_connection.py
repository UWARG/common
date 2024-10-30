"""
Test for connection to flight controller by printing to console.
Verifies if the Rpi can send messages to the flight controller.
"""

from datetime import datetime
import pathlib
import time

from pymavlink import mavutil


DELAY_TIME = 1.0  # seconds
# /dev/ttyAMA0 for drone, tcp:127.0.0.1:14550 for mission planner simulator
CONNECTION_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds
LOG_FILE_PATH = pathlib.Path("logs", f"mavlink_connection_{time.time_ns()}.log")
DATETIME_FMT = "%Y-%m-%d_%H-%M-%S"


LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)


def req_msg(connection) -> bool:  # noqa: ANN001
    """
    Request the flight controller to send a non-existant message to the Rpi
    """

    message = connection.mav.command_long_encode(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,  # Confirmation
        3,  # Random message ID that doesn't exist
        0,
        0,
        0,
        0,
        0,
        0,
    )

    connection.mav.send(message)

    response = connection.recv_match(type="COMMAND_ACK", blocking=True, timeout=TIMEOUT)
    if response and response.command == 512:
        # print(response)
        # print(response.command)  # Seems to return 512 when the command doesn't exist
        return True

    return False


if __name__ == "__main__":
    vehicle = mavutil.mavlink_connection(CONNECTION_ADDRESS, baud=57600)
    while True:
        if req_msg(vehicle):
            print("CONNECTED, MESSAGE SENT TO PIXHAWK - Pixhawk recieved invalid command request")
            with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(f"{datetime.now().strftime(DATETIME_FMT)}  -  CONNECTED\n")
        else:
            print("DISCONNECTED, MESSAGE NOT RECIEVED - Pixhawk did not recieve any commands")
            with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(f"{datetime.now().strftime(DATETIME_FMT)}  -  DISCONNECTED\n")
        time.sleep(DELAY_TIME)
