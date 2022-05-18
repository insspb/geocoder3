__all__ = ["OttawaQuery"]

import logging
import re

from geocoder.base import MultipleResultsQuery, OneResult


class OttawaResult(OneResult):
    @property
    def lat(self):
        return self.raw_json.get("location", {}).get("y")

    @property
    def lng(self):
        return self.raw_json.get("location", {}).get("x")

    @property
    def postal(self):
        if self.address:
            expression = (
                r"([ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1}( *\d{1}[A-Z]{1}\d{1})?)"
            )
            pattern = re.compile(expression)
            match = pattern.search(self.address.upper())
            if match:
                return match.group(0)

    @property
    def house_number(self):
        if self.address:
            expression = r"\d+"
            pattern = re.compile(expression)
            match = pattern.search(self.address)
            if match:
                return int(match.group(0))

    @property
    def city(self):
        return "Ottawa"

    @property
    def state(self):
        return "Ontario"

    @property
    def country(self):
        return "Canada"

    @property
    def address(self):
        return self.raw_json.get("address")

    @property
    def accuracy(self):
        return self.raw_json.get("score")


class OttawaQuery(MultipleResultsQuery):
    """
    Ottawa ArcGIS REST Services

    Geocoding is the process of assigning a location, usually in the form of
    coordinate values (points), to an address by comparing the descriptive
    location elements in the address to those present in the reference
    material. Addresses come in many forms, ranging from the common address
    format of a house number followed by the street name and succeeding
    information to other location descriptions such as postal zone or census
    tract. An address includes any type of information that distinguishes
    a place.

    API Reference: http://maps.ottawa.ca/ArcGIS/rest/services/compositeLocator/
    GeocodeServer/findAddressCandidates
    """

    _PROVIDER = "ottawa"
    _METHOD = "geocode"
    _URL = "http://maps.ottawa.ca/ArcGIS/rest/services/compositeLocator/GeocodeServer/findAddressCandidates"  # noqa
    _RESULT_CLASS = OttawaResult
    _KEY_MANDATORY = False

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "SingleLine": location.replace(", Ottawa, ON", ""),
            "f": "json",
            "outSR": 4326,
            "maxLocations": max_results,
        }

    def _adapt_results(self, json_response):
        return json_response.get("candidates", [])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = OttawaQuery("1552 Payette dr.")
    g.debug()
