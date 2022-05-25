__all__ = [
    "GeonamesResult",
    "GeonamesQuery",
    "GeonamesFullResult",
    "GeonamesDetails",
    "GeonamesChildren",
    "GeonamesHierarchy",
    "GeonamesTimezoneResult",
    "GeonamesTimezone",
]
import logging

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import geonames_username
from geocoder.location import BBox, Location

logger = logging.getLogger(__name__)


class GeonamesResult(OneResult):
    @property
    def lat(self):
        return self.object_raw_json.get("lat")

    @property
    def lng(self):
        return self.object_raw_json.get("lng")

    @property
    def geonames_id(self):
        return self.object_raw_json.get("geonameId")

    @property
    def address(self):
        return self.object_raw_json.get("name")

    @property
    def feature_class(self):
        return self.object_raw_json.get("fcl")

    @property
    def class_description(self):
        return self.object_raw_json.get("fclName")

    @property
    def code(self):
        return self.object_raw_json.get("fcode")

    @property
    def description(self):
        return self.object_raw_json.get("fcodeName")

    @property
    def state(self):
        return self.object_raw_json.get("adminName1")

    @property
    def state_code(self):
        return self.object_raw_json.get("adminCode1")

    @property
    def country(self):
        return self.object_raw_json.get("countryName")

    @property
    def country_code(self):
        return self.object_raw_json.get("countryCode")

    @property
    def population(self):
        return self.object_raw_json.get("population")


class GeonamesQuery(MultipleResultsQuery):
    """
    GeoNames REST Web Services

    GeoNames is mainly using REST webservices. Find nearby postal codes / reverse
    geocoding
    This service comes in two flavors.You can either pass the lat/long or a
    postalcode/place name.

    API Reference: http://www.geonames.org/export/web-services.html
    """

    _PROVIDER = "geonames"
    _METHOD = "geocode"
    _URL = "http://api.geonames.org/searchJSON"
    _RESULT_CLASS = GeonamesResult
    _KEY = geonames_username

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        """Will be overridden according to the targeted web service"""
        base_kwargs = {
            "q": location,
            "fuzzy": kwargs.get("fuzzy", 1.0),
            "username": provider_key,
            "maxRows": max_results,
        }
        # check out for bbox in kwargs
        bbox = kwargs.pop("proximity", None)
        if bbox is not None:
            bbox = BBox.factory(bbox)
            base_kwargs.update(
                {
                    "east": bbox.east,
                    "west": bbox.west,
                    "north": bbox.north,
                    "south": bbox.south,
                }
            )

        # look out for valid extra kwargs
        supported_kwargs = {
            "name",
            "name_equals",
            "name_startsWith",
            "startRow",
            "country",
            "countryBias",
            "continentCode",
            "adminCode1",
            "adminCode2",
            "adminCode3",
            "cities",
            "featureClass",
            "featureCode",
            "lang",
            "type",
            "style",
            "isNameRequired",
            "tag",
            "operator",
            "charset",
            "east",
            "west",
            "north",
            "south",
            "orderby",
            "inclBbox",
            "searchlang",
        }

        found_kwargs = supported_kwargs & set(kwargs.keys())
        logger.debug("Adding extra kwargs %s", found_kwargs)

        # update base kwargs with extra ones
        base_kwargs.update(dict([(extra, kwargs[extra]) for extra in found_kwargs]))
        return base_kwargs

    def _catch_errors(self, json_response):
        """Changed: removed check on number of elements:
        - totalResultsCount not systematically returned (e.g in hierarchy)
        - done in base.py
        """
        status = json_response.get("status")
        if status:
            message = status.get("message")
            value = status.get("value")
            custom_messages = {
                10: "Invalid credentials",
                18: "Do not use the demo account for your application",
            }
            self.error = custom_messages.get(value, message)
            logger.error("Error %s from JSON %s", self.error, json_response)

        return self.error

    def _adapt_results(self, json_response):
        # extract the array of JSON objects
        return json_response["geonames"]


