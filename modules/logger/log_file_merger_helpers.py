"""
Log file merger helper functions.
"""

import datetime
import pathlib

from ..read_yaml import read_yaml


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

    if not log_directory_path.exists():
        print(f"No log directory exists at: {log_directory_path}")
        return False, None, None, None

    return True, log_directory_path, file_datetime_format, log_datetime_format


def get_log_run_directories(
    log_directory_path: pathlib.Path,
    file_datetime_format: str,
    include_directories_with_merged_logs: bool,
) -> "tuple[bool, list[pathlib.Path] | None]":
    """
    Retrieves the paths of log run directories.

    log_directory_path: Path to the log directory.
    file_datetime_format: Datetime format in the filename.
    include_directories_with_merged_logs: Includes directories that have merged log files.

    Returns: Success, list of paths of log run directories.
    """
    if not log_directory_path.exists():
        print(f"ERROR: Log directory does not exist: {log_directory_path}")
        return False, None

    log_run_directories = []
    for entry in log_directory_path.iterdir():
        if entry.is_dir():
            try:
                # Try to parse the directory name as a date using the given format
                datetime.datetime.strptime(entry.name, file_datetime_format)
            except ValueError:
                # Skip directories with invalid datetime format
                print(f"Skipping directory with invalid format: {entry.name}")
                continue

            # Check for the presence of merged logs
            merged_log_file_path = pathlib.Path(entry, MERGED_LOGS_FILENAME)
            if include_directories_with_merged_logs or not merged_log_file_path.exists():
                log_run_directories.append(entry)
            else:
                print(f"Excluding directory with existing merged logs file: {entry.name}")

    if len(log_run_directories) == 0:
        print(f"ERROR: There are no eligible log directories in: {log_directory_path}")
        return False, None

    log_run_directories.sort()

    return True, log_run_directories


def read_log_files(
    log_file_directory: pathlib.Path, log_datetime_format: str
) -> "tuple[bool, list[str] | None]":
    """
    Reads log files in the specified directory and returns a list with all of the log entries.

    log_file_directory: The directory containing log files to be read.
    log_datetime_format: Datetime format in the log entries.

    Returns: Success, list of log entries.
    """
    if not log_file_directory.exists():
        print(f"ERROR: Log file directory does not exist: {log_file_directory}")
        return False, None

    # Get list of log files excluding merged logs
    # List is sorted to ensure they are always read in the same order
    log_files = sorted(
        file
        for file in log_file_directory.iterdir()
        if file.is_file() and file.suffix == LOG_FILE_SUFFIX and file.name != MERGED_LOGS_FILENAME
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
                        datetime.datetime.strptime(line.split(": ")[0], log_datetime_format)
                        log_entries.append(line)
                    except ValueError:
                        # Skip lines that do not match the format
                        print(f"WARNING: Skipping invalid log entry: {line.strip()}")
        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            # Skip files that cannot be opened
            print(f"ERROR: Failed to read log file: {log_file}, exception: {exception}")

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
    if len(log_entries) == 0:
        print("ERROR: No log entries passed to sort function")
        return False, None

    # Sort the log entries based on the timestamp at the beginning of each entry
    # The lambda function extracts the timestamp from each entry and converts it to a datetime object for comparison
    sorted_log_entries = sorted(
        log_entries,
        key=lambda entry: datetime.datetime.strptime(entry.split(": ")[0], log_datetime_format),
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
    if len(sorted_log_entries) == 0:
        print("ERROR: No log entries passed to write function")
        return False, None

    if not log_file_directory.exists():
        print(f"ERROR: Log file directory does not exist: {log_file_directory}")
        return False, None

    merged_log_file = pathlib.Path(log_file_directory, MERGED_LOGS_FILENAME)

    try:
        with merged_log_file.open("w", encoding="utf-8") as file:
            file.writelines(sorted_log_entries)
    # Catching all exceptions for library call
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(
            f"ERROR: Failed to create the merged log file: {merged_log_file}, exception: {exception}"
        )
        return False, None

    if not merged_log_file.exists():
        print(f"ERROR: Failed to create the merged log file: {merged_log_file}")
        return False, None

    return True, merged_log_file
