__all__ = [
    "GisgraphyResult",
    "GisgraphyQuery",
    "GisgraphyReverseResult",
    "GisgraphyReverse",
]
from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.location import Location


class GisgraphyResult(OneResult):
    @property
    def lat(self):
        return self.object_raw_json.get("lat")

    @property
    def lng(self):
        return self.object_raw_json.get("lng")

    @property
    def address(self):
        return self.object_raw_json.get("formatedFull", "")

    @property
    def country(self):
        return self.object_raw_json.get("countryCode", "")

    @property
    def state(self):
        return self.object_raw_json.get("state", "")

    @property
    def city(self):
        return self.object_raw_json.get("city", "")

    @property
    def street(self):
        return self.object_raw_json.get("streetName", "")

    @property
    def house_number(self):
        return self.object_raw_json.get("houseNumber", "")

    @property
    def postal(self):
        return self.object_raw_json.get("zipCode", "")


class GisgraphyQuery(MultipleResultsQuery):
    """
    Gisgraphy REST API

    API Reference: http://www.gisgraphy.com/documentation/user-guide.php
    """

    _PROVIDER = "gisgraphy"
    _METHOD = "geocode"
    _URL = "https://services.gisgraphy.com/geocoding/"
    _RESULT_CLASS = GisgraphyResult
    _KEY_MANDATORY = False

    def _build_headers(self, provider_key, **kwargs):
        return {
            "Referer": "https://services.gisgraphy.com",
            "User-agent": "geocoder-converter",
        }

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "address": location,
            "limitnbresult": max_results,
            "format": "json",
        }

    def _adapt_results(self, json_response):
        return json_response["result"]


class GisgraphyReverseResult(GisgraphyResult):
    @property
    def ok(self):
        return bool(self.address)


class GisgraphyReverse(GisgraphyQuery):
    """
    Gisgraphy REST API

    API Reference: http://www.gisgraphy.com/documentation/user-guide.php
    """

    _PROVIDER = "gisgraphy"
    _METHOD = "reverse"
    _URL = "https://services.gisgraphy.com/reversegeocoding/"
    _RESULT_CLASS = GisgraphyReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "lat": location.lat,
            "lng": location.lng,
            "format": "json",
        }
