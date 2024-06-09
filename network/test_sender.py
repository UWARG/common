"""
Test socket operations by sending images over client sockets.
"""

import struct
from pathlib import Path

import cv2
import numpy as np

from network.modules.server_socket import ClientSocket


IMAGE_PATH = Path(__file__).resolve().parent
SOCKET_ADDRESS = "127.0.0.1"
SOCKET_PORT = 5000 


IMAGE_ENCODE_EXT = ".png"


def get_images() -> "list[bytes]":
    """
    Returns a list of images in byte representation.
    """
    return [
        image_encode(cv2.imread(str(IMAGE_PATH / "test_images/landing_pad_1.png")))[1],
        image_encode(cv2.imread(str(IMAGE_PATH / "test_images/landing_pad_2.png")))[1],
    ]


def image_encode(image: "np.ndarray") -> "tuple[bool, bytes | None]":
    """
    Encodes an image (np.ndarray as an RGB matrix) and returns its byte sequence.
    """
    result, encoded_image = cv2.imencode(IMAGE_ENCODE_EXT, image)
    if not result:
        return False, None

    encoded_image_bytes = encoded_image.tobytes()

    return True, encoded_image_bytes


def recv_all(client_socket: ClientSocket, data_len: int) -> "tuple[bool, bytes | None]":
    """
    Receives an image of data_len bytes from a socket
    """
    image_data = b""
    data_recv = 0
    while data_recv < data_len:
        result, data = client_socket.recv(data_len - data_recv)
        if not result:
            return False, None

        print(f"Received {len(data)} bytes.")
        data_recv += len(data)
        image_data += data

    return True, image_data


def start_sender(host: str, port: int):
    """
    Client will send landing pad images to the server, and the server will send them back.
    """
    result, client_socket = ClientSocket.create(  # pylint: disable=unpacking-non-sequence
        host=host, port=port
    )
    assert result, "Failed to create ClientSocket."
    print(f"Connected to: {host}:{port}.")

    for image in get_images():
        # Send image byte length, 4 byte message
        data_len = struct.pack("<I", len(image))
        result = client_socket.send(data_len)
        assert result, "Failed to send image byte length."
        print("Sent image byte length to server.")

        result = client_socket.send(image)
        assert result, "Failed to send image data."
        print("Sent image data to server.")

        recv_all(client_socket, len(image))
        print("Received image data from server.")

    result = client_socket.close()
    assert result, "Failed to close client connection."

    print("Connection to server closed.")



if __name__ == "__main__":
    result = start_sender(SOCKET_ADDRESS, SOCKET_PORT)

    print("Done!")