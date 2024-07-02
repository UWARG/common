import socket
import struct 

CHUNK_SIZE = 4096

class UdpSocket:
    """
    Wrapper for Python's socket module.
    """



    def __init__(self, socket_instance: socket.socket = None) -> None:
        """
        Parameters
        ----------
        instance: socket.socket
            For initializing Socket with an existing socket object.
        """

        if socket_instance is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__socket.settimeout(10.0)
        else:
            self.__socket = socket_instance

    @classmethod
    def send_to(self, data: bytes, host: str = "", port: int = 5000) -> bool:
        """
        Sends data to specified address


        Parameters
        ----------
        data: bytes
        host: str (default "")
            Empty string is interpreted as '0.0.0.0' (IPv4) or '::' (IPv6), which is an open address
        port: int (default 5000)
            The host, combined with the port, will form the address as a tuple


        Returns
        -------
        bool: if data was transferred successfully

        """
        address = (host, port)

        data_sent = 0
        data_size = len(data)

        while data_sent < data_size:

            if data_sent + CHUNK_SIZE > data_size:
                chunk = data[data_sent:data_size]
            else:
                chunk = data[data_sent:data_sent+CHUNK_SIZE]

            try:
                self.__socket.sendto(chunk, address)
                data_sent += len(chunk)
            except socket.error as e:
                print(f"Could not send data: {e}")
                return False

        return True

    def recv(self, buf_size: int) -> "tuple[bool, bytes | None]":
        """
        Parameters
        ----------
        buf_size: int
            The number of bytes to receive

        Returns
        -------
        tuple:
            bool - True if data was received and unpacked successfully, False otherwise
            bytes | None - The received data, or None if unsuccessful

        """
        data = b''
        addr = None
        data_size = 0

        while data_size < buf_size:

            try:
                packet, current_addr = self.__socket.recvfrom(buf_size)
                if addr is None:
                    addr = current_addr
                elif addr != current_addr:
                    print(f"Data received from multiple addresses: {addr} and {current_addr}")
                    packet = b''
                
                # Add the received packet to the accumulated data and increment the size accordingly 
                data += packet  
                data_size += len(packet) 


            except socket.error as e:
                print(f"Could not receive data: {e}")
                return False, None
            

        return True, data


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
