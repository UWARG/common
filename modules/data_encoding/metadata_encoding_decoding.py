"""
Encoding and Decoding Metadata
Save first byte as char to represent which worker sent the message
"""

import base64
import struct

from . import worker_enum


DATA_FORMAT = "=Bi"  # 1 unsigned char + 1 int = 5 bytes


def encode_metadata(
    worker_id: worker_enum.WorkerEnum, number_of_messages: int
) -> "tuple[True, bytes] | tuple[False, None]":
    """
    Encode PositionGlobal object into a C-style string for STATUSTEXT message.
    Worker_ID to be encoded as the first byte of the message.

    Parameters:
       worker_id: ID of the worker defined by its constant in WorkerEnum.
       number_of_messages: number of messages intended to be sent.

    Returns:
        packed_metadata (bytes): Encoded int corresponding to number of messages as bytes.
        First byte depends on which worker is calling the funciton, value depends on its corresponding enum value (see worker_enum.py)
    """
    try:
        # Ensure worker ID is in the WorkerEnum class
        if not isinstance(worker_id, worker_enum.WorkerEnum):
            return False, None

        # Encode message using PositionGlobal's latitude, longitude, altitude, with the worker ID in the front
        packed_metadata = struct.pack(
            DATA_FORMAT,
            worker_id.value,
            number_of_messages,
        )

        # Encode in base64 so it can be put into a string
        encoded_str = base64.b64encode(packed_metadata)
    except (struct.error, AttributeError, ValueError):
        return False, None

    return True, encoded_str


def decode_metadata(
    encoded_str: bytes,
) -> "tuple[True, worker_enum.WorkerEnum, int] | tuple[False, None, None]":
    """
    Decode bytes into a PositionGlobal object.

    Parameters:
        encoded_message (bytes): Encoded bytearray containing Worker message ID, number of messages sent.

    Returns:
        Tuple: success, WorkerEnum member instance corresponding to ID, number of messages received as an integer.
    """
    # Unpack the byte sequence
    try:
        # Decode base64
        encoded_metadata = base64.b64decode(encoded_str)

        # Ensure correct length (note the null terminator gets automatically dropped by STATUSTEXT)
        if len(encoded_metadata) != struct.calcsize(DATA_FORMAT):
            return False, None, None

        # unpack returns tuple (unsigned char,) so [0] is needed
        unpacked_data = struct.unpack(DATA_FORMAT, encoded_metadata)
        worker_id = worker_enum.WorkerEnum(unpacked_data[0])
        number_of_messages = unpacked_data[1]
    except struct.error:
        return False, None, None

    # Create and return a PositionGlobal object
    return True, worker_id, number_of_messages
