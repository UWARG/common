import io
import libscrc
import serial
from helper import decode_msg 

class GenericCommsDevice():

    def __init__(self, port, baudrate):
        self.current_msg = io.BytesIO()
        self.length = -1
        self.ser = serial.Serial(port=port, baudrate=baudrate, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    def get_crc32(self, b):
        return libscrc.crc32(b)

    def transmit(self, msg):
        buf = io.BytesIO()
        msg._encode_one(buf)
        crc32 = self.get_crc32(buf.getbuffer().tobytes())
        msg.crc = crc32.to_bytes(4, 'big')
        buf = io.BytesIO()
        msg._encode_one(buf)
        self.ser.write(buf.getbuffer().tobytes())

    def receive(self):

        while self.ser.inWaiting(): 
            readByte = self.ser.read()[0]
            self.current_msg.write(readByte.to_bytes(1,'big'))
            
            if readByte == 0x7e:
                # start of new message
                lengthBytes = self.ser.read(size=2)
                self.length = int.from_bytes(lengthBytes, 'big')
                self.current_msg.write(lengthBytes)
            else:
                if len(self.current_msg.getbuffer()) == self.length + 8:
                    # check crc
                    raw_data = self.current_msg.getbuffer().tobytes()
                    calc_crc32 = self.get_crc32(raw_data[:-4])
                    msg_crc32 = int.from_bytes(raw_data[-4:],'big')
                    if msg_crc32 == calc_crc32:
                        if (raw_data[3] == 5):
                            self.current_msg.seek(0)
                            out = decode_msg(self.current_msg)
                            self.length = -1
                            self.current_msg = io.BytesIO()
                            return out
        return None
