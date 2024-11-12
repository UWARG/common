"""
Test calls only, not conversion correctness as that is handled by the library.
"""

import pytest

from modules import location_global
from modules import location_local
from modules import orientation
from modules import position_global
from modules import position_local
from modules.mavlink import drone_odometry_global
from modules.mavlink import drone_odometry_local
from modules.mavlink import local_global_conversion


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=duplicate-code,protected-access,redefined-outer-name


@pytest.fixture
def home_position() -> position_global.PositionGlobal:  # type: ignore
    """
    Home position.
    """
    result, position = position_global.PositionGlobal.create(43.472978, -80.540103, 336.0)
    assert result
    assert position is not None

    yield position


def test_position_global_from_position_local(home_position: position_global.PositionGlobal) -> None:
    """
    Normal.
    """
    # Setup
    result, position = position_local.PositionLocal.create(0.0, 0.0, 0.0)
    assert result
    assert position is not None

    # Run
    result, actual = local_global_conversion.position_global_from_position_local(
        home_position, position
    )

    # Check
    assert result
    assert actual is not None
    assert isinstance(actual, position_global.PositionGlobal)


def test_position_global_from_location_local(home_position: position_global.PositionGlobal) -> None:
    """
    Normal.
    """
    # Setup
    result, location = location_local.LocationLocal.create(0.0, 0.0)
    assert result
    assert location is not None

    # Run
    result, actual = local_global_conversion.position_global_from_location_local(
        home_position, location
    )

    # Check
    assert result
    assert actual is not None
    assert isinstance(actual, position_global.PositionGlobal)


def test_position_local_from_position_global(home_position: position_global.PositionGlobal) -> None:
    """
    Normal.
    """
    # Setup
    result, position = position_global.PositionGlobal.create(43.472978, -80.540103, 336.0)
    assert result
    assert position is not None

    # Run
    result, actual = local_global_conversion.position_local_from_position_global(
        home_position, position
    )

    # Check
    assert result
    assert actual is not None
    assert isinstance(actual, position_local.PositionLocal)


def test_position_local_from_location_global(home_position: position_global.PositionGlobal) -> None:
    """
    Normal.
    """
    # Setup
    result, location = location_global.LocationGlobal.create(43.472978, -80.540103)
    assert result
    assert location is not None

    # Run
    result, actual = local_global_conversion.position_local_from_location_global(
        home_position, location
    )

    # Check
    assert result
    assert actual is not None
    assert isinstance(actual, position_local.PositionLocal)


def test_drone_odometry_local_from_global(home_position: position_global.PositionGlobal) -> None:
    """
    Normal.
    """
    # Setup
    result, drone_position = position_global.PositionGlobal.create(43.472978, -80.540103, 336.0)
    assert result
    assert drone_position is not None

    result, drone_orientation = orientation.Orientation.create(0.0, 0.0, 0.0)
    assert result
    assert drone_orientation is not None

    result, odometry = drone_odometry_global.DroneOdometryGlobal.create(
        drone_position, drone_orientation, drone_odometry_global.FlightMode.MANUAL
    )
    assert result
    assert odometry is not None

    # Run
    result, actual = local_global_conversion.drone_odometry_local_from_global(
        home_position, odometry
    )

    # Check
    assert result
    assert actual is not None
    assert isinstance(actual, drone_odometry_local.DroneOdometryLocal)
