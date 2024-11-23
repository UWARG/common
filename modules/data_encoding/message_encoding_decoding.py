"""
Encoding and Decoding Global Positions
"""

import struct
from .. import position_global


# For Floats
def encode_position_global(global_position: position_global.PositionGlobal) -> bytes:
    """
    Encode PositionGlobal object into Bytes

    Parameters:
       global_position: PositionGlobal object

    Returns:
        packed_coordinates (bytes): Encoded latitude, longitude, altitude of PositionGlobal object as bytes.
    """

    # Encode message using PositionGlobal's latitude, longitude, altitude
    packed_coordinates = struct.pack(
        "ddd",
        global_position.latitude,
        global_position.longitude,
        global_position.altitude,  # 3 double-precision floats
    )

    return packed_coordinates


def decode_bytes_to_position_global(
    encoded_global_position: bytes,
) -> position_global.PositionGlobal:
    """
    Decode bytes into a PositionGlobal object.

    Parameters:
        encoded_message (bytes): Encoded bytearray containing latitude, longitude, altitude

    Returns:
        PositionGlobal: Decoded PositionGlobal object.
    """

    # check to make sure encoded message is 3 double precision floats
    if len(encoded_global_position) != 24:  # 3 double precision floats * 8 bytes for each float
        raise ValueError("Invalid byte sequence length. Expected 24 bytes.")

    # Unpack the byte sequence
    latitude, longitude, altitude = struct.unpack("ddd", encoded_global_position)

    # Create and return a PositionGlobal object
    success, position = position_global.PositionGlobal.create(latitude, longitude, altitude)
    if not success:
        raise ValueError("Failed to create PositionGlobal object.")

    return position
