__all__ = ["BaiduQuery", "BaiduResult", "BaiduReverseResult", "BaiduReverse"]
import hashlib
import re
from collections import OrderedDict
from typing import Optional
from urllib.parse import quote, quote_plus, urlencode

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import baidu_key, baidu_security_key
from geocoder.location import Location


class BaiduResult(OneResult):
    @property
    def lat(self):
        return self.object_raw_json.get("location", {}).get("lat")

    @property
    def lng(self):
        return self.object_raw_json.get("location", {}).get("lng")

    @property
    def address(self) -> Optional[str]:
        """Object simple string address.

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support address property."
        )

    @property
    def quality(self):
        return self.object_raw_json.get("level")

    @property
    def confidence(self):
        return self.object_raw_json.get("confidence")


class BaiduQuery(MultipleResultsQuery):
    """
    Baidu Geocoding API

    Baidu Maps Geocoding API is a free open the API, the default quota
    one million times / day.

    References

    API Documentation: http://developer.baidu.com/map
    Get Baidu Key: http://lbsyun.baidu.com/apiconsole/key
    """

    _PROVIDER = "baidu"
    _METHOD = "geocode"
    _URL = "http://api.map.baidu.com/geocoder/v2/"
    _RESULT_CLASS = BaiduResult
    _KEY = baidu_key

    def _build_params(self, location, provider_key, **kwargs):
        coordtype = kwargs.get("coordtype", "wgs84ll")
        params = {
            "address": re.sub("[ ,]", "%", location),
            "output": "json",
            "ret_coordtype": coordtype,
            "ak": provider_key,
        }

        # adapt params to authentication method
        self.security_key = kwargs.get("sk", baidu_security_key)

        return self._encode_params(params) if self.security_key else params

    def _encode_params(self, params):
        # maintain the order of the parameters during signature creation when
        # returning results
        # signature is added to the end of the parameters
        ordered_params = sorted([(k, v) for (k, v) in params.items() if v])

        params = OrderedDict(ordered_params)

        # urlencode with Chinese symbols sabotage the query
        params["sn"] = self._sign_url("/geocoder/v2/", params, self.security_key)

        return params

    def _sign_url(self, base_url, params, security_key):
        """
        Signs a request url with a security key.
        """
        if not base_url or not security_key:
            return None

        params = params.copy()
        address = params.pop("address")

        url = f"{base_url}?address={address}&{urlencode(params)}"
        encoded_url = quote(url, safe="/:=&?#+!$,;'@()*[]")

        signature = quote_plus(encoded_url + self.security_key).encode("utf-8")

        return hashlib.md5(signature).hexdigest()

    def _build_headers(self, provider_key, **kwargs):
        return {"Referer": kwargs.get("referer", "http://developer.baidu.com")}

    def _adapt_results(self, json_response):
        return [json_response["result"]]

    def _catch_errors(self, json_response):
        status_code = json_response.get("status")
        if status_code != 0:
            self.status_code = status_code
            self.error = json_response.get("message")

        return self.error


class BaiduReverseResult(OneResult):
    @property
    def ok(self):
        return bool(self.address)

    @property
    def lat(self) -> Optional[float]:
        """Latitude of the object

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support lat property."
        )

    @property
    def lng(self) -> Optional[float]:
        """Longitude of the object

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support lng property."
        )

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
        return self.object_raw_json["addressComponent"]["city"]

    @property
    def district(self):
        return self.object_raw_json["addressComponent"]["district"]

    @property
    def street(self):
        return self.object_raw_json["addressComponent"]["street"]

    @property
    def house_number(self):
        return self.object_raw_json["addressComponent"]["street_number"]


class BaiduReverse(BaiduQuery):
    """
    Baidu Geocoding API

    Baidu Maps Geocoding API is a free open the API, the default quota
    one million times / day.

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
