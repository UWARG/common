# Network
<<<<<<< HEAD
This module facilitates communication over TCP and UDP.

## Testing
Instructions on how to use the unit tests.

### TCP
To test `TcpClientSocket` and `TcpServerSocket`, run the test scripts in the following order (could be on 2 different machines, but edit network addresses accordingly):

1. `test_tcp_receiver.py`
2. `test_tcp_sender.py`

`start_tcp_receiver.py` will start a server socket listening for connections on `localhost:8080`.
`start_tcp_sender.py` will then start a client socket and connect to the server. 
Then, the client will send an integer (4 bytes) representing the message length, followed by the actual test message.
The server will receive the message and send it back to the client.
This process repeats until all test messages are sent.

### UDP
To test `UdpClientSocket` and `UdpServerSocket`, run the test scripts in the following order (could be on 2 different machines, but edit network addresses accordingly):

1. `test_udp_receiver.py`
2. `test_udp_sender.py`

`start_udp_receiver.py` will start a server socket listening for data on `localhost:8080`.
`start_udp_sender.py` will then start a client socket and send data to the server. 
Then, the client will send an integer (4 bytes) representing the message length, followed by the actual test message.
This process repeats until all test messages are sent.

*Note: UDP does not guarantee that data is sent or is not corrupted.
It is a connectionless protocol and thus the server cannot send any messages.
=======
To test `client_socket` and `server_socket`, we will set up a socket server that listens for image byte data from a sender.

Run the test scripts in the following order:

1. `test_receiver.py`
2. `test_sender.py`

`test_receiver.py` will start a socket server listening on `127.0.0.1:8080`. `test_sender.py` will first encode each image returned from `get_images`, then send the raw byte data to the server. 

The main loop expects a response from the server, consisting of the original image, data before continuing to the next image. The asserted condition in the main loop tests for equality between the image byte data that was sent to the server, and the byte data that was received, ensuring data integrity.

>>>>>>> 8c58ed6 (Refactor pytest into sender and receiver scripts)
