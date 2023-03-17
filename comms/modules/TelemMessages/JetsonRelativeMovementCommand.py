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

class JetsonRelativeMovementCommand(object):
    __slots__ = ["header", "ID", "x", "y", "z", "heading"]

    __typenames__ = ["TelemMessages.Header", "byte", "float", "float", "float", "float"]

    __dimensions__ = [None, None, None, None, None, None]

    def __init__(self):
        self.header = TelemMessages.Header()
        self.header.flag = 0x7e
        self.header.type = 0x2
        self.header.length = bytes([ 0x0, 0x11 ])
        self.ID = 0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.heading = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(JetsonRelativeMovementCommand._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == TelemMessages.Header._get_packed_fingerprint()
        self.header._encode_one(buf)
        buf.write(struct.pack(">Bffff", self.ID, self.x, self.y, self.z, self.heading))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != JetsonRelativeMovementCommand._get_packed_fingerprint():
            raise ValueError("Decode error")
        return JetsonRelativeMovementCommand._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = JetsonRelativeMovementCommand()
        self.header = TelemMessages.Header._decode_one(buf)
        self.ID, self.x, self.y, self.z, self.heading = struct.unpack(">Bffff", buf.read(17))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if JetsonRelativeMovementCommand in parents: return 0
        newparents = parents + [JetsonRelativeMovementCommand]
        tmphash = (0xaf32ebf569830f07+ TelemMessages.Header._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if JetsonRelativeMovementCommand._packed_fingerprint is None:
            JetsonRelativeMovementCommand._packed_fingerprint = struct.pack(">Q", JetsonRelativeMovementCommand._get_hash_recursive([]))
        return JetsonRelativeMovementCommand._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", JetsonRelativeMovementCommand._get_packed_fingerprint())[0]

