"""
Test communication physically
"""

from py.generic_comms_device import GenericCommsDevice
from py import TelemMessages


if __name__ == "__main__":
    sender = GenericCommsDevice("/dev/ttyUSB0", 115200)
    receiver = GenericCommsDevice("/dev/ttyUSB0", 115200)
    for i in range(0, 1000):
        msg = TelemMessages.GroundStationDisarm()
        msg.arm = i % 2 == 0
        sender.transmit(msg)

        result, out = receiver.receive()
        if not result:
            continue

        print(type(out))
        print(out.header.type)
        print(i)
        print(out.arm)
