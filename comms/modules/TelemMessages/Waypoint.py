"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class Waypoint(object):
    __slots__ = ["latitude", "longitude", "altitude", "waypoint_id"]

    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.waypoint_id = 0

    def encode(self):
        buf = BytesIO()
        buf.write(Waypoint._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">dddB", self.latitude, self.longitude, self.altitude, self.waypoint_id))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != Waypoint._get_packed_fingerprint():
            raise ValueError("Decode error")
        return Waypoint._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = Waypoint()
        self.latitude, self.longitude, self.altitude, self.waypoint_id = struct.unpack(">dddB", buf.read(25))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if Waypoint in parents: return 0
        tmphash = (0x488b606b85e99f5b) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if Waypoint._packed_fingerprint is None:
            Waypoint._packed_fingerprint = struct.pack(">Q", Waypoint._get_hash_recursive([]))
        return Waypoint._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

