"""
Module used to convert list of waypoints to KML file
"""
import os

import simplekml


def waypoints_to_kml(waypoints: "list[tuple[float, float]]",
                     document_name: str,
                     save_path: str = None) -> str:
    """
    Generates KML file from a list of waypoints.

    Parameters
    ----------
    waypoints: list[tuple[float, float]]
        Waypoint coordinates in decimal degrees (latitude, longitude).
    document_name: str
        Name of the KML file to save (without the .kml extension).
    save_path: str, optional
        Path where the KML file should be saved. If not provided, the file
        will be saved in the current working directory.

    Returns
    -------
    str
        Path to generated KML file.
    """
    kml = simplekml.Kml()

    for idx, waypoint in enumerate(waypoints):
        waypoint_name = f'Point {idx}'
        lat, lng = waypoint

        # coords parameters are in the order: lon, lat, optional height
        kml.newpoint(name=waypoint_name, coords=[(lng, lat)])

    if save_path is None:
        # Save in the current working directory
        save_path = os.getcwd()

    kml_file_path = os.path.join(save_path, f'{document_name}.kml')
    kml.save(kml_file_path)

    return kml_file_path
