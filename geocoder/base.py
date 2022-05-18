"""
Base classes of provider definition responsible for minimum set of methods and
properties, that should be implemented or overridden in all nested providers.
"""
import json
import logging
from collections import OrderedDict
from collections.abc import MutableSequence
from typing import Optional
from urllib.parse import urlparse

import requests

from geocoder.distance import Distance

logger = logging.getLogger(__name__)


class OneResult(object):
    """Container for one (JSON) object returned by provider"""

    _TO_EXCLUDE = [
        "parse",
        "json",
        "url",
        "fieldnames",
        "help",
        "debug",
        "short_name",
        "api",
        "content",
        "params",
        "street_number",
        "api_key",
        "key",
        "id",
        "x",
        "y",
        "latlng",
        "headers",
        "timeout",
        "wkt",
        "locality",
        "province",
        "rate_limited_get",
        "osm",
        "route",
        "schema",
        "properties",
        "geojson",
        "tree",
        "error",
        "proxies",
        "road",
        "xy",
        "northeast",
        "northwest",
        "southeast",
        "southwest",
        "road_long",
        "city_long",
        "state_long",
        "country_long",
        "postal_town_long",
        "province_long",
        "road_long",
        "street_long",
        "interpolated",
        "method",
        "geometry",
        "session",
    ]

    def __init__(self, json_content):

        self.object_raw_json = json_content

        # attributes required to compute bbox
        self.northeast = []
        self.northwest = []
        self.southeast = []
        self.southwest = []

        # attributes returned in JSON format
        self.fieldnames = []
        self.json = {}
        self._parse_json_with_fieldnames()

    # Essential attributes for Quality Control
    @property
    def lat(self) -> Optional[float]:
        """Latitude of the object"""
        return None

    @property
    def lng(self) -> Optional[float]:
        """Longitude of the object"""
        return None

    # Bounding Box attributes
    @property
    def bbox(self) -> dict:
        """Object bounding box when can be calculated/retrieved."""
        return {}

    # Essential attributes for Street Address
    @property
    def address(self) -> Optional[str]:
        """Object simple string address."""
        return None

    def __repr__(self) -> str:
        """Display [address] if available; [lat,lng] otherwise"""
        return f"[{self.address}]" if self.address else f"[{self.lat}, {self.lng}]"

    def _parse_json_with_fieldnames(self):
        """Parse the raw JSON with all attributes/methods defined in the class, except for the
        ones defined starting with '_' or flagged in cls._TO_EXCLUDE.

        The final result is stored in self.json
        """
        for key in dir(self):
            if not key.startswith("_") and key not in self._TO_EXCLUDE:
                self.fieldnames.append(key)
                value = getattr(self, key)
                if value:
                    self.json[key] = value
        # Add OK attribute even if value is "False"
        self.json["ok"] = self.ok

    @property
    def ok(self) -> bool:
        """
        Status of retrieving location/IP coordinates or reverse geocoding.

        Usually should be replaced in reverse results class.
        """
        return bool(self.lng and self.lat)

    @property
    def status(self) -> str:
        if self.ok:
            return "OK"
        if not self.address:
            return "ERROR - No results found"
        return "ERROR - No Geometry"

    def debug(self):
        logger.debug("From provider")
        logger.debug("-------------")
        logger.debug(json.dumps(self.object_raw_json, indent=4))
        logger.debug("Cleaned json")
        logger.debug("------------")
        logger.debug(json.dumps(self.json, indent=4))

    def _get_bbox(self, south, west, north, east) -> dict:
        if not all([south, east, north, west]):
            return {}

        # South Latitude, West Longitude, North Latitude, East Longitude
        self.south = float(south)
        self.west = float(west)
        self.north = float(north)
        self.east = float(east)

        # Bounding Box Corners
        self.northeast = [self.north, self.east]
        self.northwest = [self.north, self.west]
        self.southwest = [self.south, self.west]
        self.southeast = [self.south, self.east]

        return dict(northeast=self.northeast, southwest=self.southwest)

    @property
    def confidence(self) -> int:
        """
        Is as a measure of how confident we are that centre point coordinates returned
        for the result precisely reflect the result.
        """
        if not self.bbox:
            # Cannot determine score
            return 0

        # Units are measured in Kilometers
        distance = Distance(self.northeast, self.southwest, units="km")
        for score, maximum in [
            (10, 0.25),
            (9, 0.5),
            (8, 1),
            (7, 5),
            (6, 7.5),
            (5, 10),
            (4, 15),
            (3, 20),
            (2, 25),
        ]:
            if distance < maximum:
                return score
            if distance >= 25:
                return 1

    @property
    def geometry(self) -> dict:
        return {"type": "Point", "coordinates": [self.x, self.y]} if self.ok else {}

    @property
    def geojson(self) -> dict:
        feature = {
            "type": "Feature",
            "properties": self.json,
        }
        if self.bbox:
            feature["bbox"] = [self.west, self.south, self.east, self.north]
            feature["properties"]["bbox"] = feature["bbox"]
        if self.geometry:
            feature["geometry"] = self.geometry
        return feature

    @property
    def wkt(self) -> Optional[str]:
        """Output coordinates in well-known text format, no SRID data."""
        return f"POINT({self.x} {self.y})" if self.ok else None

    @property
    def xy(self) -> Optional[list]:
        """Optional list of longitude and latitude values."""
        return [self.lng, self.lat] if self.ok else None

    @property
    def latlng(self) -> Optional[list]:
        """Optional list of latitude and longitude values."""
        return [self.lat, self.lng] if self.ok else None

    @property
    def y(self) -> Optional[float]:
        """Latitude of the object"""
        return self.lat

    @property
    def x(self) -> Optional[float]:
        """Longitude of the object"""
        return self.lng


