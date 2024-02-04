"""
Module to convert waypoints list to kml document.
"""
import pathlib
import time

import simplekml

from kml.modules import location_ground

def waypoints_to_kml(ground_locations: "list[location_ground.LocationGround]",
                     document_name_prefix: str,
                     save_directory: pathlib.Path) -> "tuple[bool, pathlib.Path | None]":
    """
    Generates KML file from a list of waypoints.

    Parameters
    ----------
    waypoints: list[tuple[float, float]]
        Waypoint coordinates in decimal degrees (latitude, longitude).
    document_name_prefix: str
        Name of the KML file to save (without the timestamp or .kml extension).
    save_directory: pathlib.Path
        Path to save the KML file to.

    Returns
    -------
    bool
        Whether the operation was a success.
    """
    kml = simplekml.Kml()

    for ground_location in enumerate(ground_locations):
        ground_location_name = f"Point {ground_location.name}"
        lat = ground_location.latitude
        lng = ground_location.longitude

        # coords parameters are in the order: lon, lat, optional height
        kml.newpoint(name=ground_location_name, coords=[(lng, lat)])

    kml_file_path = pathlib.Path(save_directory, f"{document_name_prefix}_{int(time.time())}.kml")

    try:
        kml.save(str(kml_file_path))
        return True, kml_file_path
    # Required for catching library exceptions
    # pylint: disable-next=broad-exception-caught
    except Exception as e:
        print(f"Error while saving KML file: {e}")
        return False, None
