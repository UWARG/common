"""
Test communication physically
"""

from modules.generic_comms_device import GenericCommsDevice


if __name__ == "__main__":
    receiver = GenericCommsDevice("/dev/ttyUSB1", 115200)
    while True:
        result, out = receiver.receive()
        if not result:
            # print("false")
            continue

        print(type(out))
        print(out.header.type)
        print(out.arm)
