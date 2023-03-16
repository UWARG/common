"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import TelemMessages.PIDValues

class PIDController(object):
    __slots__ = ["axes"]

    __typenames__ = ["TelemMessages.PIDValues"]

    __dimensions__ = [[6]]

    def __init__(self):
        self.axes = [ TelemMessages.PIDValues() for dim0 in range(6) ]

    def encode(self):
        buf = BytesIO()
        buf.write(PIDController._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        for i0 in range(6):
            assert self.axes[i0]._get_packed_fingerprint() == TelemMessages.PIDValues._get_packed_fingerprint()
            self.axes[i0]._encode_one(buf)

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != PIDController._get_packed_fingerprint():
            raise ValueError("Decode error")
        return PIDController._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = PIDController()
        self.axes = []
        for i0 in range(6):
            self.axes.append(TelemMessages.PIDValues._decode_one(buf))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if PIDController in parents: return 0
        newparents = parents + [PIDController]
        tmphash = (0x6178659769acf13e+ TelemMessages.PIDValues._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if PIDController._packed_fingerprint is None:
            PIDController._packed_fingerprint = struct.pack(">Q", PIDController._get_hash_recursive([]))
        return PIDController._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", PIDController._get_packed_fingerprint())[0]
