import os
from pathlib import Path

import pytest

from modules import waypoints_to_kml


@pytest.fixture
def waypoints():
    return [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)]


def test_waypoints_to_kml_with_save_path(waypoints, tmp_path):
    """
    Basic test case to save KML to the correct path when provided.
    """
    actual_document_name = "actual_kml_document"

    # Build a temporary directory using tmp_path so the KML files are cleaned after the tests are run
    save_path = tmp_path / "path" / "to" / "save"
    save_path.mkdir(parents=True, exist_ok=True)

    kml_status_success = waypoints_to_kml.waypoints_to_kml(waypoints, actual_document_name, save_path)

    # Assert that the operation was a success
    assert kml_status_success is True

    # Define the path to the generated KML file
    kml_file_path = save_path / f'{actual_document_name}.kml'

    # Assert that the KML file has been generated properly in the provided path
    assert kml_file_path.exists()
    assert kml_file_path.suffix == ".kml"

    # Get the directory where the test file is located
    test_directory = Path(__file__).parent

    # Define the path to the static KML file for comparison (relative to the test file directory)
    static_kml_path = test_directory / "expected_document.kml"

    # Compare the contents of the generated KML file with the static KML file
    assert kml_file_path.read_text() == static_kml_path.read_text()
