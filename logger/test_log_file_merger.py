"""
Log file merger unit tests.
"""

import pathlib

import pytest

from .modules import log_file_merger_helpers


FILE_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_DATETIME_FORMAT = "%H:%M:%S"
MERGED_LOGS_FILENAME = "merged_logs.log"
LOG_FILE_SUFFIX = ".log"
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
INVALID_LOG_ENTRIES = [
    "",
    "\n",
    "[INFO] [foo1.py | foo1 | 43] Foo1 initialized\n",
    "invalid line\n",
]
UNSORTED_LOG_ENTRIES = LOG_ENRIES_1 + LOG_ENRIES_2 + LOG_ENRIES_3
SORTED_LOG_ENTRIES = sorted(UNSORTED_LOG_ENTRIES)


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access, redefined-outer-name


@pytest.fixture
def temp_log_directory(tmp_path: pathlib.Path) -> pathlib.Path:  # type: ignore
    """
    Returns the path to a temporary log directory with dummy log subdirectories with some containing dummy merged log files.
    """
    # Create sample directories with timestamped names
    directory_1 = pathlib.Path(tmp_path, "2024-10-08_10-00-00")
    directory_2 = pathlib.Path(tmp_path, "2024-10-09_10-00-00")
    directory_3 = pathlib.Path(tmp_path, "2024-10-10_10-00-00")
    # Directory that does not follow timestamp name convention
    directory_4 = pathlib.Path(tmp_path, "invalid-directory")

    directory_1.mkdir(parents=True, exist_ok=True)
    directory_2.mkdir(parents=True, exist_ok=True)
    directory_3.mkdir(parents=True, exist_ok=True)
    directory_4.mkdir(parents=True, exist_ok=True)

    # Create dummy merged_logs.log files in some directories
    pathlib.Path(directory_2, MERGED_LOGS_FILENAME).touch()
    pathlib.Path(directory_3, MERGED_LOGS_FILENAME).touch()

    yield tmp_path


@pytest.fixture
def dummy_logs(tmp_path: pathlib.Path) -> pathlib.Path:  # type: ignore
    """
    Returns the path to a temporary log directory with dummy log files.
    """
    log_file_1 = pathlib.Path(tmp_path, f"log1{LOG_FILE_SUFFIX}")
    log_file_2 = pathlib.Path(tmp_path, f"log2{LOG_FILE_SUFFIX}")
    log_file_3 = pathlib.Path(tmp_path, f"log3{LOG_FILE_SUFFIX}")
    log_file_4 = pathlib.Path(tmp_path, f"log4{LOG_FILE_SUFFIX}")

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
        "".join(INVALID_LOG_ENTRIES),
        encoding="utf-8",
    )

    # Confirm that data was written (i.e. the file size is non-zero)
    assert log_file_1.stat().st_size > 0, f"ERROR: Failed to write to {log_file_1}"
    assert log_file_2.stat().st_size > 0, f"ERROR: Failed to write to {log_file_2}"
    assert log_file_3.stat().st_size > 0, f"ERROR: Failed to write to {log_file_3}"
    assert log_file_4.stat().st_size > 0, f"ERROR: Failed to write to {log_file_4}"

    yield tmp_path


class TestGetLogRunDirectories:
    """
    Test suite for get_log_run_directories.
    """

    def test_get_log_run_directories(self, temp_log_directory: pathlib.Path) -> None:
        """
        Test successful retrieval of log directories.
        """
        # Expected output
        expected = [
            pathlib.Path(temp_log_directory, "2024-10-08_10-00-00"),
        ]

        override = False

        # Call the function and get the result
        result, actual = log_file_merger_helpers.get_log_run_directories(
            temp_log_directory, FILE_DATETIME_FORMAT, override
        )

        # Assertions
        assert result
        assert actual is not None
        assert actual == expected

    def test_get_log_run_directories_override(self, temp_log_directory: pathlib.Path) -> None:
        """
        Test successful override of get_log_run_directories.
        """
        # Expected output
        expected = [
            pathlib.Path(temp_log_directory, "2024-10-08_10-00-00"),
            pathlib.Path(temp_log_directory, "2024-10-09_10-00-00"),
            pathlib.Path(temp_log_directory, "2024-10-10_10-00-00"),
        ]

        override = True

        # Call the function and get the result
        result, actual = log_file_merger_helpers.get_log_run_directories(
            temp_log_directory, FILE_DATETIME_FORMAT, override
        )

        # Assertions
        assert result
        assert actual is not None
        assert actual == expected

    def test_get_log_run_directories_empty_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Test get_log_run_directories in an empty directory.
        """
        override = False

        # Call the function with an empty temporary directory as an argument
        result, actual = log_file_merger_helpers.get_log_run_directories(
            tmp_path, FILE_DATETIME_FORMAT, override
        )

        # Assertions
        assert not result
        assert actual is None

    def test_get_log_run_directories_non_existent_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Test get_log_run_directories in a non-existent directory.
        """
        override = False

        non_existent_directory = pathlib.Path(tmp_path, "non_existent_directory")

        # Call the function with a non-existent directory as an argument
        result, actual = log_file_merger_helpers.get_log_run_directories(
            non_existent_directory, FILE_DATETIME_FORMAT, override
        )

        # Assertions
        assert not result
        assert actual is None


