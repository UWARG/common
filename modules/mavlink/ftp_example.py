"""
Groundside scripts to receive GPS location messages
"""

import struct
import sys
from enum import Enum
from pymavlink import mavutil

# connection params
CONNECTION_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 5.0
DELAY_TIME = 1.0

# file path to read from
# 1. start up connection on mission planner
# 2. mavlink and establish write tcp connection
# 3. config menu -> MAVFtp -> simulation drone file paths
FILE_PATH = b"/@ROMFS/locations.txt"
SEQ_NUM = 0


class Opcode(Enum):
    """
    Opcodes for FTP commands
    """

    NONE = 0
    TERMINATE_SESSION = 1
    RESET_SESSION = 2
    LIST_DIRECTORY = 3
    OPEN_FILE_RO = 4
    READ_FILE = 5
    CREATE_FILE = 6
    WRITE_FILE = 7
    REMOVE_FILE = 8
    CREATE_DIRECTORY = 9
    REMOVE_DIRECTORY = 10
    OPEN_FILE_WO = 11
    TRUNCATE_FILE = 12
    RENAME = 13
    CALC_FILE_CRC32 = 14
    BURST_READ_FILE = 15
    # ERROR responses
    ACK_RESPONSE = 128
    NAK_RESPONSE = 129


class NakErrorCode(Enum):
    """
    Error codes for FTP commands
    """

    NONE = 0  # No Error
    FAIL = 1  # Unknown failure
    FAIL_ERRNO = 2  # Command failed, Err number sent back in PayloadHeader.data[1]
    INVALID_DATA_SIZE = 3  # Payload size is invalid
    INVALID_SESSION = 4  # Session is not currently open
    NO_SESSIONS_AVAILABLE = 5  # All available sessions are in use
    EOF = 6  # Offset past end of file for ListDirectory and ReadFile commands
    UNKNOWN_CMD = 7  # Unknown command / Opcode
    FILE_EXISTS = 8  # File/Directory already exists
    FILE_PROTECTED = 9  # File/Directory is write protected
    FILE_NOT_FOUND = 10  # File/Directory is not found


def send_ftp_command(
    connection: mavutil.mavlink_connection,
    seq_num: int,
    opcode: int,
    req_opcode: int,
    session: int,
    offset: int,
    size: int,
    payload: bytes,
) -> None:
    """
    Send an FTP command to the vehicle.

    Args:
        connection (mavutil.mavlink_connection): MAVLink connection object.
        session (int): Session ID. | index 2 | range 0-255.
        opcode (int): FTP command opcode | index 3 | range 0-255.
        size (int): Size of the payload. | index 4 | range 0-255.
        req_opcode (int): Requested opcode. | index 5 | range 0-255.
        offset (int): Offset in the file. | index 8-11.
        payload (bytes): Payload data. | index 12-251.
    """
    ftp_payload = bytearray(251)  # ftp payload size

    # packing payload in file system
    ftp_payload[0:2] = struct.pack("<H", seq_num)
    ftp_payload[2] = session
    ftp_payload[3] = opcode
    ftp_payload[4] = size
    ftp_payload[5] = req_opcode
    ftp_payload[6] = 0  # burst_complete
    ftp_payload[7] = 0  # padding
    ftp_payload[8:12] = struct.pack("<I", offset)
    ftp_payload[12 : 12 + len(payload)] = payload

    connection.mav.file_transfer_protocol_send(
        target_network=0,
        target_system=connection.target_system,
        target_component=connection.target_component,
        payload=ftp_payload,
    )


vehicle = mavutil.mavlink_connection(CONNECTION_ADDRESS, baud=57600)
vehicle.wait_heartbeat()
print("heartbeat received")
if vehicle:
    print("CONNECTED...")
else:
    print("DISCONNECTED...")

# open file for reading session
send_ftp_command(
    vehicle,
    seq_num=SEQ_NUM,
    opcode=Opcode.OPEN_FILE_RO.value,
    req_opcode=Opcode.NONE.value,
    session=0,
    offset=0,
    size=len(FILE_PATH),
    payload=FILE_PATH,
)
SEQ_NUM += 1
response = vehicle.recv_match(type="FILE_TRANSFER_PROTOCOL", blocking=True, timeout=TIMEOUT)

if response is None:
    print("NO RESPONSE RECEIVED")
    # sys.exit()

response_payload = bytes(response.payload)
if response_payload[3] != Opcode.ACK_RESPONSE.value:  # Check for error - NAK Response
    error_code = response_payload[12]
    error_message = NakErrorCode(error_code).name
    print("ERROR CODE:", {error_code}, "ERROR MESSAGE:", {error_message})
    sys.exit()

print("FILE OPENED: ")

# retrieve session id, file size, and sequence number from ACK response
SESSION_ID = response_payload[2]
DATA_OFFSET = struct.unpack("<I", response_payload[8:12])[0]
FILE_SIZE = struct.unpack("<I", response_payload[12 : 12 + response_payload[4]])[0]
CHUNK_SIZE = 239  # Max data size per chunk
FILE_DATA = b""
SEQ_NUM = struct.unpack("<H", response_payload[0:2])[0]

# read file in chunks
while DATA_OFFSET < FILE_SIZE:
    send_ftp_command(
        vehicle,
        seq_num=SEQ_NUM,
        opcode=Opcode.READ_FILE.value,
        req_opcode=Opcode.NONE.value,
        session=SESSION_ID,
        offset=DATA_OFFSET,
        size=CHUNK_SIZE,
        payload=b"",
    )
    SEQ_NUM += 1
    response = vehicle.recv_match(type="FILE_TRANSFER_PROTOCOL", blocking=True, timeout=TIMEOUT)

    if response is None:
        print("ERROR: NO RESPONSE RECEIVED")
        break

    response_payload = bytes(response.payload)
    if response_payload[3] != Opcode.ACK_RESPONSE.value:
        error_code = response_payload[12]
        error_message = NakErrorCode(error_code).name
        print("ERROR CODE:", {error_code}, "ERROR MESSAGE:", {error_message})
        break

    chunk_data = response_payload[12 : 12 + response_payload[4]]
    FILE_DATA += chunk_data
    DATA_OFFSET += len(chunk_data)

    print(chunk_data.decode("utf-8", errors="ignore"), end="")

    # Send the next read command while waiting for the current response
    if DATA_OFFSET < FILE_SIZE:
        send_ftp_command(
            vehicle,
            seq_num=SEQ_NUM,
            opcode=Opcode.READ_FILE.value,
            req_opcode=Opcode.NONE.value,
            session=SESSION_ID,
            offset=DATA_OFFSET,
            size=CHUNK_SIZE,
            payload=b"",
        )
        SEQ_NUM += 1

# Terminate read session
send_ftp_command(
    vehicle,
    seq_num=SEQ_NUM,
    opcode=Opcode.TERMINATE_SESSION.value,
    req_opcode=Opcode.NONE.value,
    session=SESSION_ID,
    offset=0,
    size=0,
    payload=b"",
)

print("\nEND OF FILE")
