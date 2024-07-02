"""
Test socket operations by receiving images over server sockets.
"""

import struct

from network.modules.TCP.server_socket import TcpServerSocket


# Since the socket may be using either IPv4 or IPv6, do not specify 127.0.0.1 or ::1.
# Instead, use localhost if wanting to test on same the machine.
SOCKET_ADDRESS = ""
SOCKET_PORT = 8080


def start_server(host: str, port: int) -> int:
    """
    Starts server listening on host:port that receives images and sends them back to the client.
    """
    result, server_socket = TcpServerSocket.create(host=host, port=port)
    assert result, "Server cration failed."

    while True:
        result, data_len = server_socket.recv(4)
        if not result:
            print("Client closed the connection.")
            break

        print("Received data length from client.")

        data_len = struct.unpack("!I", data_len)
        print(f"data length: {data_len}")

        result, image_data = server_socket.recv(data_len[0])
        assert result, "Could not receive data from client."
        print("Received data from client.")

        result = server_socket.send(image_data)
        assert result, "Failed to send data back to client."
        print("Sent data back to client.")

    result = server_socket.close()
    assert result, "Failed to close connection"

    print("Connection to client closed.")

    return 0


if __name__ == "__main__":
    RESULT = start_server(SOCKET_ADDRESS, SOCKET_PORT)
    if RESULT < 0:
        print(f"ERROR: Status code: {RESULT}")

    print("Done!")