class TestReadLogFiles:
    """
    Test suite for read_log_files.
    """

    def test_read_log_files(self, dummy_logs: pathlib.Path) -> None:
        """
        Test correct reading of log files.
        """
        # Read log files in subdirectory and get the combined, unsorted list of log entries
        result, actual = log_file_merger_helpers.read_log_files(dummy_logs, LOG_DATETIME_FORMAT)

        # Assertions
        assert result
        assert actual is not None
        assert actual == UNSORTED_LOG_ENTRIES

    def test_read_log_files_empty_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files in an empty directory.
        """
        # Call the function and get the result
        result, actual = log_file_merger_helpers.read_log_files(tmp_path, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert actual is None

    def test_read_log_files_non_existent_directory(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files in an non-existent directory.
        """
        non_existent_directory = pathlib.Path(tmp_path, "non_existent_directory")

        # Call the function and get the result
        result, actual = log_file_merger_helpers.read_log_files(
            non_existent_directory, LOG_DATETIME_FORMAT
        )

        # Assertions
        assert not result
        assert actual is None

    def test_read_log_files_empty_log_files(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files with empty log files.
        """
        # Create an empty log file in the temp directory
        log_file = pathlib.Path(tmp_path, f"log{LOG_FILE_SUFFIX}")
        log_file.write_text("", encoding="utf-8")

        # Call the function and get the result
        result, actual = log_file_merger_helpers.read_log_files(tmp_path, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert actual is None

    def test_read_log_files_ignore_merged_logs(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files with merged_logs file in directory.
        """
        # Create a merged_logs file in the temp directory
        merged_log_file = pathlib.Path(tmp_path, MERGED_LOGS_FILENAME)
        merged_log_file.write_text("".join(SORTED_LOG_ENTRIES), encoding="utf-8")

        # Call the function and get the result
        result, actual = log_file_merger_helpers.read_log_files(tmp_path, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert actual is None

    def test_read_log_files_ignore_invalid_files(self, tmp_path: pathlib.Path) -> None:
        """
        Test read_log_files with invalid files.
        """
        # Create invalid log files in the temp directory
        invalid_log_file_1 = pathlib.Path(tmp_path, "log")
        invalid_log_file_1.write_text("".join(LOG_ENRIES_1), encoding="utf-8")
        invalid_log_file_2 = pathlib.Path(tmp_path, "log.txt")
        invalid_log_file_2.write_text("".join(LOG_ENRIES_2), encoding="utf-8")

        # Call the function and get the result
        result, actual = log_file_merger_helpers.read_log_files(tmp_path, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert actual is None


class TestSortLogEntries:
    """
    Test suite for sort_log_entries.
    """

    def test_sort_log_files(self) -> None:
        """
        Test correct sorting of log files.
        """
        # Read log files in subdirectory and get the combined, unsorted list of log entries
        result, actual = log_file_merger_helpers.sort_log_entries(
            UNSORTED_LOG_ENTRIES, LOG_DATETIME_FORMAT
        )

        # Assertions
        assert result
        assert actual is not None
        assert actual == SORTED_LOG_ENTRIES

    def test_sort_log_entries_empty_input(self) -> None:
        """
        Test sort_log_entries with empty input list.
        """
        empty_logs = []

        # Call the function with an empty list as an argument
        result, actual = log_file_merger_helpers.sort_log_entries(empty_logs, LOG_DATETIME_FORMAT)

        # Assertions
        assert not result
        assert actual is None


class TestWriteMergedLogs:
    """
    Test suite for write_merged_logs.
    """

    def test_write_merged_logs(self, tmp_path: pathlib.Path) -> None:
        """
        Test writing the sorted log entries into the merged log file.
        """
        # Expected output
        expected_contents = "".join(SORTED_LOG_ENTRIES)

        # Write the sorted log entries to the output file
        result, actual_file = log_file_merger_helpers.write_merged_logs(
            SORTED_LOG_ENTRIES, tmp_path
        )

        # Assertions
        assert result
        assert actual_file is not None
        assert actual_file.exists()

        # Compare contents of file
        actual_contents = actual_file.read_text(encoding="utf-8")
        assert actual_contents == expected_contents
