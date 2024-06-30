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
        self.__socket = socket_instance
        self.server_address = server_address

    @classmethod
    def create(
        cls, host: str = "localhost", port: int = 5000
    ) -> "tuple[bool, UdpClientSocket | None]":
        """
        Initializes UDP client socket with the appropriate server address.


        Parameters
        ----------
        host: str, default "localhost"
            The hostname of the server. 
        port: int, default 5000
            The port number of the server.


        Returns
        -------
        tuple[bool, UdpClientSocket | None]
            The boolean value represents whether the initialization was successful or not.
                - If it is not successful, the second parameter will be None.
                - If it is successful, the method will return True and a UdpClientSocket object will be created.
        """
        try:
            socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (host, port)
            return True, UdpClientSocket(cls.__create_key, socket_instance, server_address)

        except socket.gaierror as e:
            print(
                f"Could not connect to socket, address related error: {e}. Make sure the host and port are correct."
            )

        except socket.error as e:
            print(f"Could not connect: {e}")

        return False, None




