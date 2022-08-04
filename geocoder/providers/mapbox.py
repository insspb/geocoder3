__all__ = ["MapboxResult", "MapboxQuery", "MapboxReverseResult", "MapboxReverse"]

from typing import List

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import mapbox_access_token
from geocoder.location import BBox, Location


class MapboxResult(OneResult):
    def __init__(self, json_content):
        self._geometry = json_content.get("geometry", {})

        for item in json_content.get("context", []):
            if "." in item["id"]:
                # attribute=country & text=Canada
                attribute = item["id"].split(".")[0]
                json_content[attribute] = item["text"]

        super(MapboxResult, self).__init__(json_content)

    @property
    def lat(self):
        coord = self._geometry["coordinates"]
        if coord:
            return coord[1]

    @property
    def lng(self):
        coord = self._geometry["coordinates"]
        if coord:
            return coord[0]

    @property
    def address(self):
        return self.object_raw_json.get("place_name")

    @property
    def house_number(self):
        return self.object_raw_json.get("address")

    @property
    def street(self):
        return ""

    @property
    def city(self):
        return self.object_raw_json.get("place")

    @property
    def state(self):
        return self.object_raw_json.get("region")

    @property
    def country(self):
        return self.object_raw_json.get("country")

    @property
    def postal(self):
        return self.object_raw_json.get("postcode")

    @property
    def accuracy(self):
        if self.interpolated:
            return "interpolated"

    @property
    def quality(self):
        return self.object_raw_json.get("relevance")

    @property
    def interpolated(self):
        return self._geometry.get("interpolated")

    @property
    def bbox(self) -> List[float]:
        """Output answer as GeoJSON bbox if it can be calculated/retrieved."""
        _bbox = self.object_raw_json.get("bbox")
        if _bbox:
            west = _bbox[0]
            south = _bbox[1]
            east = _bbox[2]
            north = _bbox[3]
            return [float(west), float(south), float(east), float(north)]
        return []


class MapboxQuery(MultipleResultsQuery):
    """
    Mapbox Geocoding

    The Mapbox Geocoding API lets you convert location text into
    geographic coordinates (1600 Pennsylvania Ave NW → -77.0366,38.8971).

    API Reference: https://www.mapbox.com/developers/api/geocoding/
    Get Mapbox Access Token: https://www.mapbox.com/account
    """

    _PROVIDER = "mapbox"
    _METHOD = "geocode"
    _URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json"
    _RESULT_CLASS = MapboxResult
    _KEY = mapbox_access_token

    def _build_params(self, location, provider_key, **kwargs):
        base_params = {
            "access_token": provider_key,
            "country": kwargs.get("country"),
            "types": kwargs.get("types"),
        }
        # handle proximity
        proximity = kwargs.get("proximity")
        if proximity is not None:
            proximity = Location(proximity)
            # do not forget to convert bbox to mapbox expectations...
            base_params["proximity"] = "{longitude},{latitude}".format(
                longitude=proximity.longitude, latitude=proximity.latitude
            )

        bbox = kwargs.get("bbox")
        if bbox:
            bbox = BBox(bbox=bbox)
            # do not forget to convert bbox to mapbox expectations...
            base_params["bbox"] = "{west},{south},{east},{north}".format(
                west=bbox.west, east=bbox.east, south=bbox.south, north=bbox.north
            )

        return base_params

    def _before_initialize(self, location, **kwargs):
        self.url = self.url.format(location)

    def _adapt_results(self, json_response):
        # extract the array of JSON objects
        return json_response.get("features", [])


class MapboxReverseResult(MapboxResult):
    @property
    def ok(self):
        return bool(self.address)


class MapboxReverse(MapboxQuery):
    """
    Mapbox Reverse Geocoding

    Reverse geocoding lets you reverse this process, turning a
    pair of lat/lon coordinates into a meaningful place name
    (-77.036,38.897 → 1600 Pennsylvania Ave NW).

    API Reference: https://www.mapbox.com/developers/api/geocoding/

    Get Mapbox Access Token: https://www.mapbox.com/account
    """

    _PROVIDER = "mapbox"
    _METHOD = "reverse"
    _URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/{lng},{lat}.json"

    def _build_params(self, location, provider_key, **kwargs):
        return {
            "access_token": provider_key,
            "country": kwargs.get("country"),
            "types": kwargs.get("types"),
        }

    def _before_initialize(self, location, **kwargs):
        self.location = str(Location(location))
        lat, lng = Location(location).latlng
        self.url = self.url.format(lng=lng, lat=lat)
