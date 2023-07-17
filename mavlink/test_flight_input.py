"""
Test for flight input device by printing to console
"""

import modules.flight_input_device

if __name__ == "__main__":
    example_drone = modules.flight_input_device.FlightInputDevice('tcp:127.0.0.1:14550')
    data = example_drone.get_data()
    print("lat: " + str(data.position.latitude))
    print("lon: " + str(data.position.longitude))
    print("alt: " + str(data.position.altitude))
    print("yaw: " + str(data.orientation.yaw))
    print("roll: " + str(data.orientation.roll))
    print("pitch: " + str(data.orientation.pitch))

