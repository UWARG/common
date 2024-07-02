import socket
from network.modules.UDP.socket_wrapper import UdpSocket


class UdpClientSocket(UdpSocket):
    """
    Wrapper for client socket operations
    """

    __create_key = object()

    def __init__(
        self,
        class_private_create_key: object,
        socket_instance: socket.socket,
        server_address: tuple,
    ) -> None:
        """
        Private Constructor, use create() method.
        """

        assert class_private_create_key is UdpClientSocket.__create_key
        super().__init__(socket_instance=socket_instance)
        self.server_address = server_address

    @classmethod
    def create(
        cls, host: str = "localhost", port: int = 5000, connection_timeout: float = 60.0
    ) -> "tuple[bool, UdpClientSocket | None]":
        """
        Initializes UDP client socket with the appropriate server address.

        Parameters
        ----------
        host: str (default "localhost")
            The hostname or IP address of the server.
        port: int (default 5000)
            The port number of the server.
        connection_timeout: float (default 10.0)
            Timeout for establishing connection, in seconds

        Returns
        -------
        tuple[bool, UdpClientSocket | None]
            The boolean value represents whether the initialization was successful or not.
                - If it is not successful, the second parameter will be None.
                - If it is successful, the method will return True and a UdpClientSocket object will be created.
        """

        if connection_timeout <= 0:
            print("Must provide positive non-zero value.")
            return False, None

        try:
            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_instance.settimeout(connection_timeout)
            server_address = (host, port)
            return True, UdpClientSocket(cls.__create_key, socket_instance, server_address)
        except TimeoutError as e:
            print(f"Connection timed out: {e}")

        except socket.gaierror as e:
            print(
                f"Could not connect to socket, address related error: {e}. Make sure the host and port are correct."
            )

        except socket.error as e:
            print(f"Could not connect: {e}")

        return False, None

    def send(self, data: bytes) -> bool:
        """
        Sends data to the specified server address

        Parameters
        ----------
        data: bytes
            Takes in raw data that we wish to send

        Returns
        -------
        bool: True if data is sent successfully, and false if it fails to send
        """

        try:
            host, port = self.server_address
            super().send_to(data, host, port)
        except socket.error as e:
            print(f"Could not send data: {e}")
            return False

        return True

    def recv(self, buf_size: int) -> None:
        """
        Receive data method override to prevent client sockets from receiving data.

        Parameters
        ----------
        bufsize: int
            The amount of data to be received.

        Raises
        ------
        NotImplementedError
            Always raised because client sockets should not receive data.
        """

        raise NotImplementedError(
            "Client sockets cannot receive data as they are not bound by a port."
        )
