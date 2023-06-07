"""
Converts an image containing QR codes into text
"""

import numpy as np
from pyzbar import pyzbar


class QrScanner:
    """
    Wrapper for pyzbar
    """

    def __init__(self):
        """
        Nothing to do
        """


    @staticmethod
    def get_qr_text(frame: np.ndarray) -> "tuple[bool, str | None]":
        """
        Attempts to find and decode a QR code from the given frame
        """
        decoded_qrs = pyzbar.decode(frame)
        if len(decoded_qrs) == 0:
            return False, None

        qr_text = decoded_qrs[0].data.decode()
        return True, qr_text
