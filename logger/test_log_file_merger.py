"""
Log file merger unit tests.
"""

import os
import tempfile
import shutil
import pytest


from .modules import log_file_merger


@pytest.fixture(name="dummy_logs")
def fixture_dummy_logs() -> str:  # type: ignore
    """
    Returns the path to a temporary directory with dummy log files.
    """
    temp_directory = tempfile.mkdtemp()
    subdirectory = os.path.join(temp_directory, "subdirectory")
    os.makedirs(subdirectory)

    # Create three dummy log files in the subdirectory
    log_file_1 = os.path.join(subdirectory, "log1.log")
    log_file_2 = os.path.join(subdirectory, "log2.log")
    log_file_3 = os.path.join(subdirectory, "log3.log")

    with open(log_file_1, "w", encoding="utf-8") as f:
        f.write("12:59:28: [INFO] [foo1.py | foo1 | 43] Foo1 initialized\n")
        f.write("13:00:04: [ERROR] [foo1.py | foo1 | 30] Foo1 could not be created\n")
        f.write("13:00:22: [ERROR] [foo1.py | foo1 | 49] Foo1 failed to create class object\n")

    with open(log_file_2, "w", encoding="utf-8") as f:
        f.write("12:59:40: [INFO] [foo2.py | foo2 | 43] Foo2 initialized\n")
        f.write("13:00:06: [ERROR] [foo2.py | foo2 | 30] Foo2 could not be created\n")
        f.write("13:00:09: [ERROR] [foo2.py | foo2 | 49] Foo2 failed to create class object\n")

    with open(log_file_3, "w", encoding="utf-8") as f:
        f.write("12:59:59: [INFO] [foo3.py | foo3 | 43] Foo3 initialized\n")
        f.write("13:00:12: [ERROR] [foo3.py | foo3 | 30] Foo3 could not be created\n")
        f.write("13:00:30: [ERROR] [foo3.py | foo3 | 49] Foo3 failed to create class object\n")

    yield temp_directory

    # Cleanup
    shutil.rmtree(temp_directory)


class TestLogFileMerger:
    """
    Test suite for the log file merger.
    """

    def test_merge_log_files(self, dummy_logs: str) -> None:
        """
        Test if merger correctly combines log files.
        """
        temp_directory = dummy_logs
        subdirectory = os.path.join(temp_directory, "subdirectory")

        # Merge log files in the subdirectory
        log_file_merger.merge_log_files(subdirectory)

        # Check if merged_logs.log is created
        merged_log_file = os.path.join(subdirectory, "merged_logs.log")
        assert os.path.exists(merged_log_file)

        # Check the contents of the merged log file
        with open(merged_log_file, "r", encoding="utf-8") as f:
            merged_logs = f.readlines()

        expected_logs = [
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

        assert merged_logs == expected_logs
