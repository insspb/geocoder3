__all__ = ["IpinfoQuery"]

import logging

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import ipinfo_key
from geocoder.location import Location


class IpinfoResult(OneResult):
    @property
    def lat(self):
        loc = self.object_raw_json.get("loc")
        if loc:
            return Location(loc).lat

    @property
    def lng(self):
        loc = self.object_raw_json.get("loc")
        if loc:
            return Location(loc).lng

    @property
    def address(self):
        if self.city:
            return "{0}, {1}, {2}".format(self.city, self.state, self.country)
        elif self.state:
            return "{0}, {1}".format(self.state, self.country)
        elif self.country:
            return "{0}".format(self.country)
        else:
            return ""

    @property
    def postal(self):
        return self.object_raw_json.get("postal")

    @property
    def city(self):
        return self.object_raw_json.get("city")

    @property
    def state(self):
        return self.object_raw_json.get("region")

    @property
    def country(self):
        return self.object_raw_json.get("country")

    @property
    def hostname(self):
        return self.object_raw_json.get("hostname")

    @property
    def ip(self):
        return self.object_raw_json.get("ip")

    @property
    def org(self):
        return self.object_raw_json.get("org")


class IpinfoQuery(MultipleResultsQuery):
    """
    API Reference: https://ipinfo.io
    """

    _PROVIDER = "ipinfo"
    _METHOD = "geocode"
    _URL = "http://ipinfo.io/json"
    _RESULT_CLASS = IpinfoResult
    _KEY = ipinfo_key
    _KEY_MANDATORY = False

    def _build_headers(self, provider_key, **kwargs):
        return {
            "Authorization": "Bearer {}".format(provider_key),
        }

    def _build_params(self, location, provider_key, **kwargs):
        return {}

    def _before_initialize(self, location, **kwargs):
        if location.lower() == "me" or location == "":
            self.url = "http://ipinfo.io/json"
        else:
            self.url = "http://ipinfo.io/{0}/json".format(self.location)

    def _adapt_results(self, json_response):
        return [json_response]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = IpinfoQuery("8.8.8.8")
    g.debug()
