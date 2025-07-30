"""
GeoPoint class for representing geographic coordinates.
"""
from typing import Iterator, Any


class GeoPoint:
    """
    A class representing a geographic point as a latitude/longitude pair.
    Compatible with google.cloud.firestore_v1.GeoPoint.
    
    This class is iterable, allowing it to be unpacked into latitude and longitude.
    """

    def __init__(self, latitude: float, longitude: float):
        """
        Initialize a GeoPoint with latitude and longitude.

        Args:
            latitude: Latitude between -90 and 90.
            longitude: Longitude between -180 and 180.
        """
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a number")
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a number")

        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")

        self._latitude = float(latitude)
        self._longitude = float(longitude)

    @property
    def latitude(self) -> float:
        """Get the latitude value."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """Get the longitude value."""
        return self._longitude

    def __iter__(self) -> Iterator[float]:
        """Make GeoPoint iterable to allow unpacking."""
        yield self.latitude
        yield self.longitude

    def __eq__(self, other) -> bool:
        """Check if two GeoPoints are equal."""
        if not isinstance(other, GeoPoint):
            return False
        return (
            self.latitude == other.latitude and
            self.longitude == other.longitude
        )

    def __repr__(self) -> str:
        """Return string representation of the GeoPoint."""
        return f"GeoPoint(latitude={self.latitude}, longitude={self.longitude})"

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GeoPoint':
        """Create a GeoPoint from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        
        if latitude is None or longitude is None:
            raise ValueError("Dictionary must contain 'latitude' and 'longitude' keys")
            
        return cls(latitude, longitude)
        
    @classmethod
    def is_geopoint(cls, obj: Any) -> bool:
        """
        Check if an object is a GeoPoint-like object.
        
        A GeoPoint-like object must:
        1. Be iterable
        2. Have a class name that matches the expected name (default: 'GeoPoint')
        
        Args:
            obj: The object to check
            
        Returns:
            True if the object is a GeoPoint-like object, False otherwise
        """
        try:
            iter(obj)
        except TypeError:
            return False
            
        class_name = obj.__class__.__name__
        return class_name == 'GeoPoint'
