__all__ = [
    "BingResult",
    "BingQuery",
    "BingReverseResult",
    "BingReverse",
    "BingQueryDetail",
    "BingBatchResult",
    "BingBatch",
    "BingBatchForwardResult",
    "BingBatchForward",
    "BingBatchReverseResult",
    "BingBatchReverse",
]

import csv
import io
import logging
import re
import time
from typing import Optional

import requests

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import bing_key
from geocoder.location import Location

logger = logging.getLogger(__name__)


class BingResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._point = json_content.get("point", {})
        self._address = json_content.get("address", {})

        # proceed with super.__init__
        super(BingResult, self).__init__(json_content)

    @property
    def lat(self):
        coord = self._point["coordinates"]
        if coord:
            return coord[0]

    @property
    def lng(self):
        coord = self._point["coordinates"]
        if coord:
            return coord[1]

    @property
    def address(self):
        return self._address.get("formattedAddress")

    @property
    def house_number(self):
        if self.street:
            expression = r"\d+"
            pattern = re.compile(expression)
            match = pattern.search(self.street, re.UNICODE)
            if match:
                return match[0]

    @property
    def street(self):
        return self._address.get("addressLine")

    @property
    def neighborhood(self):
        return self._address.get("neighborhood")

    @property
    def city(self):
        return self._address.get("locality")

    @property
    def state(self):
        return self._address.get("adminDistrict")

    @property
    def country(self):
        return self._address.get("countryRegion")

    @property
    def quality(self):
        return self.object_raw_json.get("entityType")

    @property
    def accuracy(self):
        return self.object_raw_json.get("calculationMethod")

    @property
    def postal(self):
        return self._address.get("postalCode")

    @property
    def bbox(self):
        _bbox = self.object_raw_json.get("bbox")
        if _bbox:
            south = _bbox[0]
            north = _bbox[2]
            west = _bbox[1]
            east = _bbox[3]
            return self._get_bbox(south, west, north, east)


class BingQuery(MultipleResultsQuery):
    """
    Bing Maps REST Services

    The Bing™ Maps REST Services Application Programming Interface (API)
    provides a Representational State Transfer (REST) interface to
    perform tasks such as creating a static map with pushpins, geocoding
    an address, retrieving imagery metadata, or creating a route.

    API Reference: http://msdn.microsoft.com/en-us/library/ff701714.aspx
    Get Bing key: https://www.bingmapsportal.com/
    """

    _PROVIDER = "bing"
    _METHOD = "geocode"
    _URL = "http://dev.virtualearth.net/REST/v1/Locations"
    _RESULT_CLASS = BingResult
    _KEY = bing_key

    def _build_headers(self, provider_key, **kwargs):
        return {"Referer": "http://addxy.com/", "User-agent": "Mozilla/5.0"}

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "q": location,
            "o": "json",
            "inclnb": 1,
            "key": provider_key,
            "maxResults": max_results,
        }

    def _catch_errors(self, json_response):
        status = json_response["statusDescription"]
        if status != "OK":
            self.error = status

        return self.error

    def _adapt_results(self, json_response):
        # extract the array of JSON objects
        sets = json_response["resourceSets"]
        if sets:
            return sets[0]["resources"]
        return []


class BingReverseResult(BingResult):
    @property
    def ok(self):
        return bool(self.address)


class BingReverse(BingQuery):
    """
    Bing Maps REST Services

    The Bing™ Maps REST Services Application Programming Interface (API)
    provides a Representational State Transfer (REST) interface to
    perform tasks such as creating a static map with pushpins, geocoding
    an address, retrieving imagery metadata, or creating a route.

    API Reference: http://msdn.microsoft.com/en-us/library/ff701714.aspx
    """

    _PROVIDER = "bing"
    _METHOD = "reverse"

    _URL = "http://dev.virtualearth.net/REST/v1/Locations/{0}"

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "o": "json",
            "key": provider_key,
            "maxResults": max_results,
        }

    def _before_initialize(self, location, **kwargs):
        self.url = self.url.format(str(Location(location)))


