"""
Test socket operations by sending images over client sockets.
"""

import struct
import threading
from pathlib import Path

import cv2
import pytest

from network.modules.image_encode import image_encode
from network.modules.socket_wrapper import ServerSocket, ClientSocket


IMAGE_PATH = Path(__file__).resolve().parent
SOCKET_ADDRESS = "127.0.0.1"
SOCKET_PORT = 8080


def recv_all(client_socket: ClientSocket, data_len: int) -> bytes:
    """
    Receives an image of data_len bytes from a socket
    """
    image_data = b""
    data_recv = 0
    while data_recv < data_len:
        result, data = client_socket.recv(data_len - data_recv)
        if not result:
            pytest.fail("Failed to receive image data.")

        print(f"Received {len(data)} bytes.")
        data_recv += len(data)
        image_data += data

    return image_data


def start_server(host: str, port: int) -> None:
    """
    Starts server listening on host:port that receives images and sends them back to the client.
    """
    result, server_socket = ServerSocket.create(host=host, port=port)   # pylint: disable=unpacking-non-sequence
    if not result:
        pytest.fail("Failed to create ServerSocket.")

    print(f"Listening on {host}:{port}.")

    result, client_socket = server_socket.accept()
    if not result:
        pytest.fail(f"Failed to accept connection from {host}:{port}.")

    if client_socket.address() != (host, port):
        pytest.fail(f"Accepted connection has wrong host and port. Expected: {host}:{port}.")

    print(f"Accepted connection from {host}:{port}.")

    while True:
        # Length of image in bytes
        result, data_len = client_socket.recv(4)
        if not result:
            pytest.fail("Failed to receive image byte length.")

        if not data_len:
            break

        print("Received image byte length from client.")
        data_len = struct.unpack("<I", data_len)
        print(f"image byte length: {data_len}")

        image_data = recv_all(client_socket, data_len[0])
        print("Received image data from client.")

        result = client_socket.send(image_data)
        if not result:
            pytest.fail("Failed to send image data back to client.")

        print("Sent image data back to client.")

    result = client_socket.close()
    if not result:
        pytest.fail("Failed to close client connection.")

    print("Connection to client closed.")

    result = server_socket.close()
    if not result:
        pytest.fail("Failed to close server socket.")


@pytest.fixture
def images() -> "list[bytes]":
    """
    Returns a list of images in byte representation.
    """
    return [
        image_encode(cv2.imread(str(IMAGE_PATH / "test_images/landing_pad_1.png")))[1],
        image_encode(cv2.imread(str(IMAGE_PATH / "test_images/landing_pad_2.png")))[1],
    ]


@pytest.fixture
def server(autouse=True):   # noqa: ANN001, ANN201 # pylint: disable=unused-argument
    """
    Starts server in a new thread.
    """
    server_thread = threading.Thread(
        target=start_server,
        args=(
            SOCKET_ADDRESS,
            SOCKET_PORT,
        ),
    )
    server_thread.start()
    yield
    server_thread.join()


def test(images: "list[bytes]") -> None:    # pylint: disable=redefined-outer-name
    """
    Client will send landing pad images to the server, and the server will send them back.
    """
    result, client_socket = ClientSocket.create(host=SOCKET_ADDRESS, port=SOCKET_PORT)  # pylint: disable=unpacking-non-sequence
    assert result, "Failed to create ClientSocket."
    print(f"Connected to: {SOCKET_ADDRESS}:{SOCKET_PORT}.")

    for image in images:
        # Send image byte length, 4 byte message
        data_len = struct.pack("<I", len(image))
        result = client_socket.send(data_len)
        assert result, "Failed to send image byte length."
        print("Sent image byte length to server.")

        result = client_socket.send(image)
        assert result, "Failed to send image data."
        print("Sent image data to server.")

        image_data = recv_all(client_socket, len(image))
        print("Received image data from server.")
        assert image == image_data, "Sent image bytes does not match received image bytes"

    result = client_socket.close()
    assert result, "Failed to close client connection."

    print("Connection to server closed.")
