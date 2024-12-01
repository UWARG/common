"""
Groundside scripts to receive GPS location messages
"""

import struct
import sys
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
        opcode (int): FTP command opcode.
        req_opcode (int): Requested opcode.
        session (int): Session ID.
        offset (int): Offset in the file.
        size (int): Size of the payload.
        payload (bytes): Payload data.
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
    opcode=4,
    req_opcode=0,
    session=0,
    offset=0,
    size=len(FILE_PATH),
    payload=FILE_PATH,
)
SEQ_NUM += 1
response = vehicle.recv_match(type="FILE_TRANSFER_PROTOCOL", blocking=True, timeout=TIMEOUT)

if response is None:
    print("NO RESPONSE RECEIVED")
    sys.exit()

response_payload = bytes(response.payload)
if response_payload[3] != 128:  # Check for error - NAK Response
    print("ERROR RECEIVED")
    print("ERROR CODE: ", response_payload[12])
    sys.exit()

print("FILE OPENED: ")

# retrieve session id, file size, and sequence number from ACK response
SESSION_ID = response_payload[2]
DATA_OFFSET = struct.unpack("<I", response_payload[8:12])[0]
FILE_SIZE = struct.unpack("<I", response_payload[12 : 12 + response_payload[4]])[0]
SEQ_NUM = struct.unpack("<H", response_payload[0:2])[0]
CHUNK_SIZE = 239  # Max data size per chunk
FILE_DATA = b""

# read file in chunks
while DATA_OFFSET < FILE_SIZE:
    send_ftp_command(
        vehicle,
        seq_num=SEQ_NUM,
        opcode=5,
        req_opcode=0,
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
    if response_payload[3] != 128:
        print("ERROR CODE: ", response_payload[12])
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
            opcode=5,
            req_opcode=0,
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
    opcode=1,
    req_opcode=0,
    session=SESSION_ID,
    offset=0,
    size=0,
    payload=b"",
)
print("\nEND OF FILE")
