__all__ = ["LocationIQQuery", "LocationIQReverse", "LocationIQResult"]

import json
import logging

from geocoder.keys import locationiq_key
from geocoder.location import Location
from geocoder.providers.osm import OsmQuery, OsmResult


class LocationIQResult(OsmResult):
    pass


class LocationIQQuery(OsmQuery):

    _PROVIDER = "locationiq"
    _METHOD = "geocode"
    _URL = "https://locationiq.org/v1/search.php"
    _RESULT_CLASS = LocationIQResult
    _KEY = locationiq_key
    _KEY_MANDATORY = True

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "key": provider_key,
            "q": location,
            "format": "json",
            "addressdetails": 1,
            "limit": max_results,
        }


class LocationIQReverse(LocationIQQuery):

    _PROVIDER = "locationiq"
    _METHOD = "reverse"
    _URL = "https://locationiq.org/v1/reverse.php"

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "format": "json",
            "key": provider_key,
            "lat": location.latitude,
            "lon": location.longitude,
        }

    def _adapt_results(self, json_response):
        return [json_response]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = LocationIQQuery("Ottawa, Ontario")
    g.debug()
    g = LocationIQQuery("Ottawa, Ontario", max_results=5)
    print(json.dumps(g.geojson, indent=4))
