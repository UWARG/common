"""
To Test the module message_encoding_decoding.py
"""

from modules.data_encoding import message_encoding_decoding
from modules import position_global
from modules.data_encoding import worker_enum


def test_encoding_decoding() -> None:
    """
    Function to test encoding
    """
    # Step 1: Create a worker_name and PositionGlobal object
    worker_name = "communications_worker"  # =3 in Worker_Enum
    success, original_position = position_global.PositionGlobal.create(
        latitude=34.24902422, longitude=84.6233434, altitude=27.4343424
    )
    assert success

    # Step 2: Encode the PositionGlobal object
    result, encoded_bytes = message_encoding_decoding.encode_position_global(
        worker_name, original_position
    )
    assert result

    # Step 3: Decode the bytes back to a PositionGlobal object
    result, worker, decoded_position = message_encoding_decoding.decode_bytes_to_position_global(
        encoded_bytes
    )
    assert result

    # Step 4: Validate that the original and decoded objects match
    assert worker_enum.WorkerEnum[worker_name.upper()] == worker  # Checks if Enum type Matches

    assert original_position.latitude == decoded_position.latitude
    assert original_position.longitude == decoded_position.longitude
    assert original_position.altitude == decoded_position.altitude
