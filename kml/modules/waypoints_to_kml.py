import simplekml
from pathlib import Path


def waypoints_to_kml(waypoints: "list[tuple[float, float]]",
                     document_name: str,
                     save_path: Path) -> bool:
    """
    Generates KML file from a list of waypoints.

    Parameters
    ----------
    waypoints: list[tuple[float, float]]
        Waypoint coordinates in decimal degrees (latitude, longitude).
    document_name: str
        Name of the KML file to save (without the .kml extension).
    save_path: pathlib.Path, optional
        Path where the KML file should be saved. If not provided, the file
        will be saved in the current working directory.

    Returns
    -------
    bool
        Whether the operation was a success.
    """
    kml = simplekml.Kml()

    for idx, waypoint in enumerate(waypoints):
        waypoint_name = f"Point {idx}"
        lat, lng = waypoint

        # coords parameters are in the order: lon, lat, optional height
        kml.newpoint(name=waypoint_name, coords=[(lng, lat)])

    kml_file_path = save_path / f'{document_name}.kml'

    try:
        kml.save(str(kml_file_path))
        return True
    except Exception as e:
        print(f"Error while saving KML file: {e}")
        return False
