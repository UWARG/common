"""
To Test the module metadata_encoding_decoding.py
"""

from modules import data_encoding


def test_encoding_metadata() -> None:
    """
    Function to test encoding
    """

    # Step 1: Create a worker_name and PositionGlobal object
    worker_name = "communications_worker"  # =3 in Worker_Enum
    number_of_messages = 5

    # Step 2: Encode the WorkerEnum ID and number of messages

    encoded_bytes = data_encoding.metadata_encoding_decoding.encode_metadata(
        worker_name, number_of_messages
    )
    assert encoded_bytes[0] is True

    # Step 3: Decode the bytes back to a unsigned char and int respectively
    decoded_metadata = data_encoding.metadata_encoding_decoding.decode_metadata(encoded_bytes[1])
    assert decoded_metadata[0] is True

    # Step 4: Validate that the original and decoded objects match
    assert decoded_metadata[1] == data_encoding.worker_enum.WorkerEnum(
        data_encoding.worker_enum.WorkerEnum[worker_name.upper()].value
    )

    assert number_of_messages == decoded_metadata[2]
