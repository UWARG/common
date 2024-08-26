"""
Test if read_yaml function correctly reads yaml files
"""

import os
import pathlib

from .modules import read_yaml


CURRENT_DIRECTORY = os.path.dirname(__file__)


class TestOpenConfig:
    """
    Test the open_config function
    """

    def test_open_config(self) -> None:
        """
        Test if the function correctly reads the yaml file
        """
        expected = {"config": "no_error"}

        result, actual = read_yaml.open_config(
            pathlib.Path(CURRENT_DIRECTORY, "config_test_files/config_no_error.yaml")
        )

        assert result
        assert actual == expected

    def test_open_config_file_not_found(self) -> None:
        """
        Test if the function handles file not found
        """
        expected = None

        result, actual = read_yaml.open_config(
            pathlib.Path(CURRENT_DIRECTORY, "config_test_files/config_nonexistant_file.yaml")
        )

        assert not result
        assert actual == expected
