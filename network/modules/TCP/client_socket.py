"""
Wrapper for TCP client socket operations.
"""

import socket

from .socket_wrapper import TcpSocket


class TcpClientSocket(TcpSocket):
    """
    Wrapper for TCP client socket operations.
    """

    __create_key = object()

    def __init__(self, class_private_create_key: object, socket_instance: socket.socket) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is TcpClientSocket.__create_key, "Use create() method"

        super().__init__(socket_instance=socket_instance)

    @classmethod
    def create(
        cls,
        instance: socket.socket = None,
        host: str = "localhost",
        port: int = 5000,
        connection_timeout: float = 60.0,
    ) -> "tuple[bool, TcpClientSocket | None]":
        """
        Establishes socket connection through provided host and port.

        Parameters
        ----------
        instance: socket.socket (default None)
            For initializing Socket with an existing socket object.
        host: str (default "localhost")
        port: int (default 5000)
            The host combined with the port will form an address (e.g. localhost:5000)
        connection_timeout: float (default 10.0)
            Timeout for establishing connection, in seconds

        Returns
        -------
        tuple[bool, TcpClientSocket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created TcpClientSocket object.
        """

        # Reassign instance before check or Pylance will complain
        socket_instance = instance
        if socket_instance is not None:
            return True, TcpClientSocket(cls.__create_key, socket_instance)

        if connection_timeout <= 0:
            # Zero puts it on non-blocking mode, which complicates things
            print("Must be a positive non-zero value")
            return False, None

        try:
            socket_instance = socket.create_connection((host, port), connection_timeout)
            return True, TcpClientSocket(cls.__create_key, socket_instance)
        except TimeoutError:
            print("Connection timed out.")
        except socket.gaierror as e:
            print(
                f"Could not connect to socket, address related error: {e}. "
                "Make sure the host and port are correct."
            )
        except socket.error as e:
            print(f"Could not connect to socket, connection error: {e}.")

        return False, None
