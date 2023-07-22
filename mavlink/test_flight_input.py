"""
Test for flight input device by printing to console.
"""

from modules import flight_input_device
from time import sleep


if __name__ == "__main__":
    example_drone = flight_input_device.FlightInputDevice.create('tcp:127.0.0.1:14550')
    
    for i in range(5):
        data = example_drone[1].get_data()
        print("lat: " + str(data[1].position.latitude))
        print("lon: " + str(data[1].position.longitude))
        print("alt: " + str(data[1].position.altitude))
        print("yaw: " + str(data[1].orientation.yaw))
        print("roll: " + str(data[1].orientation.roll))
        print("pitch: " + str(data[1].orientation.pitch) + "\n")
        sleep(0.5)

    print("Done!")
