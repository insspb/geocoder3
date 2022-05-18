__all__ = ["USCensusReverse"]

import logging

from geocoder.base import OneResult
from geocoder.location import Location
from geocoder.providers.addresses import USCensusQuery


class USCensusReverseResult(OneResult):
    @property
    def ok(self):
        return bool(self.raw_json["States"])

    @property
    def state(self):
        if self.raw_json["States"]:
            return self.raw_json["States"][0].get("NAME")

    @property
    def statenumber(self):
        if self.raw_json["States"]:
            return self.raw_json["States"][0].get("STATE")

    @property
    def county(self):
        if self.raw_json["Counties"]:
            return self.raw_json["Counties"][0].get("NAME")

    @property
    def countynumber(self):
        if self.raw_json["Counties"]:
            return self.raw_json["Counties"][0].get("COUNTY")

    @property
    def tract(self):
        if self.raw_json["Census Tracts"]:
            return self.raw_json["Census Tracts"][0].get("NAME")

    @property
    def tractnumber(self):
        if self.raw_json["Census Tracts"]:
            return self.raw_json["Census Tracts"][0].get("TRACT")

    @property
    def block(self):
        if self.raw_json["2010 Census Blocks"]:
            return self.raw_json["2010 Census Blocks"][0].get("NAME")
        elif self.raw_json["Census Blocks"]:
            return self.raw_json["Census Blocks"][0].get("NAME")

    @property
    def blocknumber(self):
        if self.raw_json["2010 Census Blocks"]:
            return self.raw_json["2010 Census Blocks"][0].get("BLOCK")
        elif self.raw_json["Census Blocks"]:
            return self.raw_json["Census Blocks"][0].get("BLOCK")

    @property
    def geoid(self):
        if self.raw_json["2010 Census Blocks"]:
            return self.raw_json["2010 Census Blocks"][0].get("GEOID")
        elif self.raw_json["Census Blocks"]:
            return self.raw_json["Census Blocks"][0].get("GEOID")


class USCensusReverse(USCensusQuery):
    """
    US Census Geocoder REST Services

    The Census Geocoder is an address look-up tool that converts your address to an
    approximate coordinate (latitude/longitude) and returns information about the
    address range that includes the address and the census geography the address is
    within. The geocoder is available as a web interface and as an API
    (Representational State Transfer - REST - web-based service).

    API Reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf

    """

    _PROVIDER = "uscensus"
    _METHOD = "reverse"
    _URL = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
    _RESULT_CLASS = USCensusReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "x": location.longitude,
            "y": location.latitude,
            "benchmark": kwargs.get("benchmark", "4"),
            "vintage": kwargs.get("vintage", "4"),
            "format": "json",
        }

    def _adapt_results(self, json_response):
        return [json_response["result"]["geographies"]]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = USCensusReverse([38.846542, -76.92691])
    g.debug()
