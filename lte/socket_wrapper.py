"""
Wrapper for socket operations.
"""

import socket

class Socket:
    """
    Wrapper for Pyton's socket module.
    """
    __create_key = object()

    @classmethod
    def create(
        cls,
        host: str,
        port: int,
        create_max_attemps: int,
        connect_max_attempts: int
    ) -> "tuple[bool, Socket | None]":
        """
        Establishes connection to drone through provided host and port.

        Parameters
        ----------
        host: str (e.g. localhost or 127.0.0.1)
        port: int (e.g. 5000)
            The host combined with the port will form an address (e.g. localhost:5000)

        Returns
        -------
        tuple[bool, Socket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
              Socket object.
        """
        socket_instance = None
        for _ in range(create_max_attemps):
            try:
                # TCP Connection, do we want UDP instead (socket.SOCK_DGRAM)?
                socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                break
            except socket.error as e:
                print(f"Could not create socket: {e}.")

        if socket_instance is None:
            return False, None

        connected = False
        for _ in range(connect_max_attempts):
            try:
                socket_instance.connect(host, port)
                connected = True
                break
            except socket.gaierror as e:
                print(f"Could not connect to socket, address related error: {e}. "
                    "Make sure the host and port are correct.")
            except socket.error as e:
                print(f"Could not connect to socket, connection error: {e}.")

        if not connected:
            return False, None

        return True, Socket(cls.__create_key, socket_instance)

    def __init__(self, class_private_create_key, socket_instance: socket.socket):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Socket.__create_key, "Use create() method"

        self.__socket_instance = socket_instance

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
            self.__socket_instance.sendall(data)
        except socket.error as e:
            print(f"Could not send data: {e}.")
            return False

        return True