class MultipleResultsQuery(MutableSequence):
    """
    Base results and query manager container

    This class responsible for checking correct new provider files creation before it
    will be implemented in project. Such checks done in :func:`__init_subclass__` method
    and will not allow to initialize project without fix.

    Class variables:

    Some class variables are mandatory for all nested subclasses.

    :cvar str _URL:
    :cvar OneResult _RESULT_CLASS:
    :cvar str _KEY:
    :cvar bool _KEY_MANDATORY:
    :cvar str _METHOD:
    :cvar str _PROVIDER:
    :cvar float _TIMEOUT:

    Instance variables:
    """

    _URL = None
    _RESULT_CLASS = None
    _KEY = None
    _KEY_MANDATORY = True
    _METHOD = None
    _PROVIDER = None
    _TIMEOUT = 5.0

    @staticmethod
    def _is_valid_url(url) -> bool:
        """Validate that URL contains a valid protocol and a valid domain"""
        try:
            parsed = urlparse(url)
            mandatory_parts = [parsed.scheme, parsed.netloc]
            return all(mandatory_parts)
        except AttributeError:
            return False

    @classmethod
    def _is_valid_result_class(cls) -> bool:
        """Validate cls._RESULT_CLASS has correct subclass nesting"""
        try:
            return issubclass(cls._RESULT_CLASS, OneResult)
        except TypeError:
            # TypeError raised by issubclass if cls._RESULT_CLASS is None
            return False

    @classmethod
    def _get_api_key(cls, key=None) -> Optional[str]:
        # Retrieves API Key from method argument first, then from Environment variables
        key = key or cls._KEY

        # raise exception if not valid key found
        if not key and cls._KEY_MANDATORY:
            raise ValueError("Provide API Key")

        return key

    def __init_subclass__(cls, **kwargs):
        """Responsible for setup check for :class:`MultipleResultsQuery` subclasses."""
        super().__init_subclass__(**kwargs)

        # check validity of class._URL
        if not cls._is_valid_url(cls._URL):
            raise ValueError(f"Subclass must define a valid URL. Got {cls._URL}")

        # check validity of cls._RESULT_CLASS
        if not cls._is_valid_result_class():
            raise ValueError(
                f"Subclass must define _RESULT_CLASS from 'OneResult'. "
                f"Got {cls._RESULT_CLASS}",
            )

        # check validity of cls._METHOD
        if not cls._METHOD or cls._METHOD not in [
            "id",
            "geocode",
            "details",
            "reverse",
            "timezone",
            "elevation",
            "places",
            "batch",
            "batch_reverse",
            "children",
            "hierarchy",
            "parcel",
        ]:
            raise ValueError(
                f"Subclass must define correct _METHOD attribute, not equal to None. "
                f"Got {cls._METHOD}"
            )

    def __init__(self, location, **kwargs):
        super(MultipleResultsQuery, self).__init__()
        self._list = []

        # override with kwargs IF given AND not empty string
        self.url = kwargs.get("url", self._URL) or self._URL
        # double check url, just in case it has been overwritten by kwargs
        if not self._is_valid_url(self.url):
            raise ValueError("url not valid. Got %s", self.url)

        # check validity of provider key
        provider_key = self._get_api_key(kwargs.pop("key", ""))

        # point to geocode, as a string or coordinates
        self.location = location

        # set attributes to manage query
        self.encoding = kwargs.get("encoding", "utf-8")
        self.timeout = kwargs.get("timeout", self._TIMEOUT)
        self.proxies = kwargs.get("proxies", "")
        self.session = kwargs.get("session", requests.Session())
        # headers can be overwritten in _build_headers
        self.headers = self._build_headers(provider_key, **kwargs).copy()
        self.headers.update(kwargs.get("headers", {}))
        # params can be overwritten in _build_params
        # OrderedDict in order to preserve the order of the url query parameters
        self.params = OrderedDict(self._build_params(location, provider_key, **kwargs))
        self.params.update(kwargs.get("params", {}))

        # results of query (set by __call__ and _connect)
        self.status_code = None
        self.response = None
        self.error = None
        self.is_called = False

        # pointer to result where to delegate calls
        self.current_result = None
        self._before_initialize(location, **kwargs)

    def __getitem__(self, key):
        return self._list[key]

    def __setitem__(self, key, value):
        self._list[key] = value

    def __delitem__(self, key):
        del self._list[key]

    def __len__(self):
        return len(self._list)

    def insert(self, index, value):
        self._list.insert(index, value)

    def add(self, value):
        self._list.append(value)

    def __repr__(self) -> str:
        base_repr = "<[{0}] {1} - {2} {{0}}>".format(
            self.status, self._PROVIDER.title(), self._METHOD.title()
        )
        if len(self) == 0:
            return base_repr.format("[empty]")
        elif len(self) == 1:
            return base_repr.format(repr(self[0]))
        else:
            return base_repr.format(f"#{len(self)} results")

    def _build_headers(self, provider_key, **kwargs) -> dict:
        """Will be overridden according to the targeted web service"""
        return {}

    def _build_params(self, location, provider_key, **kwargs) -> dict:
        """Will be overridden according to the targeted web service"""
        return {}

    def _before_initialize(self, location, **kwargs):
        """Hook for children class to finalize their setup before the query"""
        pass

    def __call__(self):
        """Query remote server and parse results"""
        self.is_called = True

        # query URL and get valid JSON (also stored in self.json)
        json_response = self._connect()

        # catch errors
        has_error = self._catch_errors(json_response) if json_response else True

        # creates instance for results
        if not has_error:
            self._parse_results(json_response)

        return self

    def _connect(self):
        """- Query self.url (validated cls._URL)
        - Analyse response and set status, errors accordingly
        - On success:

             returns the content of the response as a JSON object
             This object will be passed to self._parse_json_response
        """
        self.status_code = "Unknown"

        try:
            # make request and get response
            self.response = response = self.rate_limited_get(
                self.url,
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

        except requests.exceptions.RequestException as err:
            # store real status code and error
            self.error = f"ERROR - {str(err)}"
            logger.error(
                "Status code %s from %s: %s", self.status_code, self.url, self.error
            )
            return False

        # return response within its JSON format
        return json_response

    def rate_limited_get(self, url, **kwargs):
        """By default, simply wraps a session.get request"""
        return self.session.get(url, **kwargs)

    def _adapt_results(self, json_response):
        """Allow children classes to format json_response into an array of objects"""
        return json_response

    def _parse_results(self, json_response):
        """Creates instances of self.one_result (validated cls._RESULT_CLASS)
        from JSON results retrieved by self._connect

        params: array of objects (dictionaries)
        """
        for json_dict in self._adapt_results(json_response):
            self.add(self._RESULT_CLASS(json_dict))

        # set default result to use for delegation
        self.current_result = len(self) > 0 and self[0]

    def _catch_errors(self, json_response):
        """Checks the JSON returned from the provider and flag errors if necessary"""
        return self.error

    @property
    def ok(self) -> bool:
        return len(self) > 0

    @property
    def status(self) -> str:
        if self.ok:
            return "OK"
        elif self.error:
            return self.error
        elif len(self) == 0:
            return "ERROR - No results found"
        else:
            return "ERROR - Unhandled Exception"

    @property
    def geojson(self) -> dict:
        geojson_results = [result.geojson for result in self]
        return {"type": "FeatureCollection", "features": geojson_results}

    def debug(self) -> list:
        logger.debug("===")
        logger.debug(repr(self))
        logger.debug("===")
        logger.debug(f"#res: {len(self)}")
        logger.debug(f"code: {self.status_code}")
        logger.debug(f"url:  {self.url}")

        stats = []

        if self.ok:
            for index, result in enumerate(self):
                logger.debug(f"Details for result #{index + 1}")
                logger.debug("---")
                stats.append(result.debug())
        else:
            logger.debug(self.status)

        return stats

    # Delegation to current result
    def set_default_result(self, index):
        """change the result used to delegate the calls to. The provided index should
        be in the range of results, otherwise it will raise an exception
        """
        self.current_result = self[index]

    def __getattr__(self, name: str):
        """Allow direct access to :attr:`MultipleResultsQuery.current_result`
        attributes from direct calling of :class:`MultipleResultsQuery`

        Called when an attribute lookup has not found the attribute in the usual
        places (i.e. it is not an instance attribute nor is it found in the class tree
        for self).

        Note that if the attribute is found through the normal mechanism,
        :func:`__getattr__` is not called.

        :param name: Attribute name for lookup
        :raises AttributeError: If provider query was not made and
            :attr:`current_result` is still empty.
        """
        if not self.ok:
            return None

        if self.current_result is None:
            raise AttributeError(
                f"{name} not found on {self.__class__.__name__}, and current_result "
                f"is None"
            )
        return getattr(self.current_result, name)
