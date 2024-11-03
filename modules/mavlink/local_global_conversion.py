"""
Conversion between local and global space.
"""

import pymap3d as pm

from . import drone_odometry
from . import drone_odometry_local
from .. import location_local
from .. import position_global
from .. import position_local


def position_global_from_position_local(
    home_position: position_global.PositionGlobal,
    local_position: position_local.PositionLocal,
) -> tuple[bool, position_global.PositionGlobal] | tuple[False, None]:
    """
    Local coordinates to global coordinates.

    home_position: Global.
    local_position: Local.

    Return: Success, global.
    """
    latitude, longitude, altitude = pm.ned2geodetic(
        local_position.north,
        local_position.east,
        local_position.down,
        home_position.latitude,
        home_position.longitude,
        home_position.altitude,
    )

    result, global_position = position_global.PositionGlobal.create(
        latitude,
        longitude,
        altitude,
    )
    if not result:
        return False, None

    return True, global_position


def position_global_from_location_local(
    home_position: position_global.PositionGlobal,
    local_location: location_local.LocationLocal,
) -> tuple[bool, position_global.PositionGlobal] | tuple[False, None]:
    """
    Local coordinates to global coordinates.

    home_position: Global.
    local_position: Local.

    Return: Global.
    """
    result, local_position = position_local.PositionLocal.create(
        local_location.north, local_location.east, 0.0
    )
    if not result:
        return False, None

    return position_global_from_position_local(home_position, local_position)


def position_local_from_position_global(
    home_position: position_global.PositionGlobal,
    global_position: position_global.PositionGlobal,
) -> tuple[True, position_local.PositionLocal] | tuple[False, None]:
    """
    Global coordinates to local coordinates.

    home_position: Global.
    global_position: Global.

    Return: Local.
    """
    north, east, down = pm.geodetic2ned(
        global_position.latitude,
        global_position.longitude,
        global_position.altitude,
        home_position.latitude,
        home_position.longitude,
        home_position.altitude,
    )

    result, local_position = position_local.PositionLocal.create(
        north,
        east,
        down,
    )
    if not result:
        return False, None

    return True, local_position


def drone_odometry_local_from_global(
    home_position: position_global.PositionGlobal,
    odometry_global: drone_odometry.DroneOdometry,
) -> tuple[bool, drone_odometry_local.DroneOdometryLocal] | tuple[False, None]:
    """
    Converts global odometry to local.

    home_position: Global.
    odometry_global: Global.

    Return: Local.
    """
    result, drone_position_local = position_local_from_position_global(
        home_position,
        odometry_global.position,
    )
    if not result:
        return False, None

    result, drone_orientation_local = drone_odometry_local.DroneOrientationLocal.create_wrap(
        odometry_global.orientation,
    )
    if not result:
        return False, None

    return drone_odometry_local.DroneOdometryLocal.create(
        drone_position_local,
        drone_orientation_local,
    )
