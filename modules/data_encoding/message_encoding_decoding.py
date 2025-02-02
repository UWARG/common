"""
Encoding and Decoding Global Positions
Save first byte as char to represent which worker sent the message 
"""

import struct

from .. import position_global
from . import worker_enum


def encode_position_global(
    worker_id: worker_enum.WorkerEnum, global_position: position_global.PositionGlobal
) -> "tuple[True, bytes] | tuple[False, None]":
    """
    Encode PositionGlobal object into Bytes. Worker_ID to be encoded as the first byte of the message

    Parameters:
       worker_id: ID of the worker defined by its constant in WorkerEnum
       global_position: PositionGlobal object

    Returns:
        packed_coordinates (bytes): Encoded latitude, longitude, altitude of PositionGlobal object as bytes.
        First byte dependant on which worker is calling the funciton, value depends on its corresponding enum value.
    """
    try:
        if not worker_id:  # If worker ID is not in the Enum Class
            return False, None

        # Encode message using PositionGlobal's latitude, longitude, altitude, with the worker ID in the front
        packed_coordinates = struct.pack(
            "=Bddd",
            worker_id.value,  # 1 byte (char)
            global_position.latitude,
            global_position.longitude,
            global_position.altitude,  # 3 double-precision floats
        )
    except (struct.error, AttributeError, ValueError):
        return False, None

    return True, packed_coordinates


def decode_bytes_to_position_global(
    encoded_global_position: bytes,
) -> (
    "tuple[True, worker_enum.WorkerEnum, position_global.PositionGlobal] | tuple[False, None, None]"
):
    """
    Decode bytes into a PositionGlobal object.

    Parameters:
        encoded_message (bytes): Encoded bytearray containing latitude, longitude, altitude

    Returns:
        Tuple: success, WorkerEnum class corresponding to ID, PositionGlobal: Decoded PositionGlobal object.
    """
    # Unpack the byte sequence
    try:
        if len(encoded_global_position) != struct.calcsize(
            "=Bddd"
        ):  # should equal 25: 1 char (1 byte) and 3 double precision floats (3 * 8 bytes)
            return False, None, None

        worker_id = worker_enum.WorkerEnum(struct.unpack("B", encoded_global_position[:1])[0])
        latitude, longitude, altitude = struct.unpack("ddd", encoded_global_position[1:])
    except struct.error:
        return False, None, None

    # Create and return a PositionGlobal object
    success, position = position_global.PositionGlobal.create(latitude, longitude, altitude)
    return success, worker_id, position
