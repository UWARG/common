"""
Encoding and Decoding Global Positions
Save first byte as char to represent which worker sent the message 
"""

import base64
import struct

from .. import position_global
from . import worker_enum


DATA_FORMAT = "=Bddd"  # 1 unsigned char + 3 doubles = 25 bytes


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
        if not isinstance(
            worker_id, worker_enum.WorkerEnum
        ):  # If worker ID is not in the Enum Class
            return False, None

        # Encode message using PositionGlobal's latitude, longitude, altitude, with the worker ID in the front
        packed_coordinates = struct.pack(
            DATA_FORMAT,
            worker_id.value,
            global_position.latitude,
            global_position.longitude,
            global_position.altitude,
        )

        # Encode in base64 so it can be put into a string
        encoded_str = base64.b64encode(packed_coordinates)
    except (struct.error, AttributeError, ValueError):
        return False, None

    return True, encoded_str


def decode_bytes_to_position_global(
    encoded_str: bytes,
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
        # Decode base64
        encoded_global_position = base64.b64decode(encoded_str)

        # Ensure corect length
        if len(encoded_global_position) != struct.calcsize(DATA_FORMAT):
            return False, None, None

        # Decode position global
        unpacked_data = struct.unpack(DATA_FORMAT, encoded_global_position)
        worker_id = worker_enum.WorkerEnum(unpacked_data[0])
        latitude, longitude, altitude = unpacked_data[1], unpacked_data[2], unpacked_data[3]
    except struct.error:
        return False, None, None

    # Create and return a PositionGlobal object
    success, position = position_global.PositionGlobal.create(latitude, longitude, altitude)
    return success, worker_id, position
