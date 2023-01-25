import libscrc
import io
import TelemMessages
import serial
from helper import decodeMsg 


def printBytes(b):
    for i in b:
        print(hex(i))


class GenericCommsDevice():

    def __init__(self, port, baudrate):
        print(port)
        self.current_msg = io.BytesIO()
        self.length = -1
        self.ser = serial.Serial(port=port, baudrate=baudrate, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

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
        self.ser.write(buf.getbuffer().tobytes())

    def receive(self):

        while self.ser.inWaiting(): 
            readByte = self.ser.read()[0]
            print(hex(readByte))
            self.current_msg.write(readByte.to_bytes(1,'big'))
            print("current length " + str(self.current_msg.getbuffer().nbytes))
            
            if readByte == 0x7e:
                # start of new message
                lengthBytes = self.ser.read(size=2)
                self.length = int.from_bytes(lengthBytes, 'big')
                print("length " + str(self.length))
                self.current_msg.write(lengthBytes)
            else:
                if len(self.current_msg.getbuffer()) == self.length + 8:
                    # entire message has been written
                    print("got the entire thing")
                    printBytes(self.current_msg.getbuffer().tobytes())

                    # check crc

                    raw_data = self.current_msg.getbuffer().tobytes()
                    calc_crc32 = self.getCRC32(raw_data[:-4])
                    msg_crc32 = int.from_bytes(raw_data[-4:],'big')
                    print(calc_crc32)
                    print(msg_crc32)
                    if msg_crc32 == calc_crc32:
                        if (raw_data[3] == 5):
                            self.current_msg.seek(0)
                            out = decodeMsg(self.current_msg)
                            self.length = -1
                            self.current_msg = io.BytesIO()
                            return out
        return None

                        # convert to class

                        # return class
                    
        # print("no bytes left in buffer")

dev = GenericCommsDevice('/dev/ttyUSB1', 115200) 

if __name__ == "__main__":
    index = 0
    while True:
        out = dev.receive()
        if out != None:
            print("index = " + str(index))
            print(type(out))
            index = index + 1
        