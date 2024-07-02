"""
Wrapper for server socket operations.
"""

import socket

from network.modules.TCP.socket_wrapper import TcpSocket


class TcpServerSocket(TcpSocket):
    """
    Wrapper for server socket operations.
    """

    __create_key = object()

    def __init__(self, class_private_create_key: object, socket_instance: socket.socket) -> None:
        """
        Private constructor, use create() method.
        """

        assert class_private_create_key is TcpServerSocket.__create_key, "Use create() method"

        super().__init__(socket_instance=socket_instance)

    @classmethod
    def create(
        cls,
        instance: socket.socket = None,
        host: str = "",
        port: int = 5000,
        connection_timeout: float = 10.0,
    ) -> "tuple[bool, TcpServerSocket | None]":
        """
        Establishes socket connection through provided host and port.
            Note: Although in practice a TCP 'server' simply connects 2 clients together,
            this newly created client is called 'server' for simplicity and differentiation.

        Parameters
        ----------
        instance: socket.socket (default None)
            For initializing Socket with an existing socket object.
        host: str (default "")
            Empty string is interpreted as '0.0.0.0' (IPv4) or '::' (IPv6), which is all addresses.
            Could also use socket.gethostname(). (needed to enable other machines to connect)
        port: int (default 5000)
            The host combined with the port will form an address (e.g. localhost:5000)
        connection_timeout: float (default 10.0)
            Timeout for operations such as recieve

        Returns
        -------
        tuple[bool, TcpServerSocket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
              TcpServerSocket object.
        """

        # Reassign instance before check or Pylance will complain
        socket_instance = instance
        if socket_instance is not None:
            return True, TcpServerSocket(cls.__create_key, socket_instance)

        if socket.has_dualstack_ipv6():
            # Create server which can accept both IPv6 and IPv4 if possible
            try:
                server = socket.create_server(
                    (host, port),
                    family=socket.AF_INET6,
                    dualstack_ipv6=True,
                )
            except socket.gaierror as e:
                print(
                    f"Could not connect to socket, address related error: {e}.",
                    "Make sure the host and port are correct.",
                )
                return False, None
            except socket.error as e:
                print(f"Could not connect to socket, connection error: {e}.")
                return False, None
        else:
            # Otherwise, server can only accept IPv4
            try:
                server = socket.create_server((host, port))
            except socket.gaierror as e:
                print(
                    f"Could not connect to socket, address related error: {e}. "
                    "Make sure the host and port are correct."
                )
                return False, None
            except socket.error as e:
                print(f"Could not connect to socket, connection error: {e}.")
                return False, None

        # Currently listening, waiting for a connection
        if host == "":
            print(f"Listening for external connections on port {port}")
        else:
            print(f"Listening for internal connections on {host}:{port}")

        # This is in blocking mode, nothing can happen until this finishes, even keyboard interrupt
        socket_instance, addr = server.accept()

        # Now, a connection as been accepted (created a new 'client' socket)
        print(f"Accepted a connection from {addr[0]}:{addr[1]}")

        socket_instance.settimeout(connection_timeout)

        server.close()
        print("No longer accepting new connections.")

        return True, TcpServerSocket(cls.__create_key, socket_instance)
