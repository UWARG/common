"""
Module to convert ground locations list to kml document.
"""

import pathlib
import time

import simplekml

from . import named_location_global


def ground_locations_to_kml(
    ground_locations: list[named_location_global.NamedLocationGlobal],
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None]":
    """
    Generates a KML file from a list of ground locations.

    ground_locations: Ground locations.
    document_name_prefix: Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: Parent directory to save the KML file to.

    Return: Success, path to the KML file.
    """
    kml = simplekml.Kml()

    for i, ground_location in enumerate(ground_locations):
        ground_location_name = f"Point {i + 1}: {ground_location.name}"
        latitude = ground_location.location.latitude
        longitude = ground_location.location.longitude

        # Coordinates are in the order: longitude, latitude, optional height
        kml.newpoint(name=ground_location_name, coords=[(longitude, latitude)])

    current_time = time.time()
    kml_file_path = pathlib.Path(save_directory, f"{document_name_prefix}_{int(current_time)}.kml")

    try:
        kml.save(str(kml_file_path))
        return True, kml_file_path
    # Required for catching library exceptions
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(f"Error while saving KML file: {exception}")
        return False, None
