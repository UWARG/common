"""
ArducamIR implementation of the camera wrapper.
"""

import enum
import numpy as np
import cv2

import ArducamEvkSDK
from ArducamEvkSDK import Camera, Frame, Param
import arducam_rgbir_remosaic

from . import base_camera


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
    def create(cls) -> "tuple[True, CameraArducamIR] | tuple[False, None]":
        # TODO: Do I need a create() function, if there are no invalid inputs?

        camera = Camera()

        return True, CameraArducamIR(cls.__create_key, camera)

    def __init__(self, class_private_create_key: object, camera: ArducamEvkSDK.Camera) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CameraArducamIR.__create_key, "Use create() method."

        param = Param()
        param.config_file_name = "config.cfg"

        if not camera.open(param):
            print("Error trying to open Arducam camera")

        self.__camera = camera
        self.__camera.init()
        self.__camera.start()

    def __del__(self) -> None:
        """
        Destructor. Release hardware resources.
        """
        self.__camera.stop()
        self.__camera.close()

    def run(self) -> tuple[True, Frame] | tuple[False, None]:
        """
        Takes a picture with ArducamIR camera.

        Return: Success, Frame
        """
        image_data = self.__camera.capture()
        if image_data is None:
            return False, None

        return True, image_data

    def frame_to_mat(self, data: np.ndarray, output: ArducamOutput) -> np.ndarray | None:
        """
        Converts Frame to Mat
        """
        bayer, ir = arducam_rgbir_remosaic.rgbir_remosaic(data, arducam_rgbir_remosaic.GRIG)
        color = cv2.cvtColor(bayer, cv2.COLOR_BayerRG2BGRA)
        ir_color = cv2.cvtColor(ir, cv2.COLOR_GRAY2BGRA)
        ir_resize = cv2.resize(ir_color, (bayer.shape[1], bayer.shape[0]))
        if output == ArducamOutput.RGB:
            return color
        if output == ArducamOutput.IR:
            return ir_resize
        print("Error. Invalid output type.")
        return None

    def demosaic(self, image: Frame, output: ArducamOutput) -> Frame:
        """
        Converts Frame to Mat
        """
        width = image.format.width
        height = image.format.height
        bit_depth = image.format.bit_depth
        data = image.data

        if bit_depth > 8:
            data = np.frombuffer(data, np.uint16).reshape(height, width)
            data = (data >> (bit_depth - 8)).astype(np.uint8)
        else:
            data = np.frombuffer(data, np.uint8).reshape(height, width)

        frame = self.frame_to_mat(data, output)

        return frame
