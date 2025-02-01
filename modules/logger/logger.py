"""
Logs debug messages.
"""

import datetime
import inspect
import logging
import os
import pathlib
import sys
import time

# Used in type annotation of logger parameters
# pylint: disable-next=unused-import
import types

import cv2
import numpy as np

from ..read_yaml import read_yaml


CONFIG_FILE_PATH = pathlib.Path(os.path.dirname(__file__), "config_logger.yaml")


class Logger:
    """
    Instantiates Logger objects.
    """

    __create_key = object()

    @classmethod
    def create(cls, name: str, enable_log_to_file: bool) -> "tuple[bool, Logger | None]":
        """
        Create and configure a logger.
        """
        # Configuration settings
        result, config = read_yaml.open_config(CONFIG_FILE_PATH)
        if not result:
            print("ERROR: Failed to load configuration file")
            return False, None

        # Get Pylance to stop complaining
        assert config is not None

        try:
            log_directory_path = config["logger"]["directory_path"]
            file_datetime_format = config["logger"]["file_datetime_format"]
            logger_format = config["logger"]["format"]
            logger_datetime_format = config["logger"]["log_datetime_format"]
        except KeyError as exception:
            print(f"Config key(s) not found: {exception}")
            return False, None

        # Create a unique logger instance
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt=logger_format,
            datefmt=logger_datetime_format,
        )

        # Handles logging to terminal
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if not enable_log_to_file:
            return True, Logger(cls.__create_key, logger, None)

        # Handles logging to file

        # Get the path to the logs directory.
        entries = os.listdir(log_directory_path)

        if len(entries) == 0:
            print("ERROR: The directory for this log session was not found.")
            return False, None

        log_names = [
            entry for entry in entries if os.path.isdir(os.path.join(log_directory_path, entry))
        ]

        # Find the log directory for the current run, which is the most recent timestamp.
        log_path = max(
            log_names,
            key=lambda datetime_string: datetime.datetime.strptime(
                datetime_string, file_datetime_format
            ),
        )

        filepath = pathlib.Path(log_directory_path, log_path, f"{name}.log")
        try:
            file = os.open(filepath, os.O_RDWR | os.O_EXCL | os.O_CREAT)
            os.close(file)
        except OSError:
            print("ERROR: Log file already exists.")
            return False, None

        file_handler = logging.FileHandler(filename=filepath, mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return True, Logger(cls.__create_key, logger, pathlib.Path(log_directory_path, log_path))

    def __init__(
        self,
        class_create_private_key: object,
        logger: logging.Logger,
        maybe_log_directory: pathlib.Path | None,
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_create_private_key is Logger.__create_key, "Use create() method."

        self.logger = logger
        self.__maybe_log_directory = maybe_log_directory

    @staticmethod
    def message_and_metadata(message: str, frame: "types.FrameType | None") -> str:
        """
        Extracts metadata from frame and appends it to the message.
        """
        if frame is None:
            return message

        # Get Pylance to stop complaining
        assert frame is not None

        function_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        line_number = inspect.getframeinfo(frame).lineno

        return f"[{filename} | {function_name} | {line_number}] {message}"

    def debug(self, message: str, log_with_frame_info: bool = True) -> None:
        """
        Logs a debug level message.
        """
        if log_with_frame_info:
            logger_frame = inspect.currentframe()
            caller_frame = logger_frame.f_back
            message = self.message_and_metadata(message, caller_frame)
        self.logger.debug(message)

    def info(self, message: str, log_with_frame_info: bool = True) -> None:
        """
        Logs an info level message.
        """
        if log_with_frame_info:
            logger_frame = inspect.currentframe()
            caller_frame = logger_frame.f_back
            message = self.message_and_metadata(message, caller_frame)
        self.logger.info(message)

    def warning(self, message: str, log_with_frame_info: bool = True) -> None:
        """
        Logs a warning level message.
        """
        if log_with_frame_info:
            logger_frame = inspect.currentframe()
            caller_frame = logger_frame.f_back
            message = self.message_and_metadata(message, caller_frame)
        self.logger.warning(message)

    def error(self, message: str, log_with_frame_info: bool = True) -> None:
        """
        Logs an error level message.
        """
        if log_with_frame_info:
            logger_frame = inspect.currentframe()
            caller_frame = logger_frame.f_back
            message = self.message_and_metadata(message, caller_frame)
        self.logger.error(message)

    def critical(self, message: str, log_with_frame_info: bool = True) -> None:
        """
        Logs a critical level message.
        """
        if log_with_frame_info:
            logger_frame = inspect.currentframe()
            caller_frame = logger_frame.f_back
            message = self.message_and_metadata(message, caller_frame)
        self.logger.critical(message)

    def save_image(
        self,
        image: np.ndarray,
        filename: str = "",
        log_with_frame_info: bool = True,
    ) -> None:
        """
        Logs an image.

        Args:
            image: The image to log.
            filename: The filename to save the image as.
            log_with_frame_info: Whether to log the frame info.
        """
        if self.__maybe_log_directory is None:
            self.logger.warning("Image not saved: Logger not set up with file logging")
            return

        # Get Pylance to stop complaining
        assert self.__maybe_log_directory is not None

        full_file_name = (
            f"{self.logger.name}_{int(time.time())}_{filename}.png"
            if filename != ""
            else f"{self.logger.name}_{int(time.time())}.png"
        )
        filepath = pathlib.Path(self.__maybe_log_directory, full_file_name)

        cv2.imwrite(str(filepath), image)

        self.info(f"Image saved as: {full_file_name}", log_with_frame_info)
