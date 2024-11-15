"""
Module to convert ground locations list to kml document.
"""

import pathlib
import time

import simplekml
import simplekml.base

from .. import location_global
from .. import position_global_relative_altitude


def __save_kml_file(
    kml: simplekml.Kml, document_name_prefix: str, save_directory: pathlib.Path
) -> tuple[True, pathlib.Path] | tuple[False, None]:
    """
    Save KML to the directory.
    """
    current_time = time.time()
    kml_file_path = pathlib.Path(save_directory, f"{document_name_prefix}_{int(current_time)}.kml")

    try:
        kml.save(str(kml_file_path))
    # Required for catching library exceptions
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(f"Error while saving KML file: {exception}")
        return False, None

    return True, kml_file_path


def named_positions_to_kml(
    named_positions: list[position_global_relative_altitude.NamedPositionGlobalRelativeAltitude],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> tuple[True, pathlib.Path] | tuple[False, None]:
    """
    Generates a KML file from a list of ground locations.

    named_positions: Positions with names.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    if len(named_positions) == 0:
        return False, None

    # Force KML ID reset for determinism
    # pylint: disable-next=protected-access
    simplekml.base.Kmlable._globalid = 0

    kml = simplekml.Kml()

    for named_position in named_positions:
        name = named_position.name
        latitude = named_position.latitude
        longitude = named_position.longitude
        relative_altitude = named_position.relative_altitude

        # Coordinates are in the order: longitude, latitude, optional height
        kml.newpoint(name=name, coords=[(longitude, latitude, relative_altitude)])

    return __save_kml_file(kml, document_name_prefix, save_directory)


def positions_to_kml(
    positions: list[position_global_relative_altitude.PositionGlobalRelativeAltitude],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None]":
    """
    Converts positions to named positions with enumerated name and calls named_positions_to_kml.

    positions: Positions without names.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    named_positions = []
    for i, position in enumerate(positions):
        result, named_position = (
            position_global_relative_altitude.NamedPositionGlobalRelativeAltitude.create(
                str(i), position.latitude, position.longitude, position.relative_altitude
            )
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert named_position is not None

        named_positions.append(named_position)

    return named_positions_to_kml(named_positions, document_name_prefix, save_directory)


def named_locations_to_kml(
    named_locations: list[location_global.NamedLocationGlobal],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> tuple[True, pathlib.Path] | tuple[False, None]:
    """
    Converts named locations to named positions and calls named_positions_to_kml.

    named_locations: Locations with names.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    named_positions = []
    for named_location in named_locations:
        result, named_position = (
            position_global_relative_altitude.NamedPositionGlobalRelativeAltitude.create(
                named_location.name, named_location.latitude, named_location.longitude, 0.0
            )
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert named_position is not None

        named_positions.append(named_position)

    return named_positions_to_kml(named_positions, document_name_prefix, save_directory)


def locations_to_kml(
    locations: list[location_global.LocationGlobal],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None]":
    """
    Converts locations to named positions with enumerated name and altitude 0.0 and calls named_positions_to_kml.

    locations: Locations without names.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    named_positions = []
    for i, location in enumerate(locations):
        result, named_position = (
            position_global_relative_altitude.NamedPositionGlobalRelativeAltitude.create(
                str(i), location.latitude, location.longitude, 0.0
            )
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert named_position is not None

        named_positions.append(named_position)

    return named_positions_to_kml(named_positions, document_name_prefix, save_directory)
