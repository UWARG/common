"""
Test for flight input device by printing to console.
"""
import time

from modules import flight_input_device


DELAY_TIME = 0.5
TCP_ADDRESS = 'tcp:127.0.0.1:14550'
if __name__ == "__main__":
    result, example_drone = flight_input_device.FlightInputDevice.create(TCP_ADDRESS)
    if not result: 
        print("failed")
        quit()

    for i in range(5):
        result, data = example_drone.get_odometry()
        if result:
            print("lat:" + " " + str(data.position.latitude))
            print("lon:" + " " + str(data.position.longitude))
            print("alt:" + " " + str(data.position.altitude))
            print("yaw:" + " " + str(data.orientation.yaw))
            print("roll:" + " " + str(data.orientation.roll))
            print("pitch:" + " " + str(data.orientation.pitch))
            print("")
        else: 
            print("failed")
        time.sleep(DELAY_TIME)

    print("Done!")
