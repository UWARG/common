"""
Test socket operations by sending images over client sockets.
"""

import struct
from pathlib import Path
import numpy as np

from network.modules.TCP.client_socket import TcpClientSocket


IMAGE_PATH = Path(__file__).resolve().parent
SOCKET_ADDRESS = "localhost"
SOCKET_PORT = 8080


IMAGE_ENCODE_EXT = ".png"


def start_sender(host: str, port: int) -> int:
    """
    Client will send landing pad images to the server, and the server will send them back.
    """

    test_messages = [
        b"Hello world!",
        np.random.bytes(4096),
        np.random.bytes(10000000),
    ]

    result, client_socket = TcpClientSocket.create(host=host, port=port)
    assert result, "Failed to create ClientSocket."
    print(f"Connected to: {host}:{port}.")

    for data in test_messages:
        # Send data length, 4 byte message (unsigned int, network or big-endian format)
        data_len = struct.pack("!I", len(data))
        result = client_socket.send(data_len)
        assert result, "Failed to send data byte length."
        print("Sent data byte length to server.")

        result = client_socket.send(data)
        assert result, "Failed to send data."
        print("Sent data to server.")

        result, recv_data = client_socket.recv(len(data))
        assert result, "Failed to receive returning data."
        print("Received data from server.")
        assert data == recv_data, "Sent data does not match received data"
        print("Received data is same as sent data, no corruption has occured.")

    result = client_socket.close()
    assert result, "Failed to close client connection."

    print("Connection to server closed.")
    return 0


if __name__ == "__main__":
    RESULT = start_sender(SOCKET_ADDRESS, SOCKET_PORT)
    if RESULT < 0:
        print(f"ERROR: Status code: {RESULT}")

    print("Done!")
