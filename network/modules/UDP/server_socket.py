import socket
from network.modules.UDP.socket_wrapper import UdpSocket


class UdpServerSocket(UdpSocket):
    """
    Wrapper for server socket operations.
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
        assert class_private_create_key is UdpServerSocket.__create_key, "Use create() method"
        super().__init__(socket_instance=socket_instance)
        self.__socket = socket_instance
        self.server_address = server_address

    @classmethod
    def create(cls, host: str = "", port: int = 5000, connection_timeout: float = 10.0) -> "tuple[bool, UdpServerSocket | None]":
        """
        Creates a UDP server socket bound to the provided host and port.


        Parameters
        ----------
        host: str (default "")
            The hostname or IP address to bind the socket to.
        port: int (default 5000)
            The port number to bind the socket to.
        connection_timeout: float (default 10.0)
            Timeout for establishing connection, in seconds


        Returns
        -------
        tuple[bool, UdpServerSocket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
                UdpServerSocket object.
        """

        if connection_timeout <= 0:
            print(f"Must provide a positive non-zero value.")
            return False, None

        try:
            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_instance.settimeout(connection_timeout)
            server_address = (host, port)
            socket_instance.bind(server_address)
            return True, UdpServerSocket(cls.__create_key, socket_instance, server_address)
        
        except TimeoutError as e:
            print(f"Connection timed out.")
        except socket.error as e:
            print(f"Could not create socket, error: {e}.")
            return False, None


