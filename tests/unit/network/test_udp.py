"""
Test UDP sockets by sending random data to a server (for Pytest).
"""

import os
from pathlib import Path
import struct
from typing import Generator

import numpy as np
import pytest
from xprocess import ProcessStarter, XProcess

from modules.network.udp.client_socket import UdpClientSocket


# Since the socket may be using either IPv4 or IPv6, do not specify 127.0.0.1 or ::1.
# Instead, use localhost if wanting to test on same the machine.
SERVER_PORT = 8825
ROOT_DIR = Path(__file__).parent.parent


# TODO: This file requires a server so it is not a unit test!
pytestmark = pytest.mark.skipif(
    True, reason="This file requires a server so it is not a unit test!"
)


@pytest.fixture
def test_messages() -> "Generator[bytes]":
    """
    Test messages to send to server.
    """

    yield [
        b"Hello world!",
        np.random.bytes(4096),
        np.random.bytes(10000000),
    ]


# fmt: off
@pytest.fixture
def myserver(xprocess: XProcess) -> Generator:
    """
    Starts server.
    """

    myenv = os.environ.copy()
    myenv["PYTHONPATH"] = str(ROOT_DIR)
    myenv["PYTHONUNBUFFERED"] = "1"

    class Starter(ProcessStarter):
        """
        xprocess config to start the server as another process.
        """

        pattern = f"Listening for external data on port {SERVER_PORT}"
        timeout = 60
        args = ["python", "-m", "network.start_udp_receiver", SERVER_PORT]
        env = myenv

    xprocess.ensure("mysever", Starter)

    yield

    xprocess.getinfo("myserver").terminate()
# fmt: on


# pylint: disable=W0621,W0613
def test_client(test_messages: "Generator[bytes]", myserver: Generator) -> None:
    """
    Client will send messages to the server.
    We do not know whether they have been received successfully or not, since these are UDP packets
    """

    result, client = UdpClientSocket.create(port=SERVER_PORT)
    assert result

    for data in test_messages:
        # Send data length, 4 byte message (unsigned int, network or big-endian format)
        data_len = struct.pack("!I", len(data))
        result = client.send(data_len)
        assert result

        result = client.send(data)
        assert result
