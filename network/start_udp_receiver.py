"""
Test socket operations by receiving images over server sockets.
"""

import sys
import struct

from network.modules.UDP.server_socket import UdpServerSocket


# Since the socket may be using either IPv4 or IPv6, do not specify 127.0.0.1 or ::1.
# Instead, use localhost if wanting to test on same the machine.
SOCKET_ADDRESS = ""
SOCKET_PORT = 8080


# pylint: disable=R0801
def start_server(host: str, port: int) -> int:
    """
    Starts server listening on host:port that receives some messages.
    """
    result, server_socket = UdpServerSocket.create(host=host, port=port)
    assert result, "Server cration failed."

    while True:
        result, data_len = server_socket.recv(4)
        if not result:
            print("Client closed the connection.")
            break

        print("Received data length from client.")

        data_len = struct.unpack("!I", data_len)
        print(f"data length: {data_len}")

        result, data = server_socket.recv(data_len[0])
        assert result, "Could not receive data from client."
        assert len(data) == data_len[0], "Data lengths not matching"
        print("Received data from client.")

    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        RESULT = start_server(SOCKET_ADDRESS, int(sys.argv[1]))
    else:
        RESULT = start_server(SOCKET_ADDRESS, SOCKET_PORT)
    if RESULT < 0:
        print(f"ERROR: Status code: {RESULT}")

    print("Done!")
