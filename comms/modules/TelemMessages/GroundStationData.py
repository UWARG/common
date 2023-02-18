"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

from .. import TelemMessages



class GroundStationData(object):
    __slots__ = ["header", "motor_outputs", "data", "battery_voltages", "controller_values"]

    def __init__(self):
        self.header = TelemMessages.Header()
        self.header.flag = 0x7e
        self.header.type = 0x7
        self.header.length = bytes([ 0x0, 0x69 ])
        self.motor_outputs = bytes(12)
        self.data = TelemMessages.SensorData()
        self.battery_voltages = bytes(13)
        self.controller_values = bytes(16)

    def encode(self):
        buf = BytesIO()
        buf.write(GroundStationData._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == TelemMessages.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        buf.write(bytearray(self.motor_outputs[:12]))
        assert self.data._get_packed_fingerprint() == TelemMessages.SensorData._get_packed_fingerprint()
        self.data._encode_one(buf)
        buf.write(bytearray(self.battery_voltages[:13]))
        buf.write(bytearray(self.controller_values[:16]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != GroundStationData._get_packed_fingerprint():
            raise ValueError("Decode error")
        return GroundStationData._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = GroundStationData()
        self.header = TelemMessages.Header._decode_one(buf)
        self.motor_outputs = buf.read(12)
        self.data = TelemMessages.SensorData._decode_one(buf)
        self.battery_voltages = buf.read(13)
        self.controller_values = buf.read(16)
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if GroundStationData in parents: return 0
        newparents = parents + [GroundStationData]
        tmphash = (0xe42b6068e6ac2d15+ TelemMessages.Header._get_hash_recursive(newparents)+ TelemMessages.SensorData._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if GroundStationData._packed_fingerprint is None:
            GroundStationData._packed_fingerprint = struct.pack(">Q", GroundStationData._get_hash_recursive([]))
        return GroundStationData._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

