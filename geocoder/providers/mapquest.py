__all__ = [
    "MapquestResult",
    "MapquestQuery",
    "MapQuestBatchResult",
    "MapquestBatch",
    "MapQuestReverseResult",
    "MapquestReverse",
]

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import mapquest_key
from geocoder.location import BBox, Location


class MapquestResult(OneResult):
    @property
    def lat(self):
        return self.object_raw_json.get("latLng", {}).get("lat")

    @property
    def lng(self):
        return self.object_raw_json.get("latLng", {}).get("lng")

    @property
    def street(self):
        return self.object_raw_json.get("street")

    @property
    def address(self):
        if self.street:
            return self.street
        elif self.city:
            return self.city
        elif self.country:
            return self.country

    @property
    def quality(self):
        return self.object_raw_json.get("geocodeQuality")

    @property
    def postal(self):
        return self.object_raw_json.get("postalCode")

    @property
    def neighborhood(self):
        return self.object_raw_json.get("adminArea6")

    @property
    def city(self):
        return self.object_raw_json.get("adminArea5")

    @property
    def county(self):
        return self.object_raw_json.get("adminArea4")

    @property
    def state(self):
        return self.object_raw_json.get("adminArea3")

    @property
    def country(self):
        return self.object_raw_json.get("adminArea1")


class MapquestQuery(MultipleResultsQuery):
    """
    MapQuest

    The geocoding service enables you to take an address and get the
    associated latitude and longitude. You can also use any latitude
    and longitude pair and get the associated address. Three types of
    geocoding are offered: address, reverse, and batch.

    API Reference: http://www.mapquestapi.com/geocoding/
    """

    _PROVIDER = "mapquest"
    _METHOD = "geocode"
    _URL = "http://www.mapquestapi.com/geocoding/v1/address"
    _RESULT_CLASS = MapquestResult
    _KEY = mapquest_key

    def _build_headers(self, provider_key, **kwargs):
        return {
            "referer": "http://www.mapquestapi.com/geocoding/",
            "host": "www.mapquestapi.com",
        }

    def _build_params(self, location, provider_key, max_results: int = 1, **kwargs):
        params = {
            "key": provider_key,
            "location": location,
            "maxResults": max_results,
            "outFormat": "json",
        }

        bbox = kwargs.get("bbox")
        if bbox:
            bbox = BBox(bbox=bbox)
            params["boundingBox"] = "{north},{west},{south},{east}".format(
                west=bbox.west, east=bbox.east, south=bbox.south, north=bbox.north
            )

        return params

    def _catch_errors(self, json_response):
        if b"The AppKey submitted with this request is invalid" in json_response:
            self.error = "MapQuest API Key invalid"

        return self.error

    def _adapt_results(self, json_response):
        results = json_response.get("results", [])
        if results:
            return results[0]["locations"]

        return []


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


class MapQuestReverseResult(MapquestResult):
    @property
    def ok(self):
        return bool(self.quality)


class MapquestReverse(MapquestQuery):
    """
    MapQuest

    The geocoding service enables you to take an address and get the
    associated latitude and longitude. You can also use any latitude
    and longitude pair and get the associated address. Three types of
    geocoding are offered: address, reverse, and batch.

    API Reference: http://www.mapquestapi.com/geocoding/

    """

    _PROVIDER = "mapquest"
    _METHOD = "reverse"
    _URL = "http://www.mapquestapi.com/geocoding/v1/reverse"

    def _build_params(self, location, provider_key, **kwargs):
        return {
            "key": provider_key,
            "location": str(Location(location)),
            "maxResults": 1,
            "outFormat": "json",
        }


if __name__ == "__main__":
    g = MapquestQuery("Ottawa", max_results=3)
    g.debug()
