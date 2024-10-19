"""
Test for connection to flight controller by printing to console.
Verifies if the Rpi can send messages to the flight controller.
"""

import time

from pymavlink import mavutil


DELAY_TIME = 1.0  # seconds
CONNECTION_ADDRESS = "tcp:127.0.0.1:14550"  # /dev/ttyAMA0 for drone, tcp:127.0.0.1:14550 for mission planner simulator
TIMEOUT = 1.0  # seconds


def req_msg(connection) -> bool:
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
        0
    )

    connection.mav.send(message)

    response = connection.recv_match(type="COMMAND_ACK", blocking=True, timeout=TIMEOUT)
    if response and response.command == 512:
        # print(response)
        # print(response.command)  # Seems to return 512 when the command doesn't exist
        return True
    
    return False

if __name__ == "__main__":
    connection = mavutil.mavlink_connection(CONNECTION_ADDRESS, baud=57600)
    while True:
        if req_msg(connection):
            print("CONNECTED, MESSAGE SENT TO PIXHAWK - Pixhawk recieved invalid command request")
        else:
            print("DISCONNECTED, MESSAGE NOT RECIEVED - Pixhawk did not recieve any commands")
        time.sleep(DELAY_TIME)
