"""
Module to convert ground locations list to kml document.
"""

import pathlib
import time

import simplekml

from .. import location_global


def locations_to_kml(
    locations: list[location_global.LocationGlobal],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None]":
    """
    Converts locations to named locations with empty name and calls named_locations_to_kml.

    locations: Locations without names.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    named_locations = []
    for i, location in enumerate(locations):
        result, named_location = location_global.NamedLocationGlobal.create(
            str(i), location.latitude, location.longitude
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert named_location is not None

        named_locations.append(named_location)

    return named_locations_to_kml(named_locations, document_name_prefix, save_directory)


def named_locations_to_kml(
    named_locations: list[location_global.NamedLocationGlobal],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> tuple[True, pathlib.Path] | tuple[False, None]:
    """
    Generates a KML file from a list of ground locations.

    named_locations: Locations with names.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    kml = simplekml.Kml()

    for named_location in named_locations:
        name = named_location.name
        latitude = named_location.latitude
        longitude = named_location.longitude

        # Coordinates are in the order: longitude, latitude, optional height
        kml.newpoint(name=name, coords=[(longitude, latitude)])

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
