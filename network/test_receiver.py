"""
Test socket operations by receiving images over server sockets.
"""

import struct

from network.modules.server_socket import ClientSocket, ServerSocket


SOCKET_ADDRESS = "127.0.0.1"
SOCKET_PORT = 8080


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


def start_server(host: str, port: int) -> int:
    """
    Starts server listening on host:port that receives images and sends them back to the client.
    """
    result, server_socket = ServerSocket.create(  # pylint: disable=unpacking-non-sequence
        host=host, port=port
    )
    if not result:
        return -1

    print(f"Listening on {host}:{port}.")

    result, client_socket = server_socket.accept()
    if not result:
        return -2

    if client_socket.address() != (host, port):
        return -3

    print(f"Accepted connection from {host}:{port}.")

    while True:
        # Length of image in bytes
        result, data_len = client_socket.recv(4)
        if not result:
            return -4

        if not data_len:
            break

        print("Received image byte length from client.")
        data_len = struct.unpack("<I", data_len)
        print(f"image byte length: {data_len}")

        result, image_data = recv_all(client_socket, data_len[0])
        if not result:
            return -5
        print("Received image data from client.")

        result = client_socket.send(image_data)
        if not result:
            return -6

        print("Sent image data back to client.")

    result = client_socket.close()
    if not result:
        return -7

    print("Connection to client closed.")

    result = server_socket.close()
    if not result:
        return -8

    return 0


if __name__ == "__main__":
    result = start_server(SOCKET_ADDRESS, SOCKET_PORT)
    if result < 0:
        print(f"ERROR: Status code: {result}")

    print("Done!")
