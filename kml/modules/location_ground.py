"""
Class LocationGround to use instead of tuple for coordinates.
"""

class LocationGround:
    """
    LocationGround class represents a geographical waypoint with a name, latitude, and longitude.

    Attributes:
        name (str): The name or label for the waypoint.
        latitude (float): The latitude coordinate of the waypoint in decimal degrees.
        longitude (float): The longitude coordinate of the waypoint in decimal degrees.

    Methods:
        __init__(name, latitude, longitude): Initializes a LocationGround object.
        __eq__(other): Checks if two LocationGround objects are equal.
        __repr__(): Returns a string representation of the LocationGround object.
    """
    def __init__(self, name: str, latitude: float, longitude: float):
        """
        Constructor for the LocationGround object.

        Args:
            name (str): The name or label for the waypoint.
            latitude (float): The latitude coordinate of the waypoint in decimal degrees.
            longitude (float): The longitude coordinate of the waypoint in decimal degrees.
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other: "LocationGround"):
        """
        Checks if two LocationGround objects are equal.

        Args:
            other (LocationGround): The other LocationGround object to compare to.
        """
        if not isinstance(other, LocationGround):
            return False

        return (
            self.name == other.name
            and self.latitude == other.latitude
            and self.longitude == other.longitude
        )

    def __repr__(self):
        """
        Returns a string representation of the LocationGround object.
        """
        return f"Ground Location: {self.name}, latitude: {self.latitude}, longitude: {self.longitude})"
