import serial
import time
import TelemMessages
from generic_comms_device import GenericCommsDevice

sender = GenericCommsDevice('/dev/ttyUSB0', 115200) 

while True:
    msg = TelemMessages.GroundStationData()
    msg.data.altitude = 5.0
    print("sending data")
    sender.transmit(msg)
    time.sleep(0.1)