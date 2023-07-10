from modules.flight_input_device import InputDevice

if __name__ == "__main__":
    example_drone = InputDevice('tcp:127.0.0.1:14550')
    print(example_drone.get_data()) 

