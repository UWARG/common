"""
To Test the module message_encoding_decoding.py
"""

from modules.data_encoding.worker_enum import WorkerEnum

from modules.data_encoding.metadata_encoding_decoding import encode_metadata, decode_metadata


def test_encoding_metadata() -> None:
    """
    Function to test encoding
    """

    # Step 1: Create a worker_name and PositionGlobal object
    worker_name = "communications_worker"  # =3 in Worker_Enum
    number_of_messages = 5

    # Step 2: Encode the PositionGlobal object

    encoded_bytes = encode_metadata(worker_name, number_of_messages)
    assert encoded_bytes[0] is True

    # Step 3: Decode the bytes back to a PositionGlobal object
    decoded_metadata = decode_metadata(encoded_bytes[1])
    assert decoded_metadata[0] is True

    # Step 4: Validate that the original and decoded objects match
    assert decoded_metadata[1] == WorkerEnum(WorkerEnum[worker_name.upper()].value)

    assert number_of_messages == decoded_metadata[2]
