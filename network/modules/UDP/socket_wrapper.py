import socket


class UdpSocket:
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
        if socket_instance is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.__socket = socket_instance


   
    def send_to(self, data: bytes, address: tuple) -> bool:
        """
        Sends data to specified address


        Parameters
        ----------
        data: bytes
        address: tuple


        Returns
        -------
        bool: if data was transferred successfully
       
        """
        try:
            self.__socket.sendto(data, address)
        except socket.error as e:
            print(f"Could not send data: {e}")
            return False
       
        return True
   


    def recv_from(self, buf_size: int) -> "tuple[bool, bytes | None]":
        """
        Receives data from the specified socket


        Parameters
        ---------
        buf_size: int
            The number of bytes to receive


        Returns
        -------
        tuple: If the data and address were received
       
        """
        try:
            data, addr = self.__socket.recvfrom(buf_size)
        except socket.error as e:
            print(f"Could not receive data: {e}")
            return False, None, ()
       
        return True, data, addr




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
            print(f"Could not close socket: {e}")
            return False
       
        return False
   


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
   
