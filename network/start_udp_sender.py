"""
Test UDP socket operations by sending images over client sockets.
"""

import struct

import numpy as np

from .modules.udp.client_socket import UdpClientSocket


SOCKET_ADDRESS = "localhost"
SOCKET_PORT = 8080


IMAGE_ENCODE_EXT = ".png"


def start_sender(host: str, port: int) -> int:
    """
    Client will send some test data (random bytes) to server.
    """

    test_messages = [
        b"Hello world!",
        np.random.bytes(4096),
        np.random.bytes(10000000),
    ]

    result, client_socket = UdpClientSocket.create(host=host, port=port)
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

    return 0


if __name__ == "__main__":
    RESULT = start_sender(SOCKET_ADDRESS, SOCKET_PORT)
    if RESULT < 0:
        print(f"ERROR: Status code: {RESULT}")

    print("Done!")
