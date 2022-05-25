__all__ = ["ArcgisQuery", "ArcgisResult", "ArcgisReverseResult", "ArcgisReverse"]
from typing import List

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.location import Location


class ArcgisResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._feature = json_content.get("feature", {})

        # proceed with super.__init__
        super(ArcgisResult, self).__init__(json_content)

    @property
    def address(self):
        return self.object_raw_json.get("name", "")

    @property
    def lat(self):
        return self._feature.get("geometry", {}).get("y")

    @property
    def lng(self):
        return self._feature.get("geometry", {}).get("x")

    @property
    def score(self):
        return self._feature.get("attributes", {}).get("Score", "")

    @property
    def quality(self):
        return self._feature.get("attributes", {}).get("Addr_Type", "")

    @property
    def bbox(self) -> List[float]:
        """Output answer as GeoJSON bbox if it can be calculated/retrieved."""
        _extent = self.object_raw_json.get("extent")
        if _extent:
            south = _extent.get("ymin")
            west = _extent.get("xmin")
            north = _extent.get("ymax")
            east = _extent.get("xmax")
            return [float(west), float(south), float(east), float(north)]
        return []


class ArcgisQuery(MultipleResultsQuery):
    """
    ArcGIS REST API

    The World Geocoding Service finds addresses and places in all supported countries
    from a single endpoint. The service can find point locations of addresses,
    business names, and so on.  The output points can be visualized on a map,
    inserted as stops for a route, or loaded as input for a spatial analysis.
    an address, retrieving imagery metadata, or creating a route.

    API Reference: https://developers.arcgis.com/rest/geocode/
    api-reference/geocoding-find.htm
    """

    _PROVIDER = "arcgis"
    _METHOD = "geocode"
    _URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find"
    _RESULT_CLASS = ArcgisResult
    _KEY_MANDATORY = False

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "f": "json",
            "text": location,
            "maxLocations": max_results,
        }

    def _adapt_results(self, json_response):
        return json_response["locations"]

    def _catch_errors(self, json_response):
        status = json_response.get("error")
        if status:
            self.error = status.get("code")
            self.message = status.get("message")
            self.details = status.get("details")

        return self.error


class ArcgisReverseResult(OneResult):
    @property
    def ok(self):
        return bool(self.address)

    @property
    def lat(self):
        return self.object_raw_json["location"].get("y")

    @property
    def lng(self):
        return self.object_raw_json["location"].get("x")

    @property
    def address(self):
        return self.object_raw_json["address"].get("Match_addr")

    @property
    def city(self):
        return self.object_raw_json["address"].get("City")

    @property
    def neighborhood(self):
        return self.object_raw_json["address"].get("Neighbourhood")

    @property
    def region(self):
        return self.object_raw_json["address"].get("Region")

    @property
    def country(self):
        return self.object_raw_json["address"].get("CountryCode")

    @property
    def postal(self):
        return self.object_raw_json["address"].get("Postal")

    @property
    def state(self):
        return self.object_raw_json["address"].get("Region")


class ArcgisReverse(ArcgisQuery):
    """
    ArcGIS REST API

    The World Geocoding Service finds addresses and places in all supported countries
    from a single endpoint. The service can find point locations of addresses,
    business names, and so on.  The output points can be visualized on a map,
    inserted as stops for a route, or loaded as input for a spatial analysis.
    an address, retrieving imagery metadata, or creating a route.

    API Reference: https://developers.arcgis.com/rest/geocode/api-reference/
    geocoding-reverse-geocode.htm
    """

    _PROVIDER = "arcgis"
    _METHOD = "reverse"
    _URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode"  # noqa
    _RESULT_CLASS = ArcgisReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "location": f"{location.lng}, {location.lat}",
            "f": "pjson",
            "distance": kwargs.get("distance", 50000),
            "outSR": kwargs.get("outSR", ""),
        }

    def _adapt_results(self, json_response):
        return [json_response]

    def _catch_errors(self, json_response):
        error = json_response.get("error", None)
        if error:
            self.error = error["message"]

        return self.error
