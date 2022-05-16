__all__ = ["MapquestResult", "MapquestQuery"]

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import mapquest_key
from geocoder.location import BBox


class MapquestResult(OneResult):
    @property
    def lat(self):
        return self.raw_json.get("latLng", {}).get("lat")

    @property
    def lng(self):
        return self.raw_json.get("latLng", {}).get("lng")

    @property
    def street(self):
        return self.raw_json.get("street")

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
        return self.raw_json.get("geocodeQuality")

    @property
    def postal(self):
        return self.raw_json.get("postalCode")

    @property
    def neighborhood(self):
        return self.raw_json.get("adminArea6")

    @property
    def city(self):
        return self.raw_json.get("adminArea5")

    @property
    def county(self):
        return self.raw_json.get("adminArea4")

    @property
    def state(self):
        return self.raw_json.get("adminArea3")

    @property
    def country(self):
        return self.raw_json.get("adminArea1")


class MapquestQuery(MultipleResultsQuery):
    """
    MapQuest

    The geocoding service enables you to take an address and get the
    associated latitude and longitude. You can also use any latitude
    and longitude pair and get the associated address. Three types of
    geocoding are offered: address, reverse, and batch.

    API Reference: http://www.mapquestapi.com/geocoding/
    """

    provider = "mapquest"
    method = "geocode"

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


if __name__ == "__main__":
    g = MapquestQuery("Ottawa", max_results=3)
    g.debug()
