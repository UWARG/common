"""
Test socket operations by sending images over client sockets.
"""

import struct
from pathlib import Path

import cv2
import numpy as np

from network.modules.TCP.client_socket import TcpClientSocket


IMAGE_PATH = Path(__file__).resolve().parent
SOCKET_ADDRESS = "localhost"
SOCKET_PORT = 8080


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


def start_sender(host: str, port: int) -> int:
    """
    Client will send landing pad images to the server, and the server will send them back.
    """
    result, client_socket = TcpClientSocket.create(host=host, port=port)
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

        result, image_data = client_socket.recv(len(image))
        assert result, "Failed to receive returning image data."
        print("Received image data from server.")
        assert image == image_data, "Sent image bytes does not match received image bytes"
        print("Received data is same as sent data, no corruption has occured.")

    result = client_socket.close()
    assert result, "Failed to close client connection."

    print("Connection to server closed.")
    return 0


if __name__ == "__main__":
    result = start_sender(SOCKET_ADDRESS, SOCKET_PORT)
    if result < 0:
        print(f"ERROR: Status code: {result}")

    print("Done!")
