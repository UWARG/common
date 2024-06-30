import socket
import struct 

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
        else:
            self.__socket = socket_instance

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

            chunk = data[data_sent:data_sent+4096]
            packed_data = struct.pack(f'!{len(chunk)}s', chunk)

            try:
                self.__socket.sendto(packed_data, address)
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

        while True:

            try:
                packet, current_addr = self.__socket.recvfrom(buf_size)
                if addr is None:
                    addr = current_addr
                elif addr != current_addr:
                    print(f"Data received from multiple addresses: {addr} and {current_addr}")
                    return False, None

                data += packet  # Add the received packet to the accumulated data

                # Assuming that receiving less than buf_size means end of data
                if len(packet) < buf_size:
                    break

            except socket.error as e:
                print(f"Could not receive data: {e}")
                return False, None
            
        try:
            unpacked_data = struct.unpack(f'!{len(data)}', data)
        except struct.error as e:
                print(f"Could not unpack data: {e}")
                return False, None

        return True, unpacked_data


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
