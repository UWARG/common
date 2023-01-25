from GenericCommsDevice import GenericCommsDevice
import TelemMessages

if __name__ == "__main__":
    dev = GenericCommsDevice('/dev/ttyUSB0', 115200) 

    msg = TelemMessages.GroundStationDisarm()
    msg.arm = True
    dev.transmit(msg)