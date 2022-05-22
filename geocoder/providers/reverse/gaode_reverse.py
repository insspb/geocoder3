__all__ = ["GaodeReverse"]

import logging

from geocoder.base import OneResult
from geocoder.location import Location
from geocoder.providers.addresses import GaodeQuery


class GaodeReverseResult(OneResult):
    @property
    def ok(self):
        return bool(self.address)

    @property
    def address(self):
        return self.object_raw_json["formatted_address"]

    @property
    def country(self):
        return self.object_raw_json["addressComponent"]["country"]

    @property
    def province(self):
        return self.object_raw_json["addressComponent"]["province"]

    @property
    def state(self):
        return self.object_raw_json["addressComponent"]["province"]

    @property
    def city(self):
        if len(self.object_raw_json["addressComponent"]["city"]) == 0:
            return self.object_raw_json["addressComponent"]["province"]
        else:
            return self.object_raw_json["addressComponent"]["city"]

    @property
    def district(self):
        return self.object_raw_json["addressComponent"]["district"]

    @property
    def street(self):
        return self.object_raw_json["addressComponent"]["streetNumber"]["street"]

    @property
    def adcode(self):
        return self.object_raw_json["addressComponent"]["adcode"]

    @property
    def township(self):
        return self.object_raw_json["addressComponent"]["township"]

    @property
    def towncode(self):
        return self.object_raw_json["addressComponent"]["towncode"]

    @property
    def house_number(self):
        return self.object_raw_json["addressComponent"]["streetNumber"]["number"]


class GaodeReverse(GaodeQuery):
    """
    Gaode GeoReverse API

    Gaode Maps GeoReverse API is a free open the API, the default quota
    2000 times / day.

    :param location: Your search location you want geocoded.
    :param key: Gaode API key.
    :param referer: Gaode API referer website.

    API Documentation: http://lbs.amap.com/api/webservice/guide/api/georegeo
    Get Gaode AMap Key: http://lbs.amap.com/dev/
    """

    _PROVIDER = "gaode"
    _METHOD = "reverse"
    _URL = "http://restapi.amap.com/v3/geocode/regeo"
    _RESULT_CLASS = GaodeReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "location": str(location.lng) + "," + str(location.lat),
            "output": "json",
            "key": provider_key,
        }

    def _adapt_results(self, json_response):
        return [json_response["regeocode"]]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = GaodeReverse("39.971577, 116.506142")
    g.debug()
