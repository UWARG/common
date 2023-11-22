"""
Test communication physically.
"""
import time

from comms.modules.generic_comms_device import GenericCommsDevice
from comms.modules import helper


DEVICE_SENDER = "/dev/ttyUSB0"
DEVICE_RECEIVER = "/dev/ttyUSB1"


if __name__ == "__main__":
    sender = GenericCommsDevice(DEVICE_SENDER, 115200)
    receiver = GenericCommsDevice(DEVICE_RECEIVER, 115200)
    for i in range(0, 10):
        msg = helper.message_picker(i)
        sender.transmit(msg)

        time.sleep(0.01)

        result, out = receiver.receive()
        if not result:
            print("Failed")
            print(i)
            continue

        print(type(out))
        print(out.header.type)
        print(i)
