"""
Module to convert ground locations list to kml document.
"""

import pathlib
import time

import simplekml

from . import location_ground


def ground_locations_to_kml(
    ground_locations: "list[location_ground.LocationGround]",
    document_name_prefix: str,
    save_directory: pathlib.Path,
) -> "tuple[bool, pathlib.Path | None]":
    """
    Generates KML file from a list of ground locations.

    Parameters
    ----------
    ground_locations: list[location_ground.LocationGround]
    document_name_prefix: str
        Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: pathlib.Path
        Path to save the KML file to.

    Returns
    -------
    bool: Whether the operation was a success.
    pathlib.Path: A path to the plotted kml file, or None if the operation failed.
    """
    kml = simplekml.Kml()

    for i, ground_location in enumerate(ground_locations):
        ground_location_name = f"Point {i + 1}: {ground_location.name}"
        latitude = ground_location.latitude
        longitude = ground_location.longitude

        # Coordinates are in the order: longitude, latitude, optional height
        kml.newpoint(name=ground_location_name, coords=[(longitude, latitude)])

    kml_file_path = pathlib.Path(save_directory, f"{document_name_prefix}_{int(time.time())}.kml")

    try:
        kml.save(str(kml_file_path))
        return True, kml_file_path
    # Required for catching library exceptions
    # pylint: disable-next=broad-exception-caught
    except Exception as e:
        print(f"Error while saving KML file: {e}")
        return False, None
