"""
Encoding and Decoding Metadata
Save first byte as char to represent which worker sent the message 
"""

import struct

from . import worker_enum


def encode_metadata(
    worker_id: worker_enum.WorkerEnum, number_of_messages: int
) -> "tuple[True, bytes] | tuple[False, None]":
    """
    Encode PositionGlobal object into Bytes. Worker_ID to be encoded as the first byte of the message

    Parameters:
       worker_id: ID of the worker defined by its constant in WorkerEnum
       number_of_messages: number of messages intended to be sent

    Returns:
        packed_coordinates (bytes): Encoded int corresponding to number of messages as bytes.
        First byte dependant on which worker is calling the funciton, value depends on its corresponding enum value (see worker_enum.py)
    """
    try:
        if not worker_id:  # If worker ID is not in the Enum Class
            return False, None

        # Encode message using PositionGlobal's latitude, longitude, altitude, with the worker ID in the front
        packed_metadata = struct.pack(
            "=Bi",
            worker_id.value,  # 1 byte (char)
            number_of_messages,  # 4 bytes
            # 5 bytes total
        )
    except (struct.error, AttributeError, ValueError):
        return False, None

    return True, packed_metadata


def decode_metadata(
    encoded_metadata: bytes,
) -> "tuple[True, worker_enum.WorkerEnum, int] | tuple[False, None, None]":
    """
    Decode bytes into a PositionGlobal object.

    Parameters:
        encoded_message (bytes): Encoded bytearray containing Worker message ID, number of messages sent

    Returns:
        Tuple: success, WorkerEnum member instance corresponding to ID, number of messages received as an integer
    """
    # Unpack the byte sequence
    try:
        if len(encoded_metadata) != struct.calcsize(
            "=Bi"
        ):  # should equal 5 bytes: 1 unsigned char + 1 int
            return False, None, None

        worker_id = struct.unpack("B", encoded_metadata[:1])[
            0
        ]  # unpack returns tuple (unsigned char,) so [0] is needed
        number_of_messages = struct.unpack("i", encoded_metadata[1:])[0]
    except struct.error:
        return False, None, None

    # Create and return a PositionGlobal object
    return True, worker_enum.WorkerEnum(worker_id), number_of_messages
