"""
Log file merger helper functions.
"""

import pathlib
from datetime import datetime

from ..read_yaml.modules import read_yaml


MERGED_LOGS_FILENAME = "merged_logs.log"
LOG_FILE_SUFFIX = ".log"


def read_configuration(
    config_file_path: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None, str | None, str | None]":
    """
    Reads the configuration YAML file and returns the log directory path and file datetime format.

    config_file_path: Path to the configuration YAML file.

    Returns: Success, log directory path, file datetime format, log datetime format.
    """
    # Open configuration settings
    result, config = read_yaml.open_config(config_file_path)
    if not result:
        print(f"ERROR: Failed to load configuration file: {config_file_path}")
        return False, None, None, None

    # Extract log directory path and file datetime format from configuration dictionary
    try:
        log_directory_path_config = config["logger"]["directory_path"]
        # Convert the directory_path string to a Path object
        log_directory_path = pathlib.Path(log_directory_path_config)
        file_datetime_format = config["logger"]["file_datetime_format"]
        log_datetime_format = config["logger"]["log_datetime_format"]
    except KeyError as exception:
        print(f"Config key(s) not found: {exception}")
        return False, None, None, None

    # Check if the log directory exists
    if not log_directory_path.exists():
        print(f"No log directory exists at: {log_directory_path}")
        return False, None, None, None

    return True, log_directory_path, file_datetime_format, log_datetime_format


def get_directory_of_specified_run(
    log_directory_path: pathlib.Path, specified_directory_name: str
) -> "tuple[bool, pathlib.Path | None]":
    """
    Retrieves the directory for a specified run.

    log_directory_path: Path to the log directory.
    specified_directory_name: Name of directory for a specified run.

    Returns: Success, path of the log directory of the specified run.
    """
    # Check if log directory exists
    if not log_directory_path.exists():
        return False, None

    # Construct the full path to the specified directory
    specified_directory_path = pathlib.Path(log_directory_path, specified_directory_name)

    # Check if the path exists
    if not specified_directory_path.exists():
        return False, None

    # Check if the path is a directory
    if not specified_directory_path.is_dir():
        return False, None

    return True, specified_directory_path


def get_directory_of_latest_run(
    log_directory_path: pathlib.Path, file_datetime_format: str
) -> "tuple[bool, pathlib.Path | None]":
    """
    Retrieves the directory for the latest log run, based on the most recent timestamped folder.

    log_directory_path: Path to the log directory.
    file_datetime_format: Datetime format in the filename.

    Returns: Success, path of the log directory of the latest run.
    """
    # Check if log directory exists
    if not log_directory_path.exists():
        return False, None

    # Creates a list of timestamped log directories in the root log directory
    log_directories = []
    for entry in log_directory_path.iterdir():
        if entry.is_dir():
            try:
                # Try to parse the directory name as a date using the given format
                datetime.strptime(entry.name, file_datetime_format)
                log_directories.append(entry)
            except ValueError:
                # Skip directories with invalid datetime format
                print(f"Skipping directory with invalid format: {entry.name}")

    if len(log_directories) == 0:
        print(f"ERROR: There are no log directories in: {log_directory_path}")
        return False, None

    # Find the most recent log directory based on the timestamp in the directory name
    # The lambda function extracts the timestamp from the name of each directory and converts it to a datetime object
    # The max function returns the directory with the latest timestamp (latest timestamp > earlier timestamp)
    latest_run_directory = max(
        log_directories, key=lambda entry: datetime.strptime(entry.name, file_datetime_format)
    )

    return True, latest_run_directory


def read_log_files(
    log_file_directory: pathlib.Path, log_datetime_format: str
) -> "tuple[bool, list[str] | None]":
    """
    Reads log files in the specified directory and returns a list with all of the log entries.

    log_file_directory: The directory containing log files to be read.
    log_datetime_format: Datetime format in the log entries.

    Returns: Success, list of log entries.
    """
    # Check if log directory exists
    if not log_file_directory.exists():
        return False, None

    # Get list of log files excluding merged logs
    # List is sorted to ensure they are always read in the same order
    log_files = sorted(
        file
        for file in log_file_directory.iterdir()
        if file.suffix == LOG_FILE_SUFFIX and file.name != MERGED_LOGS_FILENAME
    )

    if len(log_files) == 0:
        print(f"ERROR: No log files in directory: {log_file_directory}")
        return False, None

    # Read log entries from all log files
    log_entries = []
    for log_file in log_files:
        try:
            with log_file.open("r", encoding="utf-8") as file:
                for line in file:
                    try:
                        # Attempt to parse the timestamp to ensure it matches the format
                        datetime.strptime(line.split(": ")[0], log_datetime_format)
                        log_entries.append(line)
                    except ValueError:
                        # Skip lines that do not match the format
                        print(f"WARNING: Skipping invalid log entry: {line.strip()}")
        except OSError:
            # Skip files that cannot be opened
            print(f"ERROR: Failed to read log file: {log_file}")

    if len(log_entries) == 0:
        print(f"ERROR: No log entries found in any log files in directory: {log_file_directory}")
        return False, None

    return True, log_entries


def sort_log_entries(
    log_entries: "list[str]", log_datetime_format: str
) -> "tuple[bool, list[str] | None]":
    """
    Returns a sorted list of log entries in chronological order.

    log_entries: An unsorted list of log entries.
    log_datetime_format: Datetime format in the log entries.

    Returns: Success, sorted list of log entries.
    """
    # Check that log entries is not empty
    if len(log_entries) == 0:
        print("ERROR: No log entries passed to sort function")
        return False, None

    # Sort the log entries based on the timestamp at the beginning of each entry
    # The lambda function extracts the timestamp from each entry and converts it to a datetime object for comparison
    sorted_log_entries = sorted(
        log_entries, key=lambda entry: datetime.strptime(entry.split(": ")[0], log_datetime_format)
    )

    if len(sorted_log_entries) == 0:
        print("ERROR: Failed to sort log entries")
        return False, None

    return True, sorted_log_entries


def write_merged_logs(
    sorted_log_entries: "list[str]", log_file_directory: pathlib.Path
) -> "tuple[bool, pathlib.Path | None]":
    """
    Writes sorted logs to a logfile and returns the filepath.

    sorted_log_entries: An sorted list of log entries.
    log_file_directory: The directory where the merged log file will be written.

    Returns: Success, path to merged log file.
    """
    # Check that sorted log entries is not empty
    if len(sorted_log_entries) == 0:
        print("ERROR: No log entries passed to write function")
        return False, None

    # Create the merged log file path
    merged_log_file = pathlib.Path(log_file_directory, MERGED_LOGS_FILENAME)

    # Write the log entries to the merged file
    with merged_log_file.open("w", encoding="utf-8") as file:
        file.writelines(sorted_log_entries)

    if not merged_log_file.exists():
        print(f"ERROR: Failed to create the merged log file: {merged_log_file}")
        return False, None

    # Return the path of the created merged log file
    return True, merged_log_file
