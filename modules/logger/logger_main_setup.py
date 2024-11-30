"""
Logger setup for `main()` .
"""

import datetime
import pathlib

from . import logger


MAIN_LOGGER_NAME = "main"

MAX_ATTEMPTS = 3


def setup_main_logger(
    config: "dict", main_logger_name: str = MAIN_LOGGER_NAME, enable_log_to_file: bool = True
) -> "tuple[bool, logger.Logger | None, pathlib.Path | None]":
    """
    Setup prerequisites for logging in `main()` .

    config: The configuration.

    Returns: Success, logger, logger path.
    """
    # Get settings
    try:
        log_directory_path = config["logger"]["directory_path"]
        log_path_format = config["logger"]["file_datetime_format"]
    except KeyError as exception:
        print(f"ERROR: Config key(s) not found: {exception}")
        return False, None, None

    # Create logging directory
    start_time = datetime.datetime.now()
    success = False
    for i in range(0, MAX_ATTEMPTS):
        offset = datetime.timedelta(seconds=i)
        logging_path = pathlib.Path(
            log_directory_path, (start_time + offset).strftime(log_path_format)
        )
        if not logging_path.exists():
            success = True
            break

    if not success:
        print("ERROR: Could not create new log directory")

    logging_path.mkdir(exist_ok=False, parents=True)

    # Setup logger
    result, main_logger = logger.Logger.create(main_logger_name, enable_log_to_file)
    if not result:
        print("ERROR: Failed to create main logger")
        return False, None, None

    # Get Pylance to stop complaining
    assert main_logger is not None

    main_logger.info(f"{main_logger_name} logger initialized", True)

    return True, main_logger, logging_path
