"""
Test communication physically
"""

import time

from modules.generic_comms_device import GenericCommsDevice
from modules import helper


if __name__ == "__main__":
    sender = GenericCommsDevice("/dev/ttyUSB0", 115200)
    receiver = GenericCommsDevice("/dev/ttyUSB1", 115200)
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
