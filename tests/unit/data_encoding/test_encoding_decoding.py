"""
To Test the module message_encoding_decoding.py
"""

from modules.data_encoding.message_encoding_decoding import (
    encode_position_global,
    decode_bytes_to_position_global,
)
from modules import position_global


def test_encoding_decoding() -> None:
    """
    Function to test encoding
    """

    # Step 1: Create a PositionGlobal object
    success, original_position = position_global.PositionGlobal.create(
        latitude=0.0, longitude=0.0, altitude=0.0
    )
    if not success:
        print("Failed to create PositionGlobal object.")
        return

    print(f"Original PositionGlobal: {original_position}")

    # Step 2: Encode the PositionGlobal object
    try:
        encoded_bytes = encode_position_global(original_position)
        print(f"Encoded bytes: {encoded_bytes}")
    except TypeError as e:
        print(f"Encoding failed due to invalid input type: {e}")
        return
    except ValueError as e:
        print(f"Encoding failed due to invalid value: {e}")
        return

    # Step 3: Decode the bytes back to a PositionGlobal object
    try:
        decoded_position = decode_bytes_to_position_global(encoded_bytes)
        print(f"Decoded PositionGlobal: {decoded_position}")
    except TypeError as e:
        print(f"Decoding failed due to invalid input type: {e}")
        return
    except ValueError as e:
        print(f"Decoding failed due to invalid value: {e}")
        return

    # Step 4: Validate that the original and decoded objects match
    if (
        original_position.latitude == decoded_position.latitude
        and original_position.longitude == decoded_position.longitude
        and original_position.altitude == decoded_position.altitude
    ):
        print("Test passed: Original and decoded PositionGlobal objects match.")
    else:
        print("Test failed: Original and decoded PositionGlobal objects do not match.")


# Run the test
if __name__ == "__main__":
    test_encoding_decoding()