class GeonamesFullResult(GeonamesResult):
    """
    Get information for given geonames_id, e.g. timezone and administrative hierarchy
    """

    @property
    def continent(self):
        return self.object_raw_json.get("continentCode", "")

    @property
    def country_geonames_id(self):
        return self.object_raw_json.get("countryId", 0)

    @property
    def state_geonames_id(self):
        return self.object_raw_json.get("adminId1", 0)

    @property
    def admin2(self):
        return self.object_raw_json.get("adminName2", "")

    @property
    def admin2_geonames_id(self):
        return self.object_raw_json.get("adminId2", "")

    @property
    def admin3(self):
        return self.object_raw_json.get("adminName3", "")

    @property
    def admin3_geonames_id(self):
        return self.object_raw_json.get("adminId3", "")

    @property
    def admin4(self):
        return self.object_raw_json.get("adminName4", "")

    @property
    def admin4_geonames_id(self):
        return self.object_raw_json.get("adminId4", "")

    @property
    def admin5(self):
        return self.object_raw_json.get("adminName5", "")

    @property
    def admin5_geonames_id(self):
        return self.object_raw_json.get("adminId5", "")

    @property
    def srtm3(self):
        return self.object_raw_json.get("srtm3", 0)

    @property
    def wikipedia(self):
        return self.object_raw_json.get("wikipediaURL", "")

    @property
    def timeZoneId(self):
        timezone = self.object_raw_json.get("timezone")
        if timezone:
            return timezone.get("timeZoneId")

    @property
    def timeZoneName(self):
        timezone = self.object_raw_json.get("timezone")
        if timezone:
            return timezone.get("timeZoneId")

    @property
    def rawOffset(self):
        timezone = self.object_raw_json.get("timezone")
        if timezone:
            return timezone.get("gmtOffset")

    @property
    def dstOffset(self):
        timezone = self.object_raw_json.get("timezone")
        if timezone:
            return timezone.get("dstOffset")

    @property
    def bbox(self):
        bbox = self.object_raw_json.get("bbox", {})
        south = bbox.get("south")
        west = bbox.get("west")
        north = bbox.get("north")
        east = bbox.get("east")
        return self._get_bbox(south, west, north, east)


class GeonamesDetails(GeonamesQuery):
    """Details:
    http://api.geonames.org/getJSON?geonameId=6094817&style=full
    """

    _PROVIDER = "geonames"
    _METHOD = "details"
    _URL = "http://api.geonames.org/getJSON"
    _RESULT_CLASS = GeonamesFullResult

    def _build_params(self, location, provider_key, **kwargs):
        """Will be overridden according to the targeted web service"""
        return {"geonameId": location, "username": provider_key, "style": "full"}

    def _adapt_results(self, json_response):
        # the returned JSON contains the object.
        # Need to wrap it into an array
        return [json_response]


class GeonamesChildren(GeonamesQuery):
    """Children:
    http://api.geonames.org/childrenJSON?formatted=true&geonameId=6094817
    """

    _PROVIDER = "geonames"
    _METHOD = "children"

    _URL = "http://api.geonames.org/childrenJSON"

    def _build_params(self, location, provider_key, **kwargs):
        """Will be overridden according to the targeted web service"""
        return {
            "geonameId": location,
            "username": provider_key,
        }


class GeonamesHierarchy(GeonamesChildren):
    """Hierarchy:
    http://api.geonames.org/hierarchyJSON?formatted=true&geonameId=6094817
    """

    _PROVIDER = "geonames"
    _METHOD = "hierarchy"

    _URL = "http://api.geonames.org/hierarchyJSON"


class GeonamesTimezoneResult(GeonamesResult):
    """Get timezone information for given lat,lng"""

    @property
    def sunrise(self):
        return self.object_raw_json.get("sunrise")

    @property
    def gmt_offset(self):
        return self.object_raw_json.get("gmtOffset")

    @property
    def raw_offset(self):
        return self.object_raw_json.get("rawOffset")

    @property
    def dst_offset(self):
        return self.object_raw_json.get("dstOffset")

    @property
    def sunset(self):
        return self.object_raw_json.get("sunset")

    @property
    def timezone_id(self):
        return self.object_raw_json.get("timezoneId")

    @property
    def time(self):
        return self.object_raw_json.get("time")


class GeonamesTimezone(GeonamesQuery):
    """Details:
    http://api.geonames.org/timezoneJSON?lat=47.01&lng=10.2
    """

    _PROVIDER = "geonames"
    _METHOD = "timezone"
    _URL = "http://api.geonames.org/timezoneJSON"
    _RESULT_CLASS = GeonamesTimezoneResult

    def _build_params(self, location, provider_key, **kwargs):
        """Will be overridden according to the targeted web service"""
        location = Location(location)
        return {
            "lat": location.latitude,
            "lng": location.longitude,
            "username": provider_key,
        }

    def _adapt_results(self, json_response):
        # the returned JSON contains the object.
        # Need to wrap it into an array
        return [json_response]
