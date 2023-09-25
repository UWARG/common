"""
Test Process.
"""
import pathlib

import pytest

from modules import waypoints_to_kml


EXPECTED_KML_DOCUMENT_NAME = "expected_document.kml"


@pytest.fixture
def waypoints():
    return [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)]


def test_waypoints_to_kml_with_save_path(waypoints: "list[tuple[float, float]]",
                                         tmp_path: pathlib.Path):
    """
    Basic test case to save KML to the correct path when provided.
    """
    actual_document_name = "actual_kml_document"

    # Build a temporary directory using tmp_path so the KML files are cleaned after the tests are run
    tmp_path.mkdir(parents=True, exist_ok=True)

    result = waypoints_to_kml.waypoints_to_kml(waypoints, actual_document_name, tmp_path)

    # Assert success
    assert result

    # Define the path to the generated KML file
    kml_file_path = pathlib.Path(tmp_path, f"{actual_document_name}.kml")

    # Assert that the KML file has been generated properly in the provided path
    assert kml_file_path.exists()
    assert kml_file_path.suffix == ".kml"

    # Get the directory where the test file is located
    test_directory = pathlib.Path(__file__).parent

    # Define the path to the static KML file for comparison (relative to the test file directory)
    static_kml_path = test_directory / EXPECTED_KML_DOCUMENT_NAME

    # Compare the contents of the generated KML file with the static KML file
    assert kml_file_path.read_text() == static_kml_path.read_text()
