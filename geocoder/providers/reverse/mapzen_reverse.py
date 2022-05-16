__all__ = ["MapzenReverse"]

import logging

from geocoder.location import Location
from geocoder.providers.addresses import MapzenQuery, MapzenResult


class MapzenReverseResult(MapzenResult):
    @property
    def ok(self):
        return bool(self.address)


class MapzenReverse(MapzenQuery):
    """
    Mapzen REST API

    API Reference: https://mapzen.com/documentation/search/reverse/
    """

    provider = "mapzen"
    method = "reverse"

    _URL = "https://search.mapzen.com/v1/reverse"
    _RESULT_CLASS = MapzenReverseResult

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        location = Location(location)
        return {
            "point.lat": location.lat,
            "point.lon": location.lng,
            "size": max_results,
            "layers": kwargs.get("layers"),
            "source": kwargs.get("sources"),
            "boundary.country": kwargs.get("country"),
            "api_key": provider_key,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = MapzenReverse("45.4049053 -75.7077965", key="search-un1M9Hk")
    g.debug()
