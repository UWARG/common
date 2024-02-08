"""
Test Process.
"""
import pathlib

import pytest

from kml.modules import ground_locations_to_kml
from kml.modules import location_ground


PARENT_DIRECTORY = "kml"
EXPECTED_KML_DOCUMENT_PATH = pathlib.Path(PARENT_DIRECTORY, "expected_document.kml")


@pytest.fixture
def waypoints():
    """
    Waypoints input.
    """
    return [
        location_ground.LocationGround("San Francisco", 37.7749, -122.4194), 
        location_ground.LocationGround("Los Angeles", 34.0522, -118.2437), 
        location_ground.LocationGround("New York City", 40.7128, -74.0060)
    ]


def test_waypoints_to_kml_with_save_path(waypoints: "list[location_ground.LocationGround]",
                                         tmp_path: pathlib.Path):
    """
    Basic test case to save KML to the correct path when provided.
    """
    actual_kml_document_name = "actual_kml_document"

    # Build a temporary directory using tmp_path so
    # the KML files are cleaned after the tests are run
    tmp_path.mkdir(parents=True, exist_ok=True)

    result, actual_kml_file_path = ground_locations_to_kml.ground_locations_to_kml(
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

    # Compare the contents of the generated KML file with the static KML file
    assert actual_kml_file_path.read_text(encoding="utf-8") \
        == EXPECTED_KML_DOCUMENT_PATH.read_text(encoding="utf-8")
