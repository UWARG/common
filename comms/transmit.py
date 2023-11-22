"""
Run transmit.py and receive.py together.
"""
import time

from comms.modules.generic_comms_device import GenericCommsDevice
from comms.modules import helper


DEVICE = "/dev/ttyUSB0"


if __name__ == "__main__":
    sender = GenericCommsDevice(DEVICE, 115200)
    for i in range(0, 1000):
        msg = helper.message_picker(i)
        sender.transmit(msg)

        time.sleep(0.01)

        print(i)
