"""
Test on some basic QR codes.
"""

import pathlib

import cv2

from modules.qr.qr_scanner import QrScanner


PARENT_DIRECTORY = pathlib.Path("tests", "unit", "qr_images")

IMAGE_2023_TASK1_ROUTE_PATH = pathlib.Path(PARENT_DIRECTORY, "2023_task1_route.png")
IMAGE_2023_TASK1_DIVERSION_PATH = pathlib.Path(PARENT_DIRECTORY, "2023_task1_diversion.png")
IMAGE_2023_TASK2_ROUTES_PATH = pathlib.Path(PARENT_DIRECTORY, "2023_task2_routes.png")

IMAGE_2023_TASK1_ROUTE_TEXT = "Follow route: Quebec; Lima; Alpha; Tango"
IMAGE_2023_TASK1_DIVERSION_TEXT = (
    "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima"
)
IMAGE_2023_TASK2_ROUTES_TEXT = """Route number 1: 2 pers; Alpha; Hotel; 15 kg; nil; $37
Route number 2: 6 pers; Bravo; Oscar; 10 kg; nil; $150
Route number 3: 3 pers; Alpha; Papa; 15 kg; nil; $101
Route number 4: 2 pers; Papa; Whiskey; 15 kg; nil; $75
Route number 5: 4 pers; Oscar; Golf; 10 kg; nil; $83
Route number 6: 4 pers; Whiskey; Alpha; 15 kg; nil; $81
Route number 7: 2 pers; Alpha; Zulu; 15 kg; No landing Zulu – Hover for 15s; $44
Route number 8: 6 pers; Golf; Whiskey; 10 kg; nil; $115
Route number 9: 6 pers; Tango; Zulu; 15 kg; No landing Zulu – Hover for 15s; $95
Route number 10: 3 pers; Bravo; Tango; 10 kg; nil; $200
Route number 11: 5 pers; Zulu; Oscar; 15 kg; No landing Zulu – Hover for 15s; $80
Route number 12: 2 pers; Bravo; Papa; 10 kg; nil; $80
Route number 13: 2 pers; Hotel; Zulu; 15 kg; No landing Zulu – Hover for 15s; $42
Route number 14: 2 pers; Whiskey; Hotel; 15 kg; nil; $28
Route number 15: 6 pers; Tango; Oscar; 15 kg; nil; $108
Route number 16: 4 pers; Hotel; Tango; 15 kg; nil; $68
Route number 17: 3 pers; Papa; Zulu; 15 kg; No landing Zulu – Hover for 15s; $93
Route number 18: 2 pers; Bravo; Whiskey; 10 kg; nil; $35
Route number 19: 2 pers; Whiskey; Zulu; 15 kg; No landing Zulu – Hover for 15s; $110
"""


class TestScanner:
    """
    Tests DetectTarget.run() .
    """

    def test_2023_task1_route(self) -> None:
        """
        Task 1 route
        """
        # Setup
        expected = IMAGE_2023_TASK1_ROUTE_TEXT
        image = cv2.imread(str(IMAGE_2023_TASK1_ROUTE_PATH))
        assert image is not None

        # Run
        result, actual = QrScanner.get_qr_text(image)

        # Test
        assert result
        assert actual is not None
        assert actual == expected

    def test_2023_task1_diversion(self) -> None:
        """
        Task 1 diversion
        """
        # Setup
        expected = IMAGE_2023_TASK1_DIVERSION_TEXT
        image = cv2.imread(str(IMAGE_2023_TASK1_DIVERSION_PATH))
        assert image is not None

        # Run
        result, actual = QrScanner.get_qr_text(image)

        # Test
        assert result
        assert actual is not None
        assert actual == expected

    def test_2023_task2_routes(self) -> None:
        """
        Task 2 routes
        """
        # Setup
        expected = IMAGE_2023_TASK2_ROUTES_TEXT
        image = cv2.imread(str(IMAGE_2023_TASK2_ROUTES_PATH))
        assert image is not None

        # Run
        result, actual = QrScanner.get_qr_text(image)

        # Test
        assert result
        assert actual is not None
        assert actual == expected
