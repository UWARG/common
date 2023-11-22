"""
Run transmit.py and receive.py together.
"""
import time

from comms.modules.generic_comms_device import GenericCommsDevice


DEVICE = "/dev/ttyUSB1"


if __name__ == "__main__":
    receiver = GenericCommsDevice(DEVICE, 115200)
    while True:
        time.sleep(0.01)

        result, out = receiver.receive()
        if not result:
            print("Failure")
            continue

        print(type(out))
        print(out.header.type)
