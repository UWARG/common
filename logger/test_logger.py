"""
Logger unit tests.
"""

import inspect
import pathlib
import re

import pytest

from .modules import logger, logger_setup_main
from .read_yaml.modules import read_yaml


@pytest.fixture
def main_logger_instance_and_log_file_path() -> logger.Logger:  # type: ignore
    """
    Returns the main logger with logging to file enabled and sets up logging directory.
    """
    result, config = read_yaml.open_config(logger.CONFIG_FILE_PATH)
    assert result

    result, instance, log_file_path = logger_setup_main.setup_main_logger(config=config)
    assert result
    yield instance, log_file_path


@pytest.fixture
def logger_instance_to_file_enabled() -> logger.Logger:  # type: ignore
    """
    Returns a logger with logging to file enabled.
    """
    result, instance = logger.Logger.create("test_logger_to_file_enabled", True)
    assert result
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
        actual = logger.Logger.message_and_metadata(message, frame)

        expected = f"[{__file__} | test_message_and_metadata_with_frame | 59] Test message"

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
            f"[DEBUG]*{__file__} | test_log_with_frame_info | 90] {test_message}\n"
        )

        assert re.search(expected_pattern, actual)

    def test_log_to_file(
        self,
        main_logger_instance_and_log_file_path: "tuple[logger.Logger | None, pathlib.Path | None]",
        logger_instance_to_file_enabled: logger.Logger,
    ) -> None:
        """
        Test if messages are logged to file
        All levels are done in one test since they will all be logged to the same file
        """
        main_logger_instance, log_file_path = main_logger_instance_and_log_file_path

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

        main_log_file_path = pathlib.Path(log_file_path, "main.log")
        test_log_file_path = pathlib.Path(log_file_path, "test_logger_to_file_enabled.log")

        with open(main_log_file_path, "r", encoding="utf8") as log_file:
            actual_main = log_file.read()

        with open(test_log_file_path, "r", encoding="utf8") as log_file:
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

        expected_pattern = re.compile(f"[DEBUG]*{test_message}\n")

        assert re.search(expected_pattern, actual)

    def test_debug_log_info_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if info level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.info(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(f"[INFO]*{test_message}\n")

        assert re.search(expected_pattern, actual)

    def test_debug_log_warning_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if warning level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.warning(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(f"[WARNING]*{test_message}\n")

        assert re.search(expected_pattern, actual)

    def test_debug_log_error_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if error level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.error(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(f"[ERROR]*{test_message}\n")

        assert re.search(expected_pattern, actual)

    def test_debug_log_critical_to_stdout(
        self, caplog: pytest.LogCaptureFixture, logger_instance_to_file_disabled: logger.Logger
    ) -> None:
        """
        Test if critical level message is logged to stdout
        """
        test_message = "test message"

        logger_instance_to_file_disabled.critical(test_message, False)
        actual = caplog.text

        expected_pattern = re.compile(f"[CRITICAL]*{test_message}\n")

        assert re.search(expected_pattern, actual)
