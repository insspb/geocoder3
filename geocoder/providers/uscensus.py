__all__ = [
    "USCensusResult",
    "USCensusQuery",
    "USCensusBatchResult",
    "USCensusBatch",
    "USCensusReverseResult",
    "USCensusReverse",
]

import csv
import io
import logging
import re
from typing import Optional

import requests

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.location import Location

logger = logging.getLogger(__name__)


class USCensusResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._coordinates = json_content.get("coordinates", {})
        self._address_components = json_content.get("addressComponents", {})

        # proceed with super.__init__
        super(USCensusResult, self).__init__(json_content)

    @property
    def lat(self):
        return self._coordinates.get("y")

    @property
    def lng(self):
        return self._coordinates.get("x")

    @property
    def address(self):
        return self.object_raw_json.get("matchedAddress")

    @property
    def house_number(self):
        if self.address:
            match = re.search(r"^\d+", self.address, re.UNICODE)
            if match:
                return match[0]

    @property
    def fromhousenumber(self):
        return self._address_components.get("fromAddress")

    @property
    def tohousenumber(self):
        return self._address_components.get("toAddress")

    @property
    def streetname(self):
        return self._address_components.get("streetName")

    @property
    def prequalifier(self):
        return self._address_components.get("preQualifier")

    @property
    def predirection(self):
        return self._address_components.get("preDirection")

    @property
    def pretype(self):
        return self._address_components.get("preType")

    @property
    def suffixtype(self):
        return self._address_components.get("suffixType")

    @property
    def suffixdirection(self):
        return self._address_components.get("suffixDirection")

    @property
    def suffixqualifier(self):
        return self._address_components.get("suffixQualifier")

    @property
    def city(self):
        return self._address_components.get("city")

    @property
    def state(self):
        return self._address_components.get("state")

    @property
    def postal(self):
        return self._address_components.get("zip")


class USCensusQuery(MultipleResultsQuery):
    """
    US Census Geocoder REST Services

    The Census Geocoder is an address look-up tool that converts your address to an
    approximate coordinate (latitude/longitude) and returns information about the
    address range that includes the address and the census geography the address is
    within. The geocoder is available as a web interface and as an API
    (Representational State Transfer - REST - web-based service).

    API Reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
    """

    _PROVIDER = "uscensus"
    _METHOD = "geocode"
    _URL = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    _RESULT_CLASS = USCensusResult
    _KEY_MANDATORY = False

    def _build_params(self, location, provider_key, **kwargs):
        return {
            "address": location,
            "benchmark": kwargs.get("benchmark", "4"),
            "format": "json",
        }

    def _adapt_results(self, json_response):
        return json_response["result"]["addressMatches"]


class USCensusBatchResult(OneResult):
    def __init__(self, content):
        self._content = content

        if self._content:
            self._coordinates = tuple(float(pos) for pos in content[1].split(","))

        # proceed with super.__init__
        super(USCensusBatchResult, self).__init__(content)

    @property
    def lat(self):
        if self._content:
            return self._coordinates[1]

    @property
    def lng(self):
        if self._content:
            return self._coordinates[0]

    @property
    def address(self):
        if self._content:
            return self._content[0]


