"""
Merges log files.
"""

import os
import pathlib
from datetime import datetime

from ..read_yaml.modules import read_yaml

CONFIG_FILE_PATH = pathlib.Path(os.path.dirname(__file__), "config_logger.yaml")
MERGED_LOGS_FILENAME = "merged_logs"


def merge_log_files(log_file_directory: str) -> None:
    """
    Reads, sorts, and writes log files in the specified directory.

    log_file_directory: The directory containing the log files to be merged.
    """
    # Read log files
    log_files = [
        file
        for file in os.listdir(log_file_directory)
        if file.endswith(".log") and file != f"{MERGED_LOGS_FILENAME}.log"
    ]
    log_entries = []
    for log_file in log_files:
        with open(os.path.join(log_file_directory, log_file), "r", encoding="utf-8") as file:
            log_entries.extend(file.readlines())

    # Sort log entries
    log_entries.sort(key=lambda entry: datetime.strptime(entry.split(": ")[0], "%H:%M:%S"))

    # Write merged logs
    merged_log_file = os.path.join(log_file_directory, f"{MERGED_LOGS_FILENAME}.log")
    with open(merged_log_file, "w", encoding="utf-8") as file:
        file.writelines(log_entries)


def get_current_run_directory() -> str:
    """
    Returns directory of current run.
    """
    # Configuration settings
    result, config = read_yaml.open_config(CONFIG_FILE_PATH)
    if not result:
        print("ERROR: Failed to load configuration file")

    try:
        log_directory_path = config["logger"]["directory_path"]
        file_datetime_format = config["logger"]["file_datetime_format"]
    except KeyError as exception:
        print(f"Config key(s) not found: {exception}")

    # Get the path to the logs directory
    entries = os.listdir(log_directory_path)

    if len(entries) == 0:
        print("ERROR: The directory for this log session was not found.")

    log_names = [
        entry for entry in entries if os.path.isdir(os.path.join(log_directory_path, entry))
    ]

    # Find the log directory for the current run, which is the most recent timestamp
    current_directory = max(
        log_names,
        key=lambda datetime_string: datetime.strptime(datetime_string, file_datetime_format),
    )

    return os.path.join(log_directory_path, current_directory)


if __name__ == "__main__":
    current_run_directory = get_current_run_directory()
    merge_log_files(current_run_directory)
