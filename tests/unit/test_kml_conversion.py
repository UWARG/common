"""
Test Process.
"""

import pathlib

import pytest
import pytest_mock

from modules import location_global
from modules import position_global_relative_altitude
from modules.kml import kml_conversion


PARENT_DIRECTORY = pathlib.Path("tests", "unit", "kml_documents")
KML_SUFFIX = ".kml"

EXPECTED_ENUMERATED_FILENAME = "expected_enumerated.kml"
EXPECTED_NAMED_FILENAME = "expected_named.kml"


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def named_positions() -> list[position_global_relative_altitude.NamedPositionGlobalRelativeAltitude]:  # type: ignore
    """
    List of named locations.
    """
    result, san_francisco = (
        position_global_relative_altitude.NamedPositionGlobalRelativeAltitude.create(
            "San Francisco", 37.7749, -122.4194, 0.0
        )
    )
    assert result
    assert san_francisco is not None

    result, los_angeles = (
        position_global_relative_altitude.NamedPositionGlobalRelativeAltitude.create(
            "Los Angeles", 34.0522, -118.2437, 0.0
        )
    )
    assert result
    assert los_angeles is not None

    result, new_york_city = (
        position_global_relative_altitude.NamedPositionGlobalRelativeAltitude.create(
            "New York City", 40.7128, -74.0060, 0.0
        )
    )
    assert result
    assert new_york_city is not None

    yield [
        san_francisco,
        los_angeles,
        new_york_city,
    ]


@pytest.fixture
def positions() -> list[position_global_relative_altitude.PositionGlobalRelativeAltitude]:  # type: ignore
    """
    List of locations.
    """
    result, san_francisco = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        37.7749, -122.4194, 0.0
    )
    assert result
    assert san_francisco is not None

    result, los_angeles = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        34.0522, -118.2437, 0.0
    )
    assert result
    assert los_angeles is not None

    result, new_york_city = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        40.7128, -74.0060, 0.0
    )
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


class TestNamedPositions:
    """
    Test named_positions_to_kml function.
    """

    def test_with_save_path(
        self,
        named_positions: list[
            position_global_relative_altitude.NamedPositionGlobalRelativeAltitude
        ],
        tmp_path: pathlib.Path,
    ) -> None:
        """
        Basic test case to save KML to the correct path when provided.
        """
        # Setup
        expected_kml_document_path = pathlib.Path(PARENT_DIRECTORY, EXPECTED_NAMED_FILENAME)
        actual_kml_document_name = "actual"

        tmp_path.mkdir(parents=True, exist_ok=True)

        # Run
        result, actual_kml_file_path = kml_conversion.named_positions_to_kml(
            named_positions,
            actual_kml_document_name,
            tmp_path,
        )

        # Check
        assert result
        assert actual_kml_file_path is not None

        assert actual_kml_file_path.exists()
        assert actual_kml_file_path.suffix == KML_SUFFIX

        assert actual_kml_file_path.read_text(
            encoding="utf-8"
        ) == expected_kml_document_path.read_text(encoding="utf-8")

    def test_nonexistent_save_path(
        self,
        named_positions: list[
            position_global_relative_altitude.NamedPositionGlobalRelativeAltitude
        ],
    ) -> None:
        """
        Save path that doesn't exist.
        """
        # Setup
        kml_document_name = "actual"
        nonexistent_path = pathlib.Path("nonexistent")

        # Run
        result, actual_kml_file_path = kml_conversion.named_positions_to_kml(
            named_positions,
            kml_document_name,
            nonexistent_path,
        )

        # Check
        assert not result
        assert actual_kml_file_path is None

    def test_no_locations(self, tmp_path: pathlib.Path) -> None:
        """
        Empty list.
        """
        # Setup
        empty = []
        kml_document_name = "actual"

        # Run
        result, actual_kml_file_path = kml_conversion.named_positions_to_kml(
            empty,
            kml_document_name,
            tmp_path,
        )

        # Check
        assert not result
        assert actual_kml_file_path is None


class TestWrapper:
    """
    Functions are wrappers to named_positions_to_kml.
    """

    def test_positions(
        self,
        mocker: pytest_mock.MockerFixture,
        positions: list[position_global_relative_altitude.PositionGlobalRelativeAltitude],
        tmp_path: pathlib.Path,
    ) -> None:
        """
        Basic test case to save KML to the correct path when provided.
        """
        # Setup
        expected_kml_document_path = pathlib.Path(PARENT_DIRECTORY, EXPECTED_ENUMERATED_FILENAME)
        actual_kml_document_name = "actual"

        tmp_path.mkdir(parents=True, exist_ok=True)

        spy = mocker.spy(kml_conversion, "named_positions_to_kml")

        # Run
        result, actual_kml_file_path = kml_conversion.positions_to_kml(
            positions,
            actual_kml_document_name,
            tmp_path,
        )

        # Check
        spy.assert_called_once()

        assert result
        assert actual_kml_file_path is not None

        assert actual_kml_file_path.exists()
        assert actual_kml_file_path.suffix == KML_SUFFIX

        assert actual_kml_file_path.read_text(
            encoding="utf-8"
        ) == expected_kml_document_path.read_text(encoding="utf-8")

    def test_named_locations(
        self,
        mocker: pytest_mock.MockerFixture,
        named_positions: list[
            position_global_relative_altitude.NamedPositionGlobalRelativeAltitude
        ],
        tmp_path: pathlib.Path,
    ) -> None:
        """
        Basic test case to save KML to the correct path when provided.
        """
        # Setup
        expected_kml_document_path = pathlib.Path(PARENT_DIRECTORY, EXPECTED_NAMED_FILENAME)
        actual_kml_document_name = "actual"

        tmp_path.mkdir(parents=True, exist_ok=True)

        spy = mocker.spy(kml_conversion, "named_positions_to_kml")

        # Run
        result, actual_kml_file_path = kml_conversion.named_positions_to_kml(
            named_positions,
            actual_kml_document_name,
            tmp_path,
        )

        # Check
        spy.assert_called_once()

        assert result
        assert actual_kml_file_path is not None

        assert actual_kml_file_path.exists()
        assert actual_kml_file_path.suffix == KML_SUFFIX

        assert actual_kml_file_path.read_text(
            encoding="utf-8"
        ) == expected_kml_document_path.read_text(encoding="utf-8")

    def test_locations(
        self,
        mocker: pytest_mock.MockerFixture,
        locations: list[location_global.LocationGlobal],
        tmp_path: pathlib.Path,
    ) -> None:
        """
        Basic test case for locations without names.
        """
        expected_kml_document_path = pathlib.Path(PARENT_DIRECTORY, EXPECTED_ENUMERATED_FILENAME)
        actual_kml_document_name = "actual_kml_document"

        tmp_path.mkdir(parents=True, exist_ok=True)

        spy = mocker.spy(kml_conversion, "named_positions_to_kml")

        # Run
        result, actual_kml_file_path = kml_conversion.locations_to_kml(
            locations,
            actual_kml_document_name,
            tmp_path,
        )

        # Check
        spy.assert_called_once()

        assert result
        assert actual_kml_file_path is not None

        assert actual_kml_file_path.exists()
        assert actual_kml_file_path.suffix == KML_SUFFIX

        assert actual_kml_file_path.read_text(
            encoding="utf-8"
        ) == expected_kml_document_path.read_text(encoding="utf-8")
