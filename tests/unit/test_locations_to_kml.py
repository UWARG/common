"""
Test Process.
"""

import pathlib

import pytest

from modules import location_global
from modules.kml import locations_to_kml


PARENT_DIRECTORY = pathlib.Path("tests", "unit", "kml_documents")
KML_SUFFIX = ".kml"


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def locations() -> list[location_global.LocationGlobal]:  # type: ignore
    """
    List of locations.
    """
    result, san_francisco = location_global.LocationGlobal.create(37.7749, -122.4194)
    assert result
    assert san_francisco is not None

    result, los_angeles = location_global.LocationGlobal.create(34.0522, -118.2437)
    assert result
    assert los_angeles is not None

    result, new_york_city = location_global.LocationGlobal.create(40.7128, -74.0060)
    assert result
    assert new_york_city is not None

    yield [
        san_francisco,
        los_angeles,
        new_york_city,
    ]


@pytest.fixture
def named_locations() -> list[location_global.NamedLocationGlobal]:  # type: ignore
    """
    List of named locations.
    """
    result, san_francisco = location_global.NamedLocationGlobal.create(
        "San Francisco", 37.7749, -122.4194
    )
    assert result
    assert san_francisco is not None

    result, los_angeles = location_global.NamedLocationGlobal.create(
        "Los Angeles", 34.0522, -118.2437
    )
    assert result
    assert los_angeles is not None

    result, new_york_city = location_global.NamedLocationGlobal.create(
        "New York City", 40.7128, -74.0060
    )
    assert result
    assert new_york_city is not None

    yield [
        san_francisco,
        los_angeles,
        new_york_city,
    ]


def test_named_locations_to_kml_with_save_path(
    named_locations: list[location_global.NamedLocationGlobal], tmp_path: pathlib.Path
) -> None:
    """
    Basic test case to save KML to the correct path when provided.
    """
    # Setup
    expected_kml_document_path = pathlib.Path(PARENT_DIRECTORY, "expected_named.kml")
    actual_kml_document_name = "actual"

    tmp_path.mkdir(parents=True, exist_ok=True)

    # Run
    result, actual_kml_file_path = locations_to_kml.named_locations_to_kml(
        named_locations,
        actual_kml_document_name,
        tmp_path,
    )

    # Check
    assert result
    assert actual_kml_file_path is not None

    assert actual_kml_file_path.exists()
    assert actual_kml_file_path.suffix == KML_SUFFIX

    assert actual_kml_file_path.read_text(encoding="utf-8") == expected_kml_document_path.read_text(
        encoding="utf-8"
    )


def test_locations_to_kml(
    locations: list[location_global.LocationGlobal], tmp_path: pathlib.Path
) -> None:
    """
    Basic test case for locations without names.
    """
    expected_kml_document_path = pathlib.Path(PARENT_DIRECTORY, "expected_enumerated.kml")
    actual_kml_document_name = "actual_kml_document"

    tmp_path.mkdir(parents=True, exist_ok=True)

    # Run
    result, actual_kml_file_path = locations_to_kml.locations_to_kml(
        locations,
        actual_kml_document_name,
        tmp_path,
    )

    # Check
    assert result
    assert actual_kml_file_path is not None

    assert actual_kml_file_path.exists()
    assert actual_kml_file_path.suffix == KML_SUFFIX

    assert actual_kml_file_path.read_text(encoding="utf-8") == expected_kml_document_path.read_text(
        encoding="utf-8"
    )
