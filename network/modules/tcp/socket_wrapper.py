"""
Wrapper for a TCP socket.
"""

import socket


class TcpSocket:
    """
    Wrapper for a TCP socket.
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
        tuple[bool, bytes | None]
            The first parameter represents if the read is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the data that is read.
        """

        chunks = []
        bytes_recd = 0
        while bytes_recd < buf_size:
            # 4096 or other low powers of 2 is recommended
            # Although while testing without a limit, it has been observed to reach above 100000
            chunk = self.__socket.recv(min(buf_size - bytes_recd, 4096))

            if chunk == b"":
                print("Socket connection broken")  # When 0 is received, means error
                return False, None

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        return True, b"".join(chunks)

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
