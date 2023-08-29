"""
Test process for KML generation
"""
import os

import pytest
from pykml import parser

from modules import waypoints_to_kml


@pytest.fixture
def waypoints():
    return [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)]


def _validate_kml_file_from_waypoints(kml_file_path, expected_waypoints):
    """
    Helper function that uses pykml validate KML file with expected waypoints.
    """
    with open(kml_file_path, 'r') as f:
        kml_doc = parser.parse(f).getroot()

    placemarks = kml_doc.Document.Placemark
    assert len(placemarks) == len(expected_waypoints)

    for idx, waypoint in enumerate(expected_waypoints):
        waypoint_name = f"Point {idx}"
        lat, lng = waypoint

        placemark = placemarks[idx]
        assert placemark.name == waypoint_name

        # Extract and split the coordinates string
        coordinates_str = placemark.Point.coordinates.text
        coordinates_parts = coordinates_str.split(',')

        # Extract longitude and latitude components
        placemark_lng = float(coordinates_parts[0])
        placemark_lat = float(coordinates_parts[1])

        assert placemark_lng == lng
        assert placemark_lat == lat


def test_waypoints_to_kml_with_save_path(waypoints, tmp_path):
    """
    Basic test case to save KML to correct path when provided.
    """
    document_name = "test_document"

    # Build a temporary directory using tmp_path so the KML files are cleaned after the tests is run
    save_path = tmp_path / "path/to/save"
    save_path.mkdir(parents=True, exist_ok=True)

    kml_file_path = waypoints_to_kml.waypoints_to_kml(waypoints, document_name, str(save_path))

    # Assert that the KML file has been generated properly in the provided path
    assert kml_file_path.startswith(str(save_path))
    assert os.path.exists(kml_file_path)
    assert kml_file_path.endswith(".kml")

    # Validate the content of the KML file
    _validate_kml_file_from_waypoints(kml_file_path, waypoints)


def test_waypoints_to_kml_default_save_path(waypoints, tmp_path):
    """
    Basic test case to save KML to default path when no path provided.
    """
    document_name = "test_document"

    # Change current directory to the tmp_path so the KML files are cleaned after the tests is run
    os.chdir(tmp_path)

    kml_file_path = waypoints_to_kml.waypoints_to_kml(waypoints, document_name)

    # Assert that the KML file has been generated properly in the current directory
    assert kml_file_path.startswith(str(tmp_path))
    assert os.path.exists(kml_file_path)
    assert kml_file_path.endswith(".kml")

    # Validate the content of the KML file
    _validate_kml_file_from_waypoints(kml_file_path, waypoints)
