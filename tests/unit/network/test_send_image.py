"""
Integration test for image_encoding and network modules.
Encodes images then sends them to server through network sockets.
"""

import os
from pathlib import Path
import struct
from typing import Generator

import numpy as np
from PIL import Image
import pytest
from xprocess import ProcessStarter, XProcess

from modules.image_encoding import decoder
from modules.image_encoding import encoder
from modules.network.tcp.client_socket import TcpClientSocket
from modules.network.udp.client_socket import UdpClientSocket


# Since the socket may be using either IPv4 or IPv6, do not specify 127.0.0.1 or ::1.
# Instead, use localhost if wanting to test on same the machine
SERVER_PORT = 9145
ROOT_DIR = Path(__file__).parent


# TODO: This test is hangs. Disable for now.
pytestmark = pytest.mark.skipif(True, reason="This test is hangs. Disable for now.")


@pytest.fixture
def images() -> "Generator[np.ndarray]":
    """
    Images to send to server.
    """
    image_path = Path("tests", "unit", "image_encoding_images", "test.png")

    image = Image.open(image_path)
    image_bytes = [np.asarray(image)]

    yield image_bytes


# fmt: off
@pytest.fixture
def tcp_server(xprocess: XProcess) -> Generator:
    """
    Starts echo server.
    """

    myenv = os.environ.copy()
    myenv["PYTHONPATH"] = str(ROOT_DIR)
    myenv["PYTHONUNBUFFERED"] = "1"

    class Starter(ProcessStarter):
        """
        xprocess config to start a tcp echo server as another process.
        """

        pattern = f"Listening for external connections on port {SERVER_PORT}"
        timeout = 60
        args = ["python", "-m", "network.start_tcp_receiver", SERVER_PORT]
        env = myenv

    xprocess.ensure("tcp_sever", Starter)

    yield

    xprocess.getinfo("tcp_server").terminate()
# fmt: on


# pylint: disable=W0621,W0613
def test_tcp_client(images: "Generator[np.ndarray]", tcp_server: Generator) -> None:
    """
    Client will send images to the server, and the server will send them back.
    """

    result, client = TcpClientSocket.create(port=SERVER_PORT)
    assert result

    for image in images:
        # Encode image (into jpeg)
        data = encoder.encode(image)

        # Send image length, 4 byte message (unsigned int, network or big-endian format)
        data_len = struct.pack("!I", len(data))
        result = client.send(data_len)
        assert result

        # Send image to server
        result = client.send(data)
        assert result

        # Recive image back from echo server
        result, recv_data = client.recv(len(data))
        assert result

        # Decode image
        recv_image = decoder.decode(recv_data)
        assert image.shape == recv_image.shape


# fmt: off
@pytest.fixture
def udp_server(xprocess: XProcess) -> Generator:
    """
    Starts server.
    """

    myenv = os.environ.copy()
    myenv["PYTHONPATH"] = str(ROOT_DIR)
    myenv["PYTHONUNBUFFERED"] = "1"

    class Starter(ProcessStarter):
        """
        xprocess config to start a udp server as another process.
        """

        pattern = f"Listening for external data on port {SERVER_PORT + 1}"
        timeout = 60
        args = ["python", "-m", "network.start_udp_receiver", SERVER_PORT + 1]
        env = myenv

    xprocess.ensure("udp_sever", Starter)

    yield

    xprocess.getinfo("udp_server").terminate()
# fmt: on


# pylint: disable=W0621,W0613
def test_udp_client(images: "Generator[bytes]", udp_server: Generator) -> None:
    """
    Client will send image to the server.
    We do not know whether they have been received successfully or not, since these are UDP packets
    """

    result, client = UdpClientSocket.create(port=SERVER_PORT + 1)
    assert result

    for image in images:
        # Encode image
        data = encoder.encode(image)

        # Send data length, 4 byte message (unsigned int, network or big-endian format)
        data_len = struct.pack("!I", len(data))
        result = client.send(data_len)
        assert result

        # Send image to server
        result = client.send(data)
        assert result
