"""
Merges log files.
"""

import pathlib
from datetime import datetime

from ..read_yaml.modules import read_yaml


MERGED_LOGS_FILENAME = pathlib.Path("merged_logs")


def read_configuration(
    config_file_path: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None, str | None]":
    """
    Reads the configuration YAML file and returns the log directory path and file datetime format.

    config_file_path: Path to the configuration YAML file.

    Returns: Success, log directory path, file datetime format.
    """
    # Open configuration settings
    result, config = read_yaml.open_config(config_file_path)
    if not result:
        print("ERROR: Failed to load configuration file")
        return False, None, None

    # Extract log directory path and file datetime format from configuration dictionary
    try:
        # Convert the directory_path string to a Path object
        log_directory_path = pathlib.Path(config["logger"]["directory_path"])
        file_datetime_format = config["logger"]["file_datetime_format"]
    except KeyError as exception:
        print(f"Config key(s) not found: {exception}")
        return False, None, None

    return True, log_directory_path, file_datetime_format


def get_current_run_directory(
    log_directory_path: pathlib.Path, file_datetime_format: str
) -> "tuple[bool, pathlib.Path | None]":
    """
    Retrieves the directory for the current log run, based on the most recent timestamped folder.

    log_directory_path: Path to the log directory.
    file_datetime_format: Datetime format in the filename.

    Returns: Success, path of the log directory of the most recent run.
    """
    # Creates a list of timestamped log directories in the root log directory
    log_directories = [entry for entry in log_directory_path.iterdir() if entry.is_dir()]
    if not log_directories:
        print(f"ERROR: There are no log directories in: {log_directory_path}")
        return False, None

    # Find the most recent log directory based on the timestamp in the directory name
    # The lambda function extracts the timestamp from the name of each directory and converts it to a datetime object
    # The max function returns the directory with the latest timestamp
    current_run_directory = max(
        log_directories, key=lambda entry: datetime.strptime(entry.name, file_datetime_format)
    )

    return True, current_run_directory


def read_log_files(log_file_directory: pathlib.Path) -> "tuple[bool, list[str] | None]":
    """
    Reads log files in the specified directory and returns a list with all of the log entries.

    log_file_directory: The directory containing log files to be read.

    Returns: Success, list of log entries.
    """
    # Get log files excluding merged logs
    log_files = [
        file
        for file in log_file_directory.iterdir()
        if file.suffix == ".log" and file.stem != MERGED_LOGS_FILENAME
    ]
    if not log_files:
        print(f"ERROR: No log files in directory: {log_file_directory}")
        return False, None

    # Read log entries from all log files
    log_entries = []
    for log_file in log_files:
        with log_file.open("r", encoding="utf-8") as file:
            log_entries.extend(file.readlines())
    if not log_entries:
        print(f"ERROR: No log entries found in any log files in directory: {log_file_directory}")
        return False, None

    return True, log_entries


def sort_log_entries(log_entries: "list[str]") -> "tuple[bool, list[str] | None]":
    """
    Returns a sorted list of log entries in chronological order.

    log_entries: An unsorted list of log entries.

    Returns: Success, sorted list of log entries.
    """
    # Sort the log entries based on the timestamp at the beginning of each entry
    # The lambda function extracts the timestamp from each entry and converts it to a datetime object for comparison
    sorted_log_entries = sorted(
        log_entries, key=lambda entry: datetime.strptime(entry.split(": ")[0], "%H:%M:%S")
    )
    if not sorted_log_entries:
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
    # Create the merged log file path
    merged_log_file = log_file_directory / f"{MERGED_LOGS_FILENAME}.log"

    # Write the log entries to the merged file
    with merged_log_file.open("w", encoding="utf-8") as file:
        file.writelines(sorted_log_entries)
    if not merged_log_file.exists():
        print("ERROR: Failed to create the merged log file")
        return False, None

    # Return the path of the created merged log file
    return True, merged_log_file


def main() -> int:
    """
    Main function that reads log files, sorts them, and writes them to a merged log file.

    Returns: Status code.
    """
    # Config file path
    config_file_path = pathlib.Path(__file__).parent / "config_logger.yaml"

    # Read the config file
    result, log_directory_path, file_datetime_format = read_configuration(config_file_path)
    if not result:
        print("ERROR: Failed to read config file")
        return -1

    # Get log directory for the current run
    result, current_run_directory = get_current_run_directory(
        log_directory_path, file_datetime_format
    )
    if not result:
        print("ERROR: Failed to get current run directory")
        return -1

    # Read log files in the directory
    result, log_entries = read_log_files(current_run_directory)
    if not result:
        print("ERROR: Failed to read log files")
        return -1

    # Sort log entries
    result, sorted_log_entries = sort_log_entries(log_entries)
    if not result:
        print("ERROR: Failed to sort log files")
        return -1

    # Write merged log file
    result, merged_file_path = write_merged_logs(sorted_log_entries, current_run_directory)
    if not result:
        print("ERROR: Failed to write merged log file")
        return -1

    print(f"Wrote merged logs to: {merged_file_path}")
    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
