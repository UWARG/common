"""
To Test the module message_encoding_decoding.py
"""

from modules.data_encoding.worker_enum import WorkerEnum

from modules import position_global

from modules.data_encoding.message_encoding_decoding import (
    encode_position_global,
    decode_bytes_to_position_global,
)


def test_encoding_decoding() -> None:
    """
    Function to test encoding
    """

    # Step 1: Create a worker_name and PositionGlobal object
    worker_name = "communications_worker"  # =3 in Worker_Enum
    success, original_position = position_global.PositionGlobal.create(
        latitude=34.24902422, longitude=84.6233434, altitude=27.4343424
    )
    if not success:
        print("Failed to create PositionGlobal object.")
        return

    print(f"Original PositionGlobal: {original_position}")

    # Step 2: Encode the PositionGlobal object

    encoded_bytes = encode_position_global(worker_name, original_position)
    assert encoded_bytes[0] is True

    # Step 3: Decode the bytes back to a PositionGlobal object
    decoded_position = decode_bytes_to_position_global(encoded_bytes[1])
    assert decoded_position[0] is True

    # Step 4: Validate that the original and decoded objects match
    assert decoded_position[1] == WorkerEnum[worker_name.upper()].value
    assert original_position.latitude == decoded_position[2].latitude

    assert original_position.longitude == decoded_position[2].longitude
    assert original_position.altitude == decoded_position[2].altitude
