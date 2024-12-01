import time
from pymavlink import mavutil

CONNECTION_ADDRESS = "tcp:localhost:5762"  # Drone (simulated drone/pixhawk address)
DELAY = 1

# Default source_system is 255 (GCS), so we change it to 1 (Drone)
# Default source_component is 0
vehicle = mavutil.mavlink_connection(CONNECTION_ADDRESS, source_system=1, source_component=0)

vehicle.wait_heartbeat()
print("connected")
counter = 0

while True:
    counter += 1
    vehicle.mav.statustext_send(mavutil.mavlink.MAV_SEVERITY_INFO, f"helloworld {counter}".encode("utf-8"))
    print("sent statustext")
    time.sleep(DELAY)
