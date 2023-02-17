from modules.generic_comms_device import GenericCommsDevice
from modules import TelemMessages
import time


if __name__ == "__main__":
    sender = GenericCommsDevice("/dev/ttyUSB0", 115200)
    for i in range(0, 1):
        # msg = TelemMessages.GroundStationData()
        msg = TelemMessages.GroundStationDisarm()
        # msg.data.altitude = 5.0
        # print("length of batt array", len(msg.battery_voltages))
        # msg.arm = i % 2 == 0
        sender.transmit(msg)
        msg_crc32 = int.from_bytes(msg.crc, 'big')
        print(msg_crc32)
        time.sleep(1)

        print(i)
        # print(msg.arm)