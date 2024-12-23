"""
Test script to send messages to the drone using the FlightController class.
"""

import time
import sys

from pymavlink import mavutil

from modules.mavlink.flight_controller import FlightController

# Connect to the vehicle
success, controller = FlightController.create("tcp:localhost:5672")
if not success:
    print("Failed to connect")
    sys.exit(1)


messages = [  # 10 random messages
    "System startup",
    "Initializing sensors",
    "GPS lock acquired",
    "Motors armed",
    "Taking off",
    "Reaching altitude",
    "Mission started",
    "Waypoint reached",
    "Returning home",
    "Landing sequence initiated",
]

for msg in messages:
    controller.send_statustext_msg(msg, mavutil.mavlink.MAV_SEVERITY_INFO)
    time.sleep(1)  # Wait 1 second between messages
