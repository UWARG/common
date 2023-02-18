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



class JetsonOdometryData(object):
    __slots__ = ["header", "sensorData"]

    def __init__(self):
        self.header = TelemMessages.Header()
        self.header.flag = 0x7e
        self.header.type = 0x0
        self.header.length = bytes([ 0x0, 0x40 ])
        self.sensorData = TelemMessages.SensorData()

    def encode(self):
        buf = BytesIO()
        buf.write(JetsonOdometryData._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == TelemMessages.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        assert self.sensorData._get_packed_fingerprint() == TelemMessages.SensorData._get_packed_fingerprint()
        self.sensorData._encode_one(buf)

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != JetsonOdometryData._get_packed_fingerprint():
            raise ValueError("Decode error")
        return JetsonOdometryData._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = JetsonOdometryData()
        self.header = TelemMessages.Header._decode_one(buf)
        self.sensorData = TelemMessages.SensorData._decode_one(buf)
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if JetsonOdometryData in parents: return 0
        newparents = parents + [JetsonOdometryData]
        tmphash = (0x7b2e33dc32fcc162+ TelemMessages.Header._get_hash_recursive(newparents)+ TelemMessages.SensorData._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if JetsonOdometryData._packed_fingerprint is None:
            JetsonOdometryData._packed_fingerprint = struct.pack(">Q", JetsonOdometryData._get_hash_recursive([]))
        return JetsonOdometryData._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

