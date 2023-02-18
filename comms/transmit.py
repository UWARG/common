"""
Run transmit.py and receive.py together
"""

import time

from modules.generic_comms_device import GenericCommsDevice
from modules import helper


if __name__ == "__main__":
    sender = GenericCommsDevice("/dev/ttyUSB0", 115200)
    for i in range(0, 1000):
        msg = helper.message_picker(i)
        sender.transmit(msg)

        time.sleep(0.01)

        print(i)
