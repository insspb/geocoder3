__all__ = ["OsmReverse"]

from geocoder.location import Location
from geocoder.providers.addresses import OsmQuery


class OsmReverse(OsmQuery):
    """
    Nominatim

    Nominatim (from the Latin, 'by name') is a tool to search OSM data by name
    and address and to generate synthetic addresses of OSM points (reverse geocoding).

    API Reference: http://wiki.openstreetmap.org/wiki/Nominatim
    """

    provider = "osm"
    method = "reverse"

    def _build_params(
        self,
        location,
        provider_key: str,
        max_results: int = 1,
        **kwargs,
    ):
        params = {
            "q": str(Location(location)),
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": max_results,
        }
        if "lang_code" in kwargs:
            params["accept-language"] = kwargs.get("lang_code")
        return params
