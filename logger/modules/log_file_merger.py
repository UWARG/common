"""
Merges log files.
"""

import pathlib

from . import log_file_merger_helpers


CONFIG_FILE_PATH = pathlib.Path(pathlib.Path(__file__).parent, "config_logger.yaml")


def main() -> int:
    """
    Main function that reads log files, sorts them, and writes them to a merged log file.

    Returns: Status code.
    """
    # Read the config file
    result, log_directory_path, file_datetime_format, log_datetime_format = (
        log_file_merger_helpers.read_configuration(CONFIG_FILE_PATH)
    )
    if not result:
        print("ERROR: Failed to read config file")
        return -1

    # Get log directory for the latest run
    result, latest_run_directory = log_file_merger_helpers.get_directory_of_latest_run(
        log_directory_path, file_datetime_format
    )
    if not result:
        print("ERROR: Failed to get latest run directory")
        return -1

    # Read log files in the directory
    result, log_entries = log_file_merger_helpers.read_log_files(
        latest_run_directory, log_datetime_format
    )
    if not result:
        print("ERROR: Failed to read log files")
        return -1

    # Sort log entries
    result, sorted_log_entries = log_file_merger_helpers.sort_log_entries(
        log_entries, log_datetime_format
    )
    if not result:
        print("ERROR: Failed to sort log files")
        return -1

    # Write merged log file
    result, merged_file_path = log_file_merger_helpers.write_merged_logs(
        sorted_log_entries, latest_run_directory
    )
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
