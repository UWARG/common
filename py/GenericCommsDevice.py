import libscrc
import io
import TelemMessages


def printBytes(b):
    for i in b:
        print(hex(i))


class GenericCommsDevice():

    def __init__(self, port, baudrate):
        print(port)
        # self.ser = serial.Serial(port=port, baudrate=baudrate, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    def getCRC32(self, b):
        return libscrc.crc32(b)

    def transmit(self, msg):
        buf = io.BytesIO()
        #msg.crc = bytes([0,0,0,0])
        msg._encode_one(buf)
        crc32 = self.getCRC32(buf.getbuffer().tobytes())
        msg.crc = crc32.to_bytes(4, 'big')
        buf = io.BytesIO()
        msg._encode_one(buf)
        printBytes(buf.getbuffer().tobytes())
        ser.write(buf.read())
    # def recieve():
        
    #     readByte = rfd.read()
    #     if readByte == 0x7e:
    #         # start of new message
            
    #     self.currentMessage.append(readByte)


dev = GenericCommsDevice('/dev/ttyACM0', 115200) 

msg = TelemMessages.GroundStationDisarm()
msg.arm = True
dev.transmit(msg)
        