__all__ = ["YahooQuery"]

import logging

from geocoder.base import MultipleResultsQuery, OneResult


class YahooResult(OneResult):
    @property
    def lat(self):
        return self.object_raw_json.get("latitude")

    @property
    def lng(self):
        return self.object_raw_json.get("longitude")

    @property
    def address(self):
        line1 = self.object_raw_json.get("line1")
        line2 = self.object_raw_json.get("line2")
        return ", ".join([line1, line2]) if line1 else line2

    @property
    def house_number(self):
        return self.object_raw_json.get("house")

    @property
    def street(self):
        return self.object_raw_json.get("street")

    @property
    def neighborhood(self):
        return self.object_raw_json.get("neighborhood")

    @property
    def city(self):
        return self.object_raw_json.get("city")

    @property
    def county(self):
        return self.object_raw_json.get("county")

    @property
    def state(self):
        return self.object_raw_json.get("state")

    @property
    def country(self):
        return self.object_raw_json.get("country")

    @property
    def hash(self):
        return self.object_raw_json.get("hash")

    @property
    def quality(self):
        return self.object_raw_json.get("addressMatchType")

    @property
    def postal(self):
        postal = self.object_raw_json.get("postal")
        return postal or self.object_raw_json.get("uzip")


class YahooQuery(MultipleResultsQuery):
    """
    Yahoo BOSS Geo Services

    Yahoo PlaceFinder is a geocoding Web service that helps developers make
    their applications location-aware by converting street addresses or
    place names into geographic coordinates (and vice versa).

    API Reference: https://developer.yahoo.com/boss/geo/
    """

    _PROVIDER = "yahoo"
    _METHOD = "geocode"
    _URL = "https://sgws2.maps.yahoo.com/FindLocation"
    _RESULT_CLASS = YahooResult
    _KEY_MANDATORY = False

    def _build_params(self, location, provider_key, **kwargs):
        return {
            "q": location,
            "flags": "J",
            "locale": kwargs.get("locale", "en-CA"),
        }

    def _catch_errors(self, json_response):
        status = json_response["statusDescription"]
        if status and status != "OK":
            self.error = status

        return self.error

    def _adapt_results(self, json_response):
        return [json_response["Result"]]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = YahooQuery("1552 Payette dr., Ottawa, ON")
    g.debug()
