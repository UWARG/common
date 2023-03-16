from generic_comms_device import GenericCommsDevice
import TelemMessages

sender = GenericCommsDevice('/dev/ttyUSB0', 115200) 

msg = TelemMessages.GroundStationDisarm()
msg.arm = True 
sender.transmit(msg)
