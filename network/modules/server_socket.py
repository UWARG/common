"""
Wrapper for server socket operations.
"""

import socket

from network.modules.client_socket import ClientSocket
from network.modules.socket_wrapper import NetworkProtocol, Socket


class ServerSocket(Socket):
    """
    Wrapper for server socket operations.
    """

    __create_key = object()

    def __init__(self, class_private_create_key: object, socket_instance: socket.socket) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is ServerSocket.__create_key, "Use create() method"

        super().__init__(socket_instance=socket_instance)

    @classmethod
    def create(
        cls,
        instance: socket.socket = None,
        host: str = "127.0.0.1",
        port: int = 5000,
        protocol: NetworkProtocol = NetworkProtocol.TCP,
        create_max_attempts: int = 10,
        connect_max_attempts: int = 10,
    ) -> "tuple[bool, ServerSocket | None]":
        """
        Establishes socket connection through provided host and port.

        Parameters
        ----------
        instance: socket.socket (default None)
            For initializing Socket with an existing socket object.

        host: str (default "127.0.0.1")
        port: int (default 5000)
            The host combined with the port will form an address (e.g. localhost:5000)

        protocol: Protocol (default Protocol.TCP)
            Enum representing which protocol to use for the socket

        create_max_attempts: int (default 10)
        connect_max_attempts: int (default 10)

        Returns
        -------
        tuple[bool, ServerSocket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
              ServerSocket object.
        """
        # Reassign instance before check or Pylance will complain
        socket_instance = instance
        if socket_instance is not None:
            return True, ServerSocket(cls.__create_key, socket_instance)

        for _ in range(create_max_attempts):
            try:
                socket_instance = socket.socket(socket.AF_INET, protocol.value)
                break
            except socket.error as e:
                print(f"Could not create socket: {e}.")

        if socket_instance is None:
            return False, None

        connected = False
        for _ in range(connect_max_attempts):
            try:
                socket_instance.bind((host, port))
                socket_instance.listen()
                connected = True
                break
            except socket.gaierror as e:
                print(
                    f"Could not connect to socket, address related error: {e}. "
                    "Make sure the host and port are correct."
                )
            except socket.error as e:
                print(f"Could not connect to socket, connection error: {e}.")

        if not connected:
            return False, None

        return True, ServerSocket(cls.__create_key, socket_instance)

    def accept(self) -> "tuple[bool, ClientSocket | None]":
        """
        Waits (blocking) for an incoming connection. Then returns a ClientSocket instance
        representing the connection.

        Returns
        -------
        tuple[bool, ClientSocket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
              ClientSocket object.
        """
        try:
            client_socket, addr = self.get_socket().accept()
        except socket.error as e:
            print(f"Could not accept incoming connection: {e}.")
            return False, None

        print(f"Connected by {addr}.")
        return ClientSocket.create(instance=client_socket)