class USCensusBatch(MultipleResultsQuery):
    """
    US Census Geocoder REST Services

    The Census Geocoder is an address look-up tool that converts your address to an
    approximate coordinate (latitude/longitude) and returns information about the
    address range that includes the address and the census geography the address is
    within. The geocoder is available as a web interface and as an API
    (Representational State Transfer - REST - web-based service).

    API Reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html

    """

    _PROVIDER = "uscensus"
    _METHOD = "batch"
    _URL = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
    _RESULT_CLASS = USCensusBatchResult
    _KEY_MANDATORY = False

    def generate_batch(self, locations):
        out = io.StringIO()
        writer = csv.writer(out)

        for idx, address in enumerate(locations):
            writer.writerow([idx, address, None, None, None])

        return out.getvalue().encode("utf-8")

    def _build_params(self, locations, provider_key, **kwargs):
        self.batch = self.generate_batch(locations)
        self.locations_length = len(locations)
        self.timeout = int(
            kwargs.get("timeout", "1800")
        )  # 30mn timeout, us census can be really slow with big batches
        self.benchmark = str(kwargs.get("benchmark", 4))

        return {
            "benchmark": (None, self.benchmark),
            "addressFile": ("addresses.csv", self.batch),
        }

    def _connect(self):
        self.status_code = "Unknown"

        try:
            self.response = response = self.session.post(
                self.url,
                files=self.params,
                headers=self.headers,
                timeout=self.timeout,
                proxies=self.proxies,
            )

            # check that response is ok
            self.status_code = response.status_code
            response.raise_for_status()

            return response.content

        except (requests.exceptions.RequestException, LookupError) as err:
            self.error = f"ERROR - {str(err)}"
            logger.error(
                "Status code %s from %s: %s", self.status_code, self.url, self.error
            )

        return False

    def _adapt_results(self, response):
        result = io.StringIO(response.decode("utf-8"))

        return {
            row[0]: [row[4], row[5]] for row in csv.reader(result) if row[2] == "Match"
        }

    def _parse_results(self, response):
        rows = self._adapt_results(response)

        # re looping through the results to give them back in their original order
        for idx in range(self.locations_length):
            self.add(self._RESULT_CLASS(rows.get(str(idx), None)))

        self.current_result = len(self) > 0 and self[0]


class USCensusReverseResult(OneResult):
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
        """Latitude of the object

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support lng property."
        )

    @property
    def address(self) -> Optional[str]:
        """Object simple string address.

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support address property."
        )

    @property
    def ok(self):
        return bool(self.object_raw_json["States"])

    @property
    def state(self):
        if self.object_raw_json["States"]:
            return self.object_raw_json["States"][0].get("NAME")

    @property
    def statenumber(self):
        if self.object_raw_json["States"]:
            return self.object_raw_json["States"][0].get("STATE")

    @property
    def county(self):
        if self.object_raw_json["Counties"]:
            return self.object_raw_json["Counties"][0].get("NAME")

    @property
    def countynumber(self):
        if self.object_raw_json["Counties"]:
            return self.object_raw_json["Counties"][0].get("COUNTY")

    @property
    def tract(self):
        if self.object_raw_json["Census Tracts"]:
            return self.object_raw_json["Census Tracts"][0].get("NAME")

    @property
    def tractnumber(self):
        if self.object_raw_json["Census Tracts"]:
            return self.object_raw_json["Census Tracts"][0].get("TRACT")

    @property
    def block(self):
        if self.object_raw_json["2010 Census Blocks"]:
            return self.object_raw_json["2010 Census Blocks"][0].get("NAME")
        elif self.object_raw_json["Census Blocks"]:
            return self.object_raw_json["Census Blocks"][0].get("NAME")

    @property
    def blocknumber(self):
        if self.object_raw_json["2010 Census Blocks"]:
            return self.object_raw_json["2010 Census Blocks"][0].get("BLOCK")
        elif self.object_raw_json["Census Blocks"]:
            return self.object_raw_json["Census Blocks"][0].get("BLOCK")

    @property
    def geoid(self):
        if self.object_raw_json["2010 Census Blocks"]:
            return self.object_raw_json["2010 Census Blocks"][0].get("GEOID")
        elif self.object_raw_json["Census Blocks"]:
            return self.object_raw_json["Census Blocks"][0].get("GEOID")


class USCensusReverse(USCensusQuery):
    """
    US Census Geocoder REST Services

    The Census Geocoder is an address look-up tool that converts your address to an
    approximate coordinate (latitude/longitude) and returns information about the
    address range that includes the address and the census geography the address is
    within. The geocoder is available as a web interface and as an API
    (Representational State Transfer - REST - web-based service).

    API Reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf

    """

    _PROVIDER = "uscensus"
    _METHOD = "reverse"
    _URL = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
    _RESULT_CLASS = USCensusReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "x": location.longitude,
            "y": location.latitude,
            "benchmark": kwargs.get("benchmark", "4"),
            "vintage": kwargs.get("vintage", "4"),
            "format": "json",
        }

    def _adapt_results(self, json_response):
        return [json_response["result"]["geographies"]]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    g = USCensusQuery("4600 Silver Hill Road, Suitland, MD 20746", benchmark=9)
    g.debug()
