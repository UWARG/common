"""
To Test the module metadata_encoding_decoding.py
"""

from modules.data_encoding import metadata_encoding_decoding
from modules.data_encoding import worker_enum


def test_encoding_metadata() -> None:
    """
    Function to test encoding
    """
    # Step 1: Create a worker_name and PositionGlobal object
    worker_name = "communications_worker"  # =3 in worker_enum.py
    number_of_messages = 5

    # Step 2: Encode the WorkerEnum ID and number of messages
    result, encoded_bytes = metadata_encoding_decoding.encode_metadata(
        worker_name, number_of_messages
    )
    assert result

    # Step 3: Decode the bytes back to a unsigned char and int respectively
    result, worker_class, decoded_number_of_messages = metadata_encoding_decoding.decode_metadata(
        encoded_bytes
    )
    assert result

    # Step 4: Validate that the original and decoded objects match
    assert worker_class == worker_enum.WorkerEnum(worker_name.upper())
    assert number_of_messages == decoded_number_of_messages
