# Network
To test `client_socket` and `server_socket`, we will set up a socket server that listens for image byte data from a sender.

Run the test scripts in the following order:

1. `test_receiver.py`
2. `test_sender.py`

`test_receiver.py` will start a socket server listening on `127.0.0.1:8080`. `test_sender.py` will first encode each image returned from `get_images`, then send the raw byte data to the server. 

The main loop expects a response from the server, consisting of the original image, data before continuing to the next image. The asserted condition in the main loop tests for equality between the image byte data that was sent to the server, and the byte data that was received, ensuring data integrity.

