__all__ = ["BaiduReverse"]

import logging

from geocoder.base import OneResult
from geocoder.location import Location
from geocoder.providers.addresses import BaiduQuery


class BaiduReverseResult(OneResult):
    @property
    def ok(self):
        return bool(self.address)

    @property
    def address(self):
        return self.raw_json["formatted_address"]

    @property
    def country(self):
        return self.raw_json["addressComponent"]["country"]

    @property
    def province(self):
        return self.raw_json["addressComponent"]["province"]

    @property
    def state(self):
        return self.raw_json["addressComponent"]["province"]

    @property
    def city(self):
        return self.raw_json["addressComponent"]["city"]

    @property
    def district(self):
        return self.raw_json["addressComponent"]["district"]

    @property
    def street(self):
        return self.raw_json["addressComponent"]["street"]

    @property
    def house_number(self):
        return self.raw_json["addressComponent"]["street_number"]


class BaiduReverse(BaiduQuery):
    """
    Baidu Geocoding API

    Baidu Maps Geocoding API is a free open the API, the default quota
    one million times / day.

    :param location: Your search location you want geocoded.
    :param key: Baidu API key.
    :param referer: Baidu API referer website.

    API Documentation: http://developer.baidu.com/map
    Get Baidu Key: http://lbsyun.baidu.com/apiconsole/key
    """

    _PROVIDER = "baidu"
    _METHOD = "reverse"
    _URL = "http://api.map.baidu.com/geocoder/v2/"
    _RESULT_CLASS = BaiduReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        params = {
            "location": str(location),
            "ret_coordtype": kwargs.get("coordtype", "wgs84ll"),
            "output": "json",
            "ak": provider_key,
        }
        if "lang_code" in kwargs:
            params["accept-language"] = kwargs["lang_code"]

        return params


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = BaiduReverse("39.983424,116.32298", key="")
    g.debug()
