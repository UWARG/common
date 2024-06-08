"""
Wrapper for socket operations.
"""

import socket
from enum import Enum


class NetworkProtocol(Enum):
    """
    Enum used to select protocol when instantiating Socket.
    """

    TCP = socket.SOCK_STREAM
    UDP = socket.SOCK_DGRAM


class Socket:
    """
    Wrapper for Python's socket module.
    """

    def __init__(self, socket_instance: socket.socket) -> None:
        """
        Parameters
        ----------
        instance: socket.socket
            For initializing Socket with an existing socket object.
        """
        self.__socket = socket_instance

    def send(self, data: bytes) -> bool:
        """
        Sends all data at once over the socket.

        Parameters
        ----------
        data: bytes

        Returns
        -------
        bool: If the data was sent successfully.
        """
        try:
            self.__socket.sendall(data)
        except socket.error as e:
            print(f"Could not send data: {e}.")
            return False

        return True

    def recv(self, buf_size: int) -> "tuple[bool, bytes | None]":
        """
        Reads buf_size bytes from the socket.

        Parameters
        ----------
        buf_size: int
            The number of bytes to receive.

        Returns
        -------
        tuple[bool, Socket | None]
            The first parameter represents if the read is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the data
              that is read.
        """
        try:
            data = self.__socket.recv(buf_size)
        except socket.error as e:
            print(f"Could not receive data: {e}.")
            return False, None

        return True, data

    def close(self) -> bool:
        """
        Closes the socket object. All future operations on the socket object will fail.

        Returns
        -------
        bool: If the socket was closed successfully.
        """
        try:
            self.__socket.close()
        except socket.error as e:
            print(f"Could not close socket: {e}.")
            return False

        return True

    def address(self) -> "tuple[str, int]":
        """
        Retrieves the address that the socket is listening on.

        Returns
        -------
        tuple[str, int]
            The address in the format (ip address, port).
        """
        return self.__socket.getsockname()

    def get_socket(self) -> socket.socket:
        """
        Getter for the underlying socket objet.
        """
        return self.__socket
