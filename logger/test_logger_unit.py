"""
Logger unit tests.
"""

import inspect
import pytest

from logger.modules import logger


@pytest.fixture
def logger_instance() -> logger.Logger:  # type: ignore
    """
    Returns an instance of the Logger class with logging to file disabled.
    """
    result, instance = logger.Logger.create("test_logger", False)
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

        expected = f"[{__file__} | test_message_and_metadata_with_frame | 32] Test message"

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
