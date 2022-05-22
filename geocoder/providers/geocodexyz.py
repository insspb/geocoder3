__all__ = ["GeocodeXYZQuery"]
import logging
from typing import Optional

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import geocodexyz_key


class GeocodeXYZResult(OneResult):
    def _get_value(self, json_obj, key, type_class=None):
        value = json_obj.get(key, {})
        if value:
            value = value.strip()
        if type_class and value:
            return type_class(value)
        return value

    def __init__(self, json_content):
        # create safe shortcuts
        self._standard = json_content.get("standard", {})

        # proceed with super.__init__
        super(GeocodeXYZResult, self).__init__(json_content)

    @property
    def lat(self):
        return self._get_value(self.object_raw_json, "latt", float)

    @property
    def lng(self):
        return self._get_value(self.object_raw_json, "longt", float)

    @property
    def remaining_credits(self):
        return self._get_value(self.object_raw_json, "remaining_credits", int)

    @property
    def confidence(self):
        return self._get_value(self._standard, "confidence", float)

    @property
    def country(self):
        return self._get_value(self._standard, "countryname")

    @property
    def country_code(self):
        return self._get_value(self._standard, "prov")

    @property
    def city(self):
        return self._get_value(self._standard, "city")

    @property
    def region(self):
        return self._get_value(self._standard, "region")

    @property
    def street(self):
        return self._get_value(self._standard, "addresst")

    @property
    def postal(self):
        return self._get_value(self._standard, "postal")

    @property
    def house_number(self):
        return self.street_number

    @property
    def street_number(self) -> Optional[str]:
        return self._get_value(self._standard, "stnumber")

    @property
    def address(self):
        if self.street_number:
            return "{0} {1}, {2}".format(self.street_number, self.street, self.city)
        elif self.street and self.street != "un-known":
            return "{0}, {1}".format(self.street, self.city)
        else:
            return self.city


class GeocodeXYZQuery(MultipleResultsQuery):
    """API to retrieve data from geocode.xyz

    Geocode.xyz uses only open data sources, including but not limited to
    OpenStreetMap, Geonames, Osmnames, openaddresses.io, UK Ordnance Survey,
    www.dati.gov.it, data.europa.eu/euodp/en/data, PSMA Geocoded National
    Address File (Australia), etc.

    """

    _PROVIDER = "geocodexyz"
    _METHOD = "geocode"
    _URL = "https://geocode.xyz/"
    _RESULT_CLASS = GeocodeXYZResult
    _KEY = geocodexyz_key
    _KEY_MANDATORY = False

    def _build_params(self, location, provider_key, **kwargs):
        params = {
            "json": 1,
            "locate": location,
        }
        if "region" in kwargs:
            region = kwargs.pop("region")
            if region:
                params["region"] = region
        if "strictmode" in kwargs:
            params["strictmode"] = kwargs.pop("strictmode")
        if "strict" in kwargs:
            params["strict"] = kwargs.pop("strict")
        params["auth"] = kwargs.pop("auth") if "auth" in kwargs else provider_key
        return params

    def _adapt_results(self, json_response):
        return [json_response]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = GeocodeXYZQuery("1552 Payette dr., Ottawa")
    g.debug()
