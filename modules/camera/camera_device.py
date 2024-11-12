"""
Camera device using OpenCV.
"""

import sys
import time

import cv2
import numpy as np

try:
    import picamera2
except ImportError:
    pass


class CameraDevice:
    """
    Wrapper for camera.
    """

    def __init__(
        self, use_picamera: bool, name: "int | str", save_nth_image: int = 0, save_name: str = ""
    ) -> None:
        """
        use_pc2: Use picamera2 implementation instead of opencv impl
        (optional) name: Device name or index (e.g. /dev/video0 ).
        (optional) save_nth_image: For debugging, saves every nth image.
            A value of 0 indicates no images should be saved
        (optional) save_name: For debugging, file name for saved images.
        """
        self.__using_picamera = use_picamera
        if self.__using_picamera:
            self.__camera = picamera2.Picamera2()
            # maybe use create_still_configuration()
            # if format is bad, use RGB 888 for [B, G, R] layout. BGR888 uses [R, G, B] layout
            # see section 4.2.2.2 bottom warning for explanation
            config = self.__camera.create_preview_configuration(
                {"size": (1920, 1080), "format": "BGR888"}
            )
            self.__camera.configure(config)
            self.__camera.start(show_preview=False)
        else:
            self.__camera = cv2.VideoCapture(name)
            assert self.__camera.isOpened()
            self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, sys.maxsize)
            self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, sys.maxsize)

        self.__divisor = save_nth_image
        self.__counter = 0
        self.__filename_prefix = ""
        if save_name != "":
            self.__filename_prefix = save_name + "_" + str(int(time.time())) + "_"

    def __del__(self) -> None:
        """
        Destructor.
        """
        if self.__using_picamera:
            self.__camera.stop()  # see https://github.com/raspberrypi/picamera2/blob/main/examples/opencv_mertens_merge.py
        else:
            self.__camera.release()

    def get_image(self) -> "tuple[bool, np.ndarray]":
        """
        Take a picture with the camera
        """

        result, image = (
            self.__camera.capture_array() if self.__using_picamera else self.__camera.read()
        )
        if not result:
            return False, None

        if self.__filename_prefix != "" and self.__divisor != 0:
            if self.__counter % self.__divisor == 0:
                filename = self.__filename_prefix + str(self.__counter) + ".png"
                cv2.imwrite(filename, image)

            self.__counter += 1

        return result, image
