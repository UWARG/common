# Network
This module facilitates communication over TCP and UDP.

## Testing
Instructions on how to use the unit tests.

### TCP
To test `client_socket` and `server_socket`, run the test scripts in the following order:

1. `test_tcp_receiver.py`
2. `test_tcp_sender.py`

`test_tcp_receiver.py` will start a server socket listening on `localhost:8080`.
`test_tcp_sender.py` will first encode each image in `test_images`, then send the raw byte data to the server. 

The main loop expects a response from the server, consisting of the original image, data before continuing to the next image. The asserted condition in the main loop tests for equality between the image byte data that was sent to the server, and the byte data that was received, ensuring data integrity.
