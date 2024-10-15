"""
Log file merger unit tests.
"""

import pathlib
import shutil
import pytest

from .modules import log_file_merger


TEMP_LOGS_DIRECTORY = pathlib.Path("logs_temp")
MERGED_LOGS_FILENAME = pathlib.Path("merged_logs")
UNSORTED_LOG_ENTRIES = [
    "12:59:28: [INFO] [foo1.py | foo1 | 43] Foo1 initialized\n",
    "13:00:04: [ERROR] [foo1.py | foo1 | 30] Foo1 could not be created\n",
    "13:00:22: [ERROR] [foo1.py | foo1 | 49] Foo1 failed to create class object\n",
    "12:59:40: [INFO] [foo2.py | foo2 | 43] Foo2 initialized\n",
    "13:00:06: [ERROR] [foo2.py | foo2 | 30] Foo2 could not be created\n",
    "13:00:09: [ERROR] [foo2.py | foo2 | 49] Foo2 failed to create class object\n",
    "12:59:59: [INFO] [foo3.py | foo3 | 43] Foo3 initialized\n",
    "13:00:12: [ERROR] [foo3.py | foo3 | 30] Foo3 could not be created\n",
    "13:00:30: [ERROR] [foo3.py | foo3 | 49] Foo3 failed to create class object\n",
]
SORTED_LOG_ENTRIES = [
    "12:59:28: [INFO] [foo1.py | foo1 | 43] Foo1 initialized\n",
    "12:59:40: [INFO] [foo2.py | foo2 | 43] Foo2 initialized\n",
    "12:59:59: [INFO] [foo3.py | foo3 | 43] Foo3 initialized\n",
    "13:00:04: [ERROR] [foo1.py | foo1 | 30] Foo1 could not be created\n",
    "13:00:06: [ERROR] [foo2.py | foo2 | 30] Foo2 could not be created\n",
    "13:00:09: [ERROR] [foo2.py | foo2 | 49] Foo2 failed to create class object\n",
    "13:00:12: [ERROR] [foo3.py | foo3 | 30] Foo3 could not be created\n",
    "13:00:22: [ERROR] [foo1.py | foo1 | 49] Foo1 failed to create class object\n",
    "13:00:30: [ERROR] [foo3.py | foo3 | 49] Foo3 failed to create class object\n",
]


@pytest.fixture(name="temp_path")
def fixture_temp_path() -> pathlib.Path:  # type: ignore
    """
    Returns the path to a temporary log directory with dummy log subdirectories.
    """
    # Create a temporary logs directory
    temp_logs_path = TEMP_LOGS_DIRECTORY
    temp_logs_path.mkdir(parents=True, exist_ok=True)

    # Create sample directories with timestamped names
    (temp_logs_path / "2024-10-10_10-00-00").mkdir()
    (temp_logs_path / "2024-10-11_10-00-00").mkdir()
    (temp_logs_path / "2024-10-09_10-00-00").mkdir()

    yield temp_logs_path

    # Remove the temporary logs directory
    shutil.rmtree(temp_logs_path)


@pytest.fixture(name="dummy_logs")
def fixture_dummy_logs() -> pathlib.Path:  # type: ignore
    """
    Returns the path to a temporary directory with dummy log files.
    """
    subdirectory = TEMP_LOGS_DIRECTORY / "subdirectory"
    subdirectory.mkdir(parents=True, exist_ok=True)

    # Create three dummy log files in the subdirectory
    log_file_1 = subdirectory / "log1.log"
    log_file_2 = subdirectory / "log2.log"
    log_file_3 = subdirectory / "log3.log"

    log_file_1.write_text(
        "12:59:28: [INFO] [foo1.py | foo1 | 43] Foo1 initialized\n"
        "13:00:04: [ERROR] [foo1.py | foo1 | 30] Foo1 could not be created\n"
        "13:00:22: [ERROR] [foo1.py | foo1 | 49] Foo1 failed to create class object\n",
        encoding="utf-8",
    )

    log_file_2.write_text(
        "12:59:40: [INFO] [foo2.py | foo2 | 43] Foo2 initialized\n"
        "13:00:06: [ERROR] [foo2.py | foo2 | 30] Foo2 could not be created\n"
        "13:00:09: [ERROR] [foo2.py | foo2 | 49] Foo2 failed to create class object\n",
        encoding="utf-8",
    )

    log_file_3.write_text(
        "12:59:59: [INFO] [foo3.py | foo3 | 43] Foo3 initialized\n"
        "13:00:12: [ERROR] [foo3.py | foo3 | 30] Foo3 could not be created\n"
        "13:00:30: [ERROR] [foo3.py | foo3 | 49] Foo3 failed to create class object\n",
        encoding="utf-8",
    )

    return subdirectory


class TestLogFileMerger:
    """
    Test suite for the log file merger.
    """

    def test_get_current_log_directory(self, temp_path: pathlib.Path) -> None:
        """
        Test successful retrieval of the most recent run directory.
        """
        # Use the fixture to get the temporary directory with the sample structure
        temp_logs_path = temp_path

        # Define the datetime format used in the folder names
        file_datetime_format = "%Y-%m-%d_%H-%M-%S"

        # Call the function and get the result
        success, current_run_directory = log_file_merger.get_current_run_directory(
            temp_logs_path, file_datetime_format
        )

        # Assertions
        assert success
        assert current_run_directory == temp_logs_path / "2024-10-11_10-00-00"

    def test_read_log_files(self, dummy_logs: "list[str]") -> None:
        """
        Test correct reading of log files.
        """
        # Read log files in subdirectory and get the combined, unsorted list of log entries
        result, log_entries = log_file_merger.read_log_files(dummy_logs)

        assert result
        assert log_entries == UNSORTED_LOG_ENTRIES

    def test_sort_log_files(self) -> None:
        """
        Test correct sorting of log files.
        """
        # Read log files in subdirectory and get the combined, unsorted list of log entries
        result, sorted_log_entries = log_file_merger.sort_log_entries(UNSORTED_LOG_ENTRIES)

        assert result
        assert sorted_log_entries == SORTED_LOG_ENTRIES

    def test_write_merged_logs(self, temp_path: pathlib.Path) -> None:
        """
        Test writing the sorted log entries into the merged log file.
        """
        temp_logs_path = temp_path

        # Write the sorted log entries to the output file
        result, merged_log_file = log_file_merger.write_merged_logs(
            SORTED_LOG_ENTRIES, temp_logs_path
        )

        # Check if the function returned True (successful write)
        assert result

        # Verify the contents of the output file
        written_contents = merged_log_file.read_text(encoding="utf-8")

        # Create an expected output string
        expected_output = "".join(SORTED_LOG_ENTRIES)

        # Compare the written content with the expected output
        assert written_contents == expected_output
