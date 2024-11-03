"""
Reads log files, sorts them, and writes them to a merged log file.
"""

import argparse
import pathlib

from . import log_file_merger_helpers


CONFIG_FILE_PATH = pathlib.Path(pathlib.Path(__file__).parent, "config_logger.yaml")


def main() -> int:
    """
    Main function.
    """
    # Set up argument parser for the optional folder_name argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite", action="store_true", help="option to overwrite existing merged log files"
    )
    args = parser.parse_args()

    # Read the config file
    result, log_directory_path, file_datetime_format, log_datetime_format = (
        log_file_merger_helpers.read_configuration(CONFIG_FILE_PATH)
    )
    if not result:
        print(f"ERROR: Failed to read config file: {CONFIG_FILE_PATH}")
        return -1

    # Get log run directories
    result, log_run_directories = log_file_merger_helpers.get_log_run_directories(
        log_directory_path, file_datetime_format, args.overwrite
    )
    if not result:
        print(f"ERROR: Failed to get log run directories in: {log_directory_path}")
        return -1

    log_run_directories_count = len(log_run_directories)
    print(f"Writing merged logs in {log_run_directories_count} directories")

    # Read, sort and write for each log run directory
    for index, log_run_directory in enumerate(log_run_directories):
        print(
            f"Writing merged logs for {log_run_directory} ({index + 1}/{log_run_directories_count})"
        )

        # Read log files in the log run directories
        result, log_entries = log_file_merger_helpers.read_log_files(
            log_run_directory, log_datetime_format
        )
        if not result:
            print(f"ERROR: Failed to read log files in: {log_run_directory}")
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
            sorted_log_entries, log_run_directory
        )
        if not result:
            print("ERROR: Failed to write merged log file")
            return -1

        print(f"Wrote merged logs to: {merged_file_path}")

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
