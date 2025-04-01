"""
ArducamIR implementation of the camera wrapper.
"""

import enum
import numpy as np
import cv2

import ArducamEvkSDK
import arducam_rgbir_remosaic

from . import base_camera

CAMERA_CONFIG_DIR = "./config/camera_config.cfg"


class ArducamOutput(enum.Enum):
    """
    Enum for ArducamIR output
    """

    RGB = 0
    IR = 1


class CameraArducamIR(base_camera.BaseCameraDevice):
    """
    Class for the ArducamSDK implementation of the ArducamIR camera.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, width: int, height: int, config: None
    ) -> "tuple[True, CameraArducamIR] | tuple[False, None]":

        camera = ArducamEvkSDK.Camera()

        param = ArducamEvkSDK.Param()
        param.config_file_name = CAMERA_CONFIG_DIR

        if not camera.open(param):
            return False, None

        return True, CameraArducamIR(cls.__create_key, camera)

    def __init__(
        self,
        class_private_create_key: object,
        camera: ArducamEvkSDK.Camera,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CameraArducamIR.__create_key, "Use create() method."

        self.__camera = camera
        self.__camera.init()
        self.__camera.start()

    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        self.__camera.stop()
        self.__camera.close()

    def run(self) -> tuple[True, ArducamEvkSDK.Frame] | tuple[False, None]:
        """
        Takes a picture with ArducamIR camera.

        Return: Success, Frame
        """
        image_data = self.__camera.capture()
        if image_data is None:
            return False, None

        return True, image_data

    def demosaic(self, image: ArducamEvkSDK.Frame, output: ArducamOutput) -> np.ndarray | None:
        """
        Converts Bayer Pattern & IR data to OpenCV Matrix
        """
        # Convert sensor data to useable format
        data = self.format(image)
        # Splits raw sensor data into bayer data and IR data using GRIG (Green, Red, IR, Green) filter pattern
        bayer, ir = arducam_rgbir_remosaic.rgbir_remosaic(data, arducam_rgbir_remosaic.GRIG)
        if output == ArducamOutput.RGB:
            # Converts Bayer data to BGRA (Blue, Green, Red, Alpha)
            return cv2.cvtColor(bayer, cv2.COLOR_BayerRG2BGRA)
        if output == ArducamOutput.IR:
            # Converts IR data to BGRA
            ir_color = cv2.cvtColor(ir, cv2.COLOR_GRAY2BGRA)
            # Resize the IR image so that they are both the same size
            return cv2.resize(ir_color, (bayer.shape[1], bayer.shape[0]))

    def format(self, image: ArducamEvkSDK.Frame) -> np.ndarray:
        """
        Formats byte buffer sensor input into 8-bit arrays
        """
        width = image.format.width
        height = image.format.height
        bit_depth = image.format.bit_depth
        data = image.data

        if bit_depth > 8:
            data = np.frombuffer(data, np.uint16).reshape(height, width)
            # Reduce higher precision inputs to 8-bit arrays
            data = (data >> (bit_depth - 8)).astype(np.uint8)
        else:
            data = np.frombuffer(data, np.uint8).reshape(height, width)

        return data