class BingQueryDetail(MultipleResultsQuery):
    _PROVIDER = "bing"
    _METHOD = "details"

    _URL = "http://dev.virtualearth.net/REST/v1/Locations"
    _RESULT_CLASS = BingResult
    _KEY = bing_key

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "adminDistrict": kwargs.get("adminDistrict"),
            "countryRegion": kwargs.get("countryRegion"),
            "locality": kwargs.get("locality"),
            "postalCode": kwargs.get("postalCode"),
            "addressLine": kwargs.get("addressLine", location),
            "o": "json",
            "inclnb": 1,
            "key": provider_key,
            "maxResults": max_results,
        }

    def _catch_errors(self, json_response):
        status = json_response["statusDescription"]
        if status != "OK":
            self.error = status

        return self.error

    def _adapt_results(self, json_response):
        # extract the array of JSON objects
        sets = json_response["resourceSets"]
        if sets:
            return sets[0]["resources"]
        return []


class BingBatchResult(OneResult):
    # noinspection PyMissingConstructor
    def __init__(self, content):
        self._content = content

    @property
    def lat(self):
        coord = self._content
        if coord:
            return coord[0]

    @property
    def lng(self):
        coord = self._content
        if coord:
            return coord[1]

    @property
    def address(self) -> Optional[str]:
        """Object simple string address.

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support address property."
        )

    def debug(self):
        logger.debug("%s result", self.__class__.__name__)
        logger.debug("-----------")
        logger.debug(self._content)

        return [None, None]


class BingBatch(MultipleResultsQuery):
    """
    Bing Maps REST Services

    The Bing™ Maps REST Services Application Programming Interface (API)
    provides a Representational State Transfer (REST) interface to
    perform tasks such as creating a static map with pushpins, geocoding
    an address, retrieving imagery metadata, or creating a route.

    API Reference: http://msdn.microsoft.com/en-us/library/ff701714.aspx

    Dataflow Reference: https://msdn.microsoft.com/en-us/library/ff701733.aspx

    """

    _PROVIDER = "bing"
    _METHOD = "batch"
    _URL = "http://spatial.virtualearth.net/REST/v1/Dataflows/Geocode"
    _BATCH_TIMEOUT = 60
    _BATCH_WAIT = 5

    _RESULT_CLASS = BingBatchResult
    _KEY = bing_key

    def extract_resource_id(self, response):
        for rs in response["resourceSets"]:
            for resource in rs["resources"]:
                if "id" in resource:
                    return resource["id"]

        raise LookupError("No job ID returned from Bing batch call")

    def is_job_done(self, job_id):
        url = f"http://spatial.virtualearth.net/REST/v1/Dataflows/Geocode/{job_id}"
        response = self.session.get(
            url,
            params={"key": self.provider_key},
            timeout=self.timeout,
            proxies=self.proxies,
        )

        for rs in response.json()["resourceSets"]:
            for resource in rs["resources"]:
                if resource["id"] == job_id:
                    if resource["status"] == "Aborted":
                        raise LookupError("Bing job aborted")
                    return resource["status"] == "Completed"

        raise LookupError("Job ID not found in Bing answer - something is wrong")

    def get_job_result(self, job_id):
        url = f"http://spatial.virtualearth.net/REST/v1/Dataflows/Geocode/{job_id}/output/succeeded"  # noqa

        response = self.session.get(
            url,
            params={"key": self.provider_key},
            timeout=self.timeout,
            proxies=self.proxies,
        )

        return response.content

    def _build_params(self, locations, provider_key, **kwargs):
        self.batch = self.generate_batch(locations)
        self.locations_length = len(locations)
        self.provider_key = provider_key
        self._BATCH_TIMEOUT = kwargs.get("timeout", 60)

        return {"input": "csv", "key": provider_key}

    def _build_headers(self, provider_key, **kwargs):
        return {"Content-Type": "text/plain"}

    def _connect(self):
        self.status_code = "Unknown"

        try:
            self.response = response = self.session.post(
                self.url,
                data=self.batch,
                params=self.params,
                headers=self.headers,
                timeout=self.timeout,
                proxies=self.proxies,
            )

            # check that response is ok
            self.status_code = response.status_code
            response.raise_for_status()

            # rely on json method to get non-empty well formatted JSON
            json_response = response.json()
            self.url = response.url
            logger.info("Requested %s", self.url)

            # get the resource/job id
            resource_id = self.extract_resource_id(json_response)
            elapsed = 0

            # try for _BATCH_TIMEOUT seconds to retrieve the results of that job
            while elapsed < self._BATCH_TIMEOUT:
                if self.is_job_done(resource_id):
                    return self.get_job_result(resource_id)

                elapsed += self._BATCH_WAIT
                time.sleep(self._BATCH_WAIT)

            logger.error("Job was not finished in time.")

        except (requests.exceptions.RequestException, LookupError) as err:
            self.error = f"ERROR - {str(err)}"
            logger.error(
                "Status code %s from %s: %s", self.status_code, self.url, self.error
            )

        return False

    def _parse_results(self, response):
        rows = self._adapt_results(response)

        # re looping through the results to give them back in their original order
        for idx in range(self.locations_length):
            self.add(self._RESULT_CLASS(rows.get(str(idx), None)))

        self.current_result = len(self) > 0 and self[0]


class BingBatchForwardResult(BingBatchResult):
    @property
    def lat(self):
        coord = self._content
        if coord:
            return float(coord[0])

    @property
    def lng(self):
        coord = self._content
        if coord:
            return float(coord[1])

    @property
    def ok(self):
        return bool(self._content)

    def debug(self):
        logger.debug("Bing Batch result")
        logger.debug("-----------")
        logger.debug(self._content)

        return [None, None]


class BingBatchForward(BingBatch):
    _METHOD = "batch"
    _RESULT_CLASS = BingBatchForwardResult

    def generate_batch(self, addresses):
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(
            [
                "Id",
                "GeocodeRequest/Query",
                "GeocodeResponse/Point/Latitude",
                "GeocodeResponse/Point/Longitude",
            ]
        )

        for idx, address in enumerate(addresses):
            writer.writerow([idx, address, None, None])

        return "Bing Spatial Data Services, 2.0\n{}".format(out.getvalue()).encode(
            "utf-8"
        )

    def _adapt_results(self, response):
        result = io.StringIO(response.decode("utf-8"))
        # Skipping first line with Bing header
        next(result)

        return {
            row["Id"]: [
                row["GeocodeResponse/Point/Latitude"],
                row["GeocodeResponse/Point/Longitude"],
            ]
            for row in csv.DictReader(result)
        }


class BingBatchReverseResult(BingBatchResult):
    @property
    def address(self):
        address = self._content
        if address:
            return address[0]

    @property
    def city(self):
        city = self._content
        if city:
            return city[1]

    @property
    def postal(self):
        postal = self._content
        if postal:
            return postal[2]

    @property
    def state(self):
        state = self._content
        if state:
            return state[3]

    @property
    def country(self):
        country = self._content
        if country:
            return country[4]

    @property
    def ok(self):
        return bool(self._content)

    def debug(self):
        logger.debug("Bing Batch result")
        logger.debug("-----------")
        logger.debug(self._content)

        return [None, None]


class BingBatchReverse(BingBatch):

    _METHOD = "batch_reverse"
    _RESULT_CLASS = BingBatchReverseResult

    def generate_batch(self, locations):
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(
            [
                "Id",
                "ReverseGeocodeRequest/Location/Latitude",
                "ReverseGeocodeRequest/Location/Longitude",
                "GeocodeResponse/Address/FormattedAddress",
                "GeocodeResponse/Address/Locality",
                "GeocodeResponse/Address/PostalCode",
                "GeocodeResponse/Address/AdminDistrict",
                "GeocodeResponse/Address/CountryRegion",
            ]
        )

        for idx, location in enumerate(locations):
            writer.writerow(
                [idx, location[0], location[1], None, None, None, None, None]
            )

        return "Bing Spatial Data Services, 2.0\n{}".format(out.getvalue()).encode(
            "utf-8"
        )

    def _adapt_results(self, response):
        # print(type(response))
        result = io.StringIO(response.decode("utf-8"))
        # Skipping first line with Bing header
        next(result)

        return {
            row["Id"]: [
                row["GeocodeResponse/Address/FormattedAddress"],
                row["GeocodeResponse/Address/Locality"],
                row["GeocodeResponse/Address/PostalCode"],
                row["GeocodeResponse/Address/AdminDistrict"],
                row["GeocodeResponse/Address/CountryRegion"],
            ]
            for row in csv.DictReader(result)
        }
