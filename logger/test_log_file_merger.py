"""
Log file merger unit tests.
"""

import pathlib
import pytest

from .modules import log_file_merger_helpers


FILE_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_DATETIME_FORMAT = "%H:%M:%S"
LOG_ENRIES_1 = [
    "12:59:28: [INFO] [foo1.py | foo1 | 43] Foo1 initialized\n",
    "13:00:04: [ERROR] [foo1.py | foo1 | 30] Foo1 could not be created\n",
    "13:00:22: [ERROR] [foo1.py | foo1 | 49] Foo1 failed to create class object\n",
]
LOG_ENRIES_2 = [
    "12:59:40: [INFO] [foo2.py | foo2 | 43] Foo2 initialized\n",
    "13:00:06: [ERROR] [foo2.py | foo2 | 30] Foo2 could not be created\n",
    "13:00:09: [ERROR] [foo2.py | foo2 | 49] Foo2 failed to create class object\n",
]
LOG_ENRIES_3 = [
    "12:59:59: [INFO] [foo3.py | foo3 | 43] Foo3 initialized\n",
    "13:00:12: [ERROR] [foo3.py | foo3 | 30] Foo3 could not be created\n",
    "13:00:30: [ERROR] [foo3.py | foo3 | 49] Foo3 failed to create class object\n",
]
# Invalid lines should be ignored by function
LOG_ENRIES_4 = [
    "",
    "\n",
    "[INFO] [foo1.py | foo1 | 43] Foo1 initialized\n",
    "invalid line\n",
]
UNSORTED_LOG_ENTRIES = LOG_ENRIES_1 + LOG_ENRIES_2 + LOG_ENRIES_3
SORTED_LOG_ENTRIES = sorted(UNSORTED_LOG_ENTRIES)


@pytest.fixture(name="temp_log_directory")
def fixture_temp_log_directories(tmp_path: pathlib.Path) -> pathlib.Path:  # type: ignore
    """
    Returns the path to a temporary log directory with dummy log subdirectories.
    """
    # Create sample directories with timestamped names
    pathlib.Path(tmp_path, "2024-10-10_10-00-00").mkdir(parents=True, exist_ok=True)
    pathlib.Path(tmp_path, "2024-10-09_10-00-00").mkdir(parents=True, exist_ok=True)
    pathlib.Path(tmp_path, "2024-10-08_10-00-00").mkdir(parents=True, exist_ok=True)
    # Invalid directory should be ignored by function
    pathlib.Path(tmp_path, "invalid-directory").mkdir(parents=True, exist_ok=True)

    yield tmp_path


@pytest.fixture(name="dummy_logs")
def fixture_dummy_logs(tmp_path: pathlib.Path) -> pathlib.Path:  # type: ignore
    """
    Returns the path to a temporary log directory with dummy log files.
    """
    # Create dummy log files
    log_file_1 = pathlib.Path(tmp_path, "log1.log")
    log_file_2 = pathlib.Path(tmp_path, "log2.log")
    log_file_3 = pathlib.Path(tmp_path, "log3.log")
    log_file_4 = pathlib.Path(tmp_path, "log4.log")

    # Write to dummy log files
    log_file_1.write_text(
        "".join(LOG_ENRIES_1),
        encoding="utf-8",
    )
    log_file_2.write_text(
        "".join(LOG_ENRIES_2),
        encoding="utf-8",
    )
    log_file_3.write_text(
        "".join(LOG_ENRIES_3),
        encoding="utf-8",
    )
    log_file_4.write_text(
        "".join(LOG_ENRIES_4),
        encoding="utf-8",
    )

    yield tmp_path


class TestLogFileMerger:
    """
    Test suite for the log file merger.
    """

    def test_get_current_log_directory(self, temp_log_directory: pathlib.Path) -> None:
        """
        Test successful retrieval of the most recent run directory.
        """
        # Expected output
        actual_directory = pathlib.Path(temp_log_directory, "2024-10-10_10-00-00")

        # Call the function and get the result
        result, current_run_directory = log_file_merger_helpers.get_directory_of_latest_run(
            temp_log_directory, FILE_DATETIME_FORMAT
        )

        # Assertions
        assert result
        assert current_run_directory is not None
        assert current_run_directory == actual_directory

    def test_get_directory_of_latest_run_empty_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Test get_directory_of_latest_run in an empty directory.
        """
        # Call the function with an empty temporary directory as an argument
        result, latest_run_directory = log_file_merger_helpers.get_directory_of_latest_run(
            tmp_path, FILE_DATETIME_FORMAT
        )

        # Assertions
        assert not result
        assert latest_run_directory is None

    def test_read_log_files(self, dummy_logs: pathlib.Path) -> None:
        """
        Test correct reading of log files.
        """
        # Read log files in subdirectory and get the combined, unsorted list of log entries
        result, log_entries = log_file_merger_helpers.read_log_files(
            dummy_logs, LOG_DATETIME_FORMAT
        )

        # Assertions
        assert result
        assert log_entries is not None
        assert log_entries == UNSORTED_LOG_ENTRIES

    def test_read_log_files_empty_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files in an empty directory.
        """
        # Call the function and get the result
        result, log_entries = log_file_merger_helpers.read_log_files(tmp_path, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert log_entries is None

    def test_read_log_files_empty_log_files(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files with empty log files.
        """
        # Create an empty log file in the temp directory
        log_file = pathlib.Path(tmp_path, "log.log")
        log_file.write_text("", encoding="utf-8")

        # Call the function and get the result
        result, log_entries = log_file_merger_helpers.read_log_files(tmp_path, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert log_entries is None

    def test_sort_log_files(self) -> None:
        """
        Test correct sorting of log files.
        """
        # Read log files in subdirectory and get the combined, unsorted list of log entries
        result, sorted_log_entries = log_file_merger_helpers.sort_log_entries(
            UNSORTED_LOG_ENTRIES, LOG_DATETIME_FORMAT
        )

        # Assertions
        assert result
        assert sorted_log_entries is not None
        assert sorted_log_entries == SORTED_LOG_ENTRIES

    def test_sort_log_entries_empty_input(self) -> None:
        """
        Test sort_log_entries with empty input list.
        """
        # Call the function with an empty list as an argument
        result, sorted_log_entries = log_file_merger_helpers.sort_log_entries(
            [], LOG_DATETIME_FORMAT
        )

        # Assertions
        assert not result
        assert sorted_log_entries is None

    def test_write_merged_logs(self, tmp_path: pathlib.Path) -> None:
        """
        Test writing the sorted log entries into the merged log file.
        """
        # Expected output
        actual_merged_log_file_contents = "".join(SORTED_LOG_ENTRIES)

        # Write the sorted log entries to the output file
        result, merged_log_file = log_file_merger_helpers.write_merged_logs(
            SORTED_LOG_ENTRIES, tmp_path
        )
        merged_log_file_contents = merged_log_file.read_text(encoding="utf-8")

        # Assertions
        assert result
        assert merged_log_file is not None
        assert merged_log_file.exists()
        assert merged_log_file_contents == actual_merged_log_file_contents
