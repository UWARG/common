from generic_comms_device import GenericCommsDevice
import TelemMessages

if __name__ == "__main__":
    sender = GenericCommsDevice('/dev/ttyUSB0', 115200) 
    receiver = GenericCommsDevice('/dev/ttyUSB1', 115200)
    index = 0
    msg = TelemMessages.GroundStationDisarm()
    msg.arm = True
    sender.transmit(msg)
    while True:
        out = receiver.receive()
        if out != None:
            print(type(out))
            print(index)
            index  = index + 1
            msg = TelemMessages.GroundStationDisarm()
            msg.arm = True
            sender.transmit(msg)