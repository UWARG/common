"""
Test Process.
"""
import pathlib

import pytest

from modules import waypoints_to_kml


EXPECTED_KML_DOCUMENT_NAME = "expected_document.kml"


@pytest.fixture
def waypoints():
    """
    Waypoints input.
    """
    return [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)]


def test_waypoints_to_kml_with_save_path(waypoints: "list[tuple[float, float]]",
                                         tmp_path: pathlib.Path):
    """
    Basic test case to save KML to the correct path when provided.
    """
    actual_kml_document_name = "actual_kml_document"

    # Build a temporary directory using tmp_path so
    # the KML files are cleaned after the tests are run
    tmp_path.mkdir(parents=True, exist_ok=True)

    result, actual_kml_file_path = waypoints_to_kml.waypoints_to_kml(
        waypoints,
        actual_kml_document_name,
        tmp_path,
    )

    # Assert success
    assert result
    assert actual_kml_file_path is not None

    # Assert that the KML file has been generated properly in the provided path
    assert actual_kml_file_path.exists()
    assert actual_kml_file_path.suffix == ".kml"

    # Define the path to the static KML file for comparison
    expected_kml_file_path = pathlib.Path(EXPECTED_KML_DOCUMENT_NAME)

    # Compare the contents of the generated KML file with the static KML file
    assert actual_kml_file_path.read_text(encoding="utf-8") \
        == expected_kml_file_path.read_text(encoding="utf-8")
