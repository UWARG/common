"""
Wrapper for socket operations.
"""

import socket

from enum import Enum


class Protocol(Enum):
    """
    Enum used to select protocol when instantiating Socket.
    """
    TCP = socket.SOCK_STREAM
    UDP = socket.SOCK_DGRAM

class Socket:
    """
    Wrapper for Python's socket module.
    """
    __create_key = object()

    def __init__(self, class_private_create_key, socket_instance: socket.socket):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Socket.__create_key, "Use create() method"

        self.__socket = socket_instance

    @classmethod
    def create(
        cls,
        instance: socket.socket = None,
        **kwargs,
    ) -> "tuple[bool, Socket | None]":
        """
        Establishes socket connection through provided host and port.

        Parameters
        ----------
        instance: socket.socket (default None)
            For initializing Socket with an existing socket object.

        **kwargs: Additional keyword arguments.

        Returns
        -------
        tuple[bool, Socket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
              Socket object.
        """
        # Reassign instance before check or Pylance will complain
        socket_instance = instance
        if socket_instance is not None:
            return True, Socket(cls.__create_key, socket_instance)

        create_max_attempts = kwargs.get("create_max_attempts", 10)
        connect_max_attempts = kwargs.get("connect_max_attempts", 10)
        host = kwargs.get("host", "127.0.0.1")
        port = kwargs.get("port", 8080)
        protocol = kwargs.get("protocol", Protocol.TCP)

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
                if "bind" in kwargs:
                    socket_instance.bind((host, port))
                    socket_instance.listen()
                else:
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
        """
        try:
            self.__socket.close()
        except socket.error as e:
            print(f"Could not close socket: {e}.")
            return False

        return True

class ServerSocket(Socket):
    """
    Wrapper for server socket operations.
    """
    @classmethod
    def create(
        cls,
        instance: socket.socket = None,
        **kwargs,
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
        return super().create(instance=instance, **kwargs, bind=True)

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
            client_socket, addr = self.__socket.accept()
        except socket.error as e:
            print(f"Could not accept incoming connection: {e}.")
            return False, None

        print(f"Connected by {addr}.")
        return ClientSocket.create(instance=client_socket)


class ClientSocket(Socket):
    """
    Wrapper for client socket operations.
    """
    @classmethod
    def create(
        cls,
        instance: socket.socket = None,
        **kwargs,
    ) -> "tuple[bool, ClientSocket | None]":
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
        tuple[bool, ClientSocket | None]
            The first parameter represents if the socket creation is successful.
            - If it is not successful, the second parameter will be None.
            - If it is successful, the second parameter will be the created
              ClientSocket object.
        """
        return super().create(instance=instance, **kwargs)