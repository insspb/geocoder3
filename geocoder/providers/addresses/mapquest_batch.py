__all__ = ["MapquestBatch"]

from geocoder.base import MultipleResultsQuery
from geocoder.keys import mapquest_key
from geocoder.providers.addresses.mapquest import MapquestResult


class MapQuestBatchResult(MapquestResult):
    @property
    def ok(self):
        return bool(self.quality)


class MapquestBatch(MultipleResultsQuery):
    """
    MapQuest

    The geocoding service enables you to take an address and get the
    associated latitude and longitude. You can also use any latitude
    and longitude pair and get the associated address. Three types of
    geocoding are offered: address, reverse, and batch.

    API Reference: http://www.mapquestapi.com/geocoding/
    """

    _PROVIDER = "mapquest"
    _METHOD = "batch"
    _RESULT_CLASS = MapQuestBatchResult
    _URL = "http://www.mapquestapi.com/geocoding/v1/batch"
    _TIMEOUT = 30
    _KEY = mapquest_key

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        self._TIMEOUT = kwargs.get("timeout", 30)

        return {
            "key": provider_key,
            "location": location,
            "maxResults": max_results,
            "outFormat": "json",
        }

    def _adapt_results(self, json_response):
        results = json_response.get("results", [])
        if results:
            return [result["locations"][0] for result in results]

        return []


if __name__ == "__main__":
    g = MapquestBatch(["Denver,CO", "Boulder,CO"])
    g.debug()
