__all__ = ["GeolyticaQuery", "GeolyticaResult"]
from typing import Optional

from geocoder.base import MultipleResultsQuery, OneResult


def _correct_empty_dict(obj, key, alt=""):
    try:
        k = obj.get(key, alt).strip()
    except AttributeError:
        k = alt
    return k


class GeolyticaResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._standard = json_content.get("standard", {})

        # proceed with super.__init__
        super(GeolyticaResult, self).__init__(json_content)

    @property
    def lat(self):
        lat = _correct_empty_dict(self.object_raw_json, "latt")
        if lat:
            return float(lat)

    @property
    def lng(self):
        lng = _correct_empty_dict(self.object_raw_json, "longt")
        if lng:
            return float(lng)

    @property
    def postal(self):
        return _correct_empty_dict(self.object_raw_json, "postal")

    @property
    def house_number(self):
        return self.street_number

    @property
    def street_number(self) -> Optional[str]:
        return _correct_empty_dict(self._standard, "stnumber")

    @property
    def street(self):
        return _correct_empty_dict(self._standard, "staddress")

    @property
    def city(self):
        return _correct_empty_dict(self._standard, "city")

    @property
    def state(self):
        return _correct_empty_dict(self._standard, "prov")

    @property
    def address(self):
        if self.street_number:
            return "{0} {1}, {2}".format(self.street_number, self.street, self.city)
        elif self.street and self.street != "un-known":
            return "{0}, {1}".format(self.street, self.city)
        else:
            return self.city


class GeolyticaQuery(MultipleResultsQuery):
    """
    Geocoder.ca

    A Canadian and US location geocoder.

    API Reference: http://geocoder.ca/?api=1
    """

    _PROVIDER = "geolytica"
    _METHOD = "geocode"
    _URL = "http://geocoder.ca"
    _RESULT_CLASS = GeolyticaResult
    _KEY_MANDATORY = False

    def _build_params(self, location, provider_key, **kwargs):
        params = {"json": 1, "locate": location, "geoit": "xml"}
        if "strictmode" in kwargs:
            params["strictmode"] = kwargs.pop("strictmode")
        if "strict" in kwargs:
            params["strict"] = kwargs.pop("strict")
        if "auth" in kwargs:
            params["auth"] = kwargs.pop("auth")
        return params

    def _adapt_results(self, json_response):
        return [json_response]
