"""
Logger unit tests.
"""

import inspect
import pathlib
import re

import cv2
import numpy as np
import pytest

from modules.logger import logger
from modules.logger import logger_main_setup
from modules.read_yaml import read_yaml


@pytest.fixture
def main_logger_instance_and_logging_path() -> tuple[logger.Logger, pathlib.Path]:  # type: ignore
    """
    Returns the main logger with logging to file enabled and sets up logging directory.
    """
    result, config = read_yaml.open_config(logger.CONFIG_FILE_PATH)
    assert result
    assert config is not None

    # Increase max attempts for every use of this fixture
    result, instance, logging_path = logger_main_setup.setup_main_logger(config, max_attempts=2)
    assert result
    assert instance is not None
    assert logging_path is not None

    yield instance, logging_path


@pytest.fixture
def logger_instance_to_file_enabled() -> logger.Logger:  # type: ignore
    """
    Returns a logger with logging to file enabled.
    """
    result, instance = logger.Logger.create("test_logger_to_file_enabled", True)
    assert result
    assert instance is not None

    yield instance


@pytest.fixture
def logger_instance_to_file_disabled() -> logger.Logger:  # type: ignore
    """
    Returns a logger with logging to file disabled.
    """
    result, instance = logger.Logger.create("test_logger_to_file_disabled", False)
    assert result
    yield instance


class TestMessageAndMetadata:
    """
    Test if message_and_metadata function correctly extracts information from the frame.
    """

    def test_message_and_metadata_with_frame(self) -> None:
        """
        Test by passing in a frame
        """
        frame = inspect.currentframe()
        message = "Test message"
        expected = (
            f"[{__file__} | {self.test_message_and_metadata_with_frame.__name__} | 74] Test message"
        )

        # Get line number of this function call
        actual = logger.Logger.message_and_metadata(message, frame)

        assert actual == expected

    def test_message_and_metadata_without_frame(self) -> None:
        """
        Test with frame is None
        """
        frame = None
        message = "Test message"
        actual = logger.Logger.message_and_metadata(message, frame)

        expected = "Test message"

        assert actual == expected


# Fixtures are used to setup and teardown resources for tests
# pylint: disable=redefined-outer-name
class TestLogger:
    """
    Test if logger logs the correct messages to file and stdout
    """

    def test_log_with_frame_info(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if frame information is logged
        """
        test_message = "test message"

        logger_instance_to_file_disabled.debug(test_message, True)
        actual = caplog.text

        expected_pattern = re.compile(
            r"DEBUG.*\["
            + re.escape(__file__)
            + r" | test_log_with_frame_info | 93\]"
            + re.escape(test_message)
        )

        assert re.search(expected_pattern, actual) is not None

    def test_log_to_file(
        self,
        main_logger_instance_and_logging_path: tuple[logger.Logger, pathlib.Path],
        logger_instance_to_file_enabled: logger.Logger,
    ) -> None:
        """
        Test if messages are logged to file
        All levels are done in one test since they will all be logged to the same file
        """
        main_logger_instance, logging_path = main_logger_instance_and_logging_path

        main_message = "main message"
        main_logger_instance.debug(main_message, False)
        main_logger_instance.info(main_message, False)
        main_logger_instance.warning(main_message, False)
        main_logger_instance.error(main_message, False)
        main_logger_instance.critical(main_message, False)

        test_message = "test message"
        logger_instance_to_file_enabled.debug(test_message, False)
        logger_instance_to_file_enabled.info(test_message, False)
        logger_instance_to_file_enabled.warning(test_message, False)
        logger_instance_to_file_enabled.error(test_message, False)
        logger_instance_to_file_enabled.critical(test_message, False)

        main_logging_path = pathlib.Path(logging_path, "main.log")
        test_logging_path = pathlib.Path(logging_path, "test_logger_to_file_enabled.log")

        with open(main_logging_path, "r", encoding="utf8") as log_file:
            actual_main = log_file.read()

        with open(test_logging_path, "r", encoding="utf8") as log_file:
            actual_test = log_file.read()

        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            expected = f"[{level}] {main_message}\n"
            assert expected in actual_main  # don't know timestamps, so check existance of message

        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            expected = f"[{level}] {test_message}\n"
            assert expected in actual_test  # don't know timestamps, so check existance of message

    def test_debug_log_debug_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if debug level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.debug(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(r"DEBUG.*" + re.escape(test_message))

        assert re.search(expected_pattern, actual) is not None

    def test_debug_log_info_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if info level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.info(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(r"INFO.*" + re.escape(test_message))

        assert re.search(expected_pattern, actual) is not None

    def test_debug_log_warning_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if warning level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.warning(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(r"WARNING.*" + re.escape(test_message))

        assert re.search(expected_pattern, actual) is not None

    def test_debug_log_error_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if error level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.error(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(r"ERROR.*" + re.escape(test_message))

        assert re.search(expected_pattern, actual) is not None

    def test_debug_log_critical_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if critical level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.critical(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(r"CRITICAL.*" + re.escape(test_message))

        assert re.search(expected_pattern, actual) is not None

    def test_log_images(
        self,
        main_logger_instance_and_logging_path: tuple[logger.Logger, pathlib.Path],
        logger_instance_to_file_enabled: logger.Logger,
    ) -> None:
        """
        Test logging images.
        """
        # Setup
        expected_image = np.zeros((480, 640, 3), dtype=np.uint8)

        main_logger_instance, logging_path = main_logger_instance_and_logging_path

        # Run
        main_logger_instance.save_image(expected_image)
        logger_instance_to_file_enabled.save_image(expected_image)

        # Check
        image_paths = list(logging_path.glob("*.png"))
        assert len(image_paths) == 2

        for image_path in image_paths:
            actual_image = cv2.imread(image_path)

            assert np.array_equal(actual_image, expected_image)
