import time
from pymavlink import mavutil

CONNECTION_ADDRESS = "tcp:localhost:14550"  # Mission planner (GCS address)
DELAY = 1

# Default source_system is 255 (GCS)
# Default source_component is 0
vehicle = mavutil.mavlink_connection(CONNECTION_ADDRESS, source_system=255, source_component=0)

vehicle.wait_heartbeat()
print("connected")

while True:
    msg = vehicle.recv_match(type="STATUSTEXT", blocking=True)
    if not msg:
        print("no message")
    if msg.get_type() == "BAD_DATA":
        if mavutil.all_printable(msg.data):
            print(msg.data)
    else:
        # Message is valid
        # Use the attribute
        print(msg)
        print(msg.text)
    time.sleep(DELAY)
