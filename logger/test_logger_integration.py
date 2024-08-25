"""
Integration tests for the logger.
"""

import inspect

from .modules import logger, logger_setup_main
from .read_yaml.modules import read_yaml


def main() -> int:
    """
    Main function.
    """
    # Load configuration
    result, config = read_yaml.open_config(logger.CONFIG_FILE_PATH)
    if not result:
        print("ERROR: Failed to load configuration file")
        return -1

    result, test_logger_1, _ = logger_setup_main.setup_main_logger(config)
    if not result:
        print("ERROR: Failed to setup logger")
        return -2

    # test each log level
    test_logger_1.debug("Debug message 1", inspect.currentframe())
    test_logger_1.info("Info message 1", inspect.currentframe())
    test_logger_1.warning("Warning message 1", inspect.currentframe())
    test_logger_1.error("Error message 1", inspect.currentframe())
    test_logger_1.critical("Critical message 1", inspect.currentframe())

    result, test_logger_2, _ = logger_setup_main.setup_main_logger(config, "main_1")
    if not result:
        print("ERROR: Failed to setup logger")
        return -2

    # test each log level
    test_logger_2.debug("Debug message 2", inspect.currentframe())
    test_logger_2.info("Info message 2", inspect.currentframe())
    test_logger_2.warning("Warning message 2", inspect.currentframe())
    test_logger_2.error("Error message 2", inspect.currentframe())
    test_logger_2.critical("Critical message 2", inspect.currentframe())

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: main() failed with error code {result_main}")
    else:
        print("Success! main() exited with code 0")
