"""
Test for connection to flight input device by printing to console.
"""

import time

from pymavlink import mavutil

from .modules import flight_controller
from .modules import drone_odometry

DELAY_TIME = 1.0  # seconds
CONNECTION_ADDRESS = "tcp:127.0.0.1:14550"  # /dev/ttyAMA0 for drone, tcp:127.0.0.1:14550 for mission planner simulator
TIMEOUT = 1.0  # seconds

def check_heartbeats():
    connection = mavutil.mavlink_connection(CONNECTION_ADDRESS, baud=57600)

    while True:
        message = connection.wait_heartbeat(timeout=TIMEOUT)
        if message:
            print(f"Heartbeat from system (system {connection.target_system} component {connection.target_component})")
        else:
            print("Did not recieve a heartbeat")
        connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
        time.sleep(DELAY_TIME)

def main2():
    result, fc = flight_controller.FlightController.create(CONNECTION_ADDRESS)
    counter = 0
    check1 = True
    check2 = True
    while True:
        if counter % 2 == 0:
            result = fc.set_flight_mode("AUTO")
            time.sleep(0.5)
            result, flight_mode = fc.get_flight_mode()
            if check1 and result and flight_mode == drone_odometry.FlightMode.MOVING:
                print("Pixhawk recieved flightmode change message")
                check2 = True
            else:
                print("Pixhawk is not reciving flightmode change message")
                check2 = False
                check1 = True
        else:
            result = fc.set_flight_mode("LOITER")
            time.sleep(0.5)
            result, flight_mode = fc.get_flight_mode()
            if check2 and result and flight_mode == drone_odometry.FlightMode.STOPPED:
                print("Pixhawk recieved flightmode change message")
                check1 = True
            else:
                print("Pixhawk is not reciving flightmode change message")
                check1 = False
                check2 = True

        counter += 1
        time.sleep(DELAY_TIME)

if __name__ == "__main__":
    main2()
