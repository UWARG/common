"""
Test if read_yaml function correctly reads yaml files
"""

import pathlib

from modules.read_yaml import read_yaml


PARENT_DIRECTORY = pathlib.Path("tests", "unit", "read_yaml_configs")


class TestOpenConfig:
    """
    Test the open_config function
    """

    def test_open_config(self) -> None:
        """
        Test if the function correctly reads the yaml file
        """
        config_file_name = "config_no_error.yaml"

        expected = {"config": "no_error"}

        result, actual = read_yaml.open_config(pathlib.Path(PARENT_DIRECTORY, config_file_name))

        assert result
        assert actual == expected

    def test_open_config_file_not_found(self) -> None:
        """
        Test if the function handles file not found
        """
        config_file_name = "config_nonexistent_file.yaml"

        result, actual = read_yaml.open_config(pathlib.Path(PARENT_DIRECTORY, config_file_name))

        assert not result
        assert actual is None
