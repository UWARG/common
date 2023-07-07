from dronekit import connect 

class InputDevice: 

    def __init__(self, address: "str"):
        """
        address: tcp address (e.g. "tcp:127.0.0.1:14550")
        """
        self.vehicle = connect(address, wait_ready = True)
        assert (self.vehicle is not None)

    def get_data(self) -> "dict": 
        """
        For now since the only output is to odometry worker,
        will only get odometry data.
        """
        return