"""
Test on some basic QR codes
"""

import cv2

from modules.qr_scanner import QrScanner


IMAGE_2023_TASK1_ROUTE_PATH = "2023_task1_route.png"
IMAGE_2023_TASK1_DIVERSION_PATH = "2023_task1_diversion.png"
IMAGE_2023_TASK2_ROUTES_PATH = "2023_task2_routes.png"

IMAGE_2023_TASK1_ROUTE_TEXT = "Follow route: Quebec; Lima; Alpha; Tango"
IMAGE_2023_TASK1_DIVERSION_TEXT = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima"
IMAGE_2023_TASK2_ROUTES_TEXT = "\
Route number 1: 2 pers; Alpha; Hotel; 15 kg; nil; $37\n\
Route number 2: 6 pers; Bravo; Oscar; 10 kg; nil; $150\n\
Route number 3: 3 pers; Alpha; Papa; 15 kg; nil; $101\n\
Route number 4: 2 pers; Papa; Whiskey; 15 kg; nil; $75\n\
Route number 5: 4 pers; Oscar; Golf; 10 kg; nil; $83\n\
Route number 6: 4 pers; Whiskey; Alpha; 15 kg; nil; $81\n\
Route number 7: 2 pers; Alpha; Zulu; 15 kg; No landing Zulu – Hover for 15s; $44\n\
Route number 8: 6 pers; Golf; Whiskey; 10 kg; nil; $115\n\
Route number 9: 6 pers; Tango; Zulu; 15 kg; No landing Zulu – Hover for 15s; $95\n\
Route number 10: 3 pers; Bravo; Tango; 10 kg; nil; $200\n\
Route number 11: 5 pers; Zulu; Oscar; 15 kg; No landing Zulu – Hover for 15s; $80\n\
Route number 12: 2 pers; Bravo; Papa; 10 kg; nil; $80\n\
Route number 13: 2 pers; Hotel; Zulu; 15 kg; No landing Zulu – Hover for 15s; $42\n\
Route number 14: 2 pers; Whiskey; Hotel; 15 kg; nil; $28\n\
Route number 15: 6 pers; Tango; Oscar; 15 kg; nil; $108\n\
Route number 16: 4 pers; Hotel; Tango; 15 kg; nil; $68\n\
Route number 17: 3 pers; Papa; Zulu; 15 kg; No landing Zulu – Hover for 15s; $93\n\
Route number 18: 2 pers; Bravo; Whiskey; 10 kg; nil; $35\n\
Route number 19: 2 pers; Whiskey; Zulu; 15 kg; No landing Zulu – Hover for 15s; $110\n\
"


class TestScanner:
    """
    Tests DetectTarget.run()
    """

    def test_2023_task1_route(self):
        """
        Task 1 route
        """
        # Setup
        expected = IMAGE_2023_TASK1_ROUTE_TEXT
        image = cv2.imread(IMAGE_2023_TASK1_ROUTE_PATH)
        assert image is not None

        # Run
        result, actual = QrScanner.get_qr_text(image)

        # Test
        assert result
        assert actual is not None
        assert actual == expected

    def test_2023_task1_diversion(self):
        """
        Task 1 diversion
        """
        # Setup
        expected = IMAGE_2023_TASK1_DIVERSION_TEXT
        image = cv2.imread(IMAGE_2023_TASK1_DIVERSION_PATH)
        assert image is not None

        # Run
        result, actual = QrScanner.get_qr_text(image)

        # Test
        assert result
        assert actual is not None
        assert actual == expected

    def test_2023_task2_routes(self):
        """
        Task 2 routes
        """
        # Setup
        expected = IMAGE_2023_TASK2_ROUTES_TEXT
        image = cv2.imread(IMAGE_2023_TASK2_ROUTES_PATH)
        assert image is not None

        # Run
        result, actual = QrScanner.get_qr_text(image)

        # Test
        assert result
        assert actual is not None
        assert actual == expected
