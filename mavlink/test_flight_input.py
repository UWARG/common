"""
Test for flight input device by printing to console.
"""
import time

from modules import flight_input_device


DELAY_TIME = 0.5
TCP_ADDRESS = 'tcp:127.0.0.1:14550'
if __name__ == "__main__":
    result, device = flight_input_device.FlightInputDevice.create(TCP_ADDRESS)
    if not result: 
        print("failed")
        quit()

    for i in range(5):
        result, odometry = device.get_odometry()
        if result:
            print("lat:" + " " + str(odometry.position.latitude))
            print("lon:" + " " + str(odometry.position.longitude))
            print("alt:" + " " + str(odometry.position.altitude))
            print("yaw:" + " " + str(odometry.orientation.yaw))
            print("roll:" + " " + str(odometry.orientation.roll))
            print("pitch:" + " " + str(odometry.orientation.pitch))
            print("")
        else: 
            print("failed")
        time.sleep(DELAY_TIME)

    print("Done!")
