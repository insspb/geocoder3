"""
Base classes of provider definition responsible for minimum set of methods and
properties, that should be implemented or overridden in all nested providers.
"""
import json
import logging
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from collections.abc import MutableSequence
from typing import List, MutableMapping, Optional, Tuple, Union
from urllib.parse import urlparse

import requests

from geocoder.distance import Distance

logger = logging.getLogger(__name__)


class OneResult(metaclass=ABCMeta):
    """Container for one (JSON) object returned by provider

    **Class variables:**

    :cvar cls._TO_EXCLUDE: List of properties and attributes to exclude in
        :func:`OneResult._parse_json_with_fieldnames`
    :cvar bool cls._GEOCODER3_READY: Temporary value, representing is provider tested
        and finished migration to geocoder3. On default value will bypass some internal
        checks.

    **Instance variables:**

    After creation each instance of :class:`OneResult` has the following mandatory
    variables. For some providers this list can be extended by provider implementation.

    :ivar self.object_raw_json: Raw json for object, passed by
        :func:`MultipleResultsQuery._parse_results`
    :ivar self.object_json: Result of :func:`OneResult._parse_json_with_fieldnames`
    :ivar self.fieldnames: Fieldnames list generated in
        :func:`OneResult._parse_json_with_fieldnames`

    **Init parameters:**

    For initialization parameters, please check :func:`OneResult.__init__`
    method documentation.
    """

    _GEOCODER3_READY = False
    _TO_EXCLUDE = [
        "parse",
        "object_raw_json",
        "object_json",
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
        """Initialize :class:`OneResult` object and parse input json

        :param dict json_content: Dictionary, passed by
            :func:`MultipleResultsQuery.__call__`
        """
        self.object_raw_json = json_content
        # attributes returned in JSON format
        self.fieldnames = []
        self.object_json = {}
        self._parse_json_with_fieldnames()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls.lat, "__isabstractmethod__", False):
            raise NotImplementedError("All subclasses should implement 'lat' property")
        if getattr(cls.lng, "__isabstractmethod__", False):
            raise NotImplementedError("All subclasses should implement 'lng' property")
        if getattr(cls.address, "__isabstractmethod__", False):
            raise NotImplementedError(
                "All subclasses should implement 'address' property"
            )

    @property
    @abstractmethod
    def lat(self) -> Optional[float]:
        """Latitude of the object"""
        return None

    @property
    @abstractmethod
    def lng(self) -> Optional[float]:
        """Longitude of the object"""
        return None

    @property
    def west(self) -> Optional[float]:
        """Return optional west coordinate of bbox, if available."""
        return self.bbox[0] if self.bbox else None

    @property
    def south(self) -> Optional[float]:
        """Return optional south coordinate of bbox, if available."""
        return self.bbox[1] if self.bbox else None

    @property
    def east(self) -> Optional[float]:
        """Return optional east coordinate of bbox, if available."""
        return self.bbox[2] if self.bbox else None

    @property
    def north(self) -> Optional[float]:
        """Return optional north coordinate of bbox, if available."""
        return self.bbox[3] if self.bbox else None

    @property
    def northeast(self) -> List[float]:
        """Return north-east list of coordinates for bounds, if available."""
        return [self.north, self.east] if self.bbox else []

    @property
    def southwest(self) -> List[float]:
        """Return south-west list of coordinates for bounds, if available."""
        return [self.south, self.west] if self.bbox else []

    @property
    def bbox(self) -> List[float]:
        """Output answer as GeoJSON bbox if it can be calculated/retrieved."""
        return []

    @property
    def bounds(self) -> dict:
        """Output answer as Google Maps API bounds if it can be calculated/retrieved."""
        return (
            {"northeast": self.northeast, "southwest": self.southwest}
            if self.northeast and self.southwest
            else {}
        )

    @property
    @abstractmethod
    def address(self) -> Optional[str]:
        """Object simple string address."""
        return None

    def __repr__(self) -> str:
        """Display [address] if available; [lat, lng] otherwise"""
        return f"[{self.address}]" if self.address else f"[{self.lat}, {self.lng}]"

    def _parse_json_with_fieldnames(self):
        """Parse the instance object with all attributes/methods defined in the class,
        except for the ones defined starting with '_' or flagged in
        :attr:`cls._TO_EXCLUDE`.

        The final result is stored in :attr:`self.object_json` and
        :attr:`self.fieldnames`
        """
        for key in dir(self):
            if not key.startswith("_") and key not in self._TO_EXCLUDE:
                self.fieldnames.append(key)
                value = getattr(self, key)
                if value:
                    self.object_json[key] = value
        # Add OK attribute even if value is "False"
        self.object_json["ok"] = self.ok

    @property
    def ok(self) -> bool:
        """Status of retrieving location/IP coordinates or reverse geocoding.

        Usually should be replaced in reverse results class.
        """
        return bool(self.lng and self.lat)

    @property
    def status(self) -> str:
        """Specify current summary status of instance"""
        if self.ok:
            return "OK"
        if not self.address:
            return "ERROR - No results found"
        return "ERROR - No Geometry"

    def debug(self):
        """Display debug information for instance of :class:`OneResult`"""
        logger.debug("From provider")
        logger.debug("-------------")
        logger.debug(json.dumps(self.object_raw_json, indent=4))
        logger.debug("Cleaned json")
        logger.debug("------------")
        logger.debug(json.dumps(self.object_json, indent=4))

    def _get_bbox(self, south, west, north, east) -> dict:
        """Wrapper for bbox data generation"""
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
        """Is as a measure of how confident we are that centre point coordinates
        returned for the result precisely reflect the result.
        """
        if not self.bounds:
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
        """Output answer as GeoJSON Point"""
        return {"type": "Point", "coordinates": [self.x, self.y]} if self.ok else {}

    @property
    def geojson(self) -> dict:
        """Output answer as GeoJSON Feature"""
        feature = {
            "type": "Feature",
            "properties": self.object_json,
        }
        if self.bbox:
            feature["bbox"] = self.bbox
            feature["properties"]["bbox"] = self.bbox
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
    """Base results and query manager container

    This class responsible for checking correct new provider files creation before it
    will be implemented in project. Such checks done in :func:`__init_subclass__` method
    and will not allow to initialize project without fix.

    **Class variables:**

    Some class variables are mandatory for all nested subclasses.

    :cvar str cls._URL: Default URL for provider, can be overwritten with `url` input
        parameter
    :cvar OneResult cls._RESULT_CLASS: Provider's individual result class.
    :cvar str cls._KEY: Provider's default api_key. Usually map to ENV variable
        responsible for key parsing. Can be overwritten with **key** parameter on
        instance creation. Shows actually used key when requested from instance.
    :cvar bool cls._KEY_MANDATORY: Special mark for check of mandatory presence of api
        key, for providers with mandatory key requirement
    :cvar str cls._METHOD: Provider's internal method, that should match with api.py
        :attr:`options` definition.
    :cvar str cls._PROVIDER: Provider's internal name, that should match with api.py
        :attr:`options` definition.
    :cvar float cls._TIMEOUT: Default timeout for :func:`requests.request`
        configuration, can be overwritten on instance creation or instance calling
    :cvar bool cls._GEOCODER3_READY: Temporary value, representing is provider tested
        and finished migration to geocoder3. On default value will generate warning on
        any provider call.

    **Instance variables:**

    After creation each instance of :class:`MultipleResultsQuery` has the following
    mandatory variables. For some providers this list can be extended by provider
    implementation.

    :ivar list[OneResult] self.results_list: Hold all answers from provider in parsed
        state
    :ivar str self.url: Final request url that will be/was used during request
    :ivar str self.location: Object to geocode/reverse geocode
    :ivar float self.timeout: Final request timeout that was used during request
    :ivar Optional[dict] self.proxies: Final request proxies that was used during
        request
    :ivar requests.Session self.session: :class:`requests.Session` object, that was used
    :ivar dict self.headers: Final request headers that was used during request
    :ivar dict self.params: Final request query params that was used during request
    :ivar Optional[int] self.status_code: :class:`requests.Response` final HTTP answer
        code or `None` if request is not made yet, or :mod:`requests` failed during
        request
    :ivar requests.Response self.raw_response: Contain raw :class:`requests.Response`
        from provider
    :ivar Union[dict, list] self.raw_json: Contain raw :func:`requests.Response.json`
        from provider
    :ivar str self.error: :mod:`requests` detailed error, if was raised during request
    :ivar bool self.is_called: `False` on instance initialization, become `True` after
        calling of :func:`__call__` method(i.e. instance call)
    :ivar OneResult self.current_result: Mapping to result, that are used for direct
        attributes retrieval in :func:`__getattr__`

    **Init parameters:**

    For initialization parameters, please check :func:`MultipleResultsQuery.__init__`
    method documentation.
    """

    _URL = None
    _RESULT_CLASS = None
    _KEY = None
    _KEY_MANDATORY = True
    _METHOD = None
    _PROVIDER = None
    _TIMEOUT = 5.0
    _GEOCODER3_READY = False

    @staticmethod
    def _is_valid_url(url: Optional[str]) -> bool:
        """Validate that URL contains a valid protocol and a valid domain

        :param Optional[str] url: Any string to be checked for format validity.
            Does not check for endpoint existence.
        """
        try:
            parsed = urlparse(url)
            mandatory_parts = [parsed.scheme in ["http", "https"], parsed.netloc]
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
    def _get_api_key(cls, key: Optional[str] = None) -> Optional[str]:
        """Retrieves API Key from method argument first, then from Environment variables

        :param Optional[str] key: Custom API Key data for provider usage, if required.
            Passed from :func:`__init__` method.
        :raises ValueError: If api key was not provided, but mandatory for provider use
        """
        key = key or cls._KEY

        if not key and cls._KEY_MANDATORY:
            raise ValueError("Provide API Key")

        return key

    def __init_subclass__(cls, **kwargs):
        """Responsible for setup check for :class:`MultipleResultsQuery` subclasses.

        :raises ValueError: When subclass not define :attr:`cls._URL` value.
        :raises ValueError: When subclass incorrectly define :attr:`cls._RESULT_CLASS`
            value.
        :raises ValueError: When subclass incorrectly define :attr:`cls._METHOD` value.
        """
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

    def __init__(
        self,
        location,
        url: Optional[str] = None,
        key: Optional[str] = None,
        timeout: Union[None, float, Tuple[float, float], Tuple[float, None]] = None,
        proxies: Optional[MutableMapping[str, str]] = None,
        session: Optional[requests.Session] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        params: Optional[dict] = None,
        **kwargs,
    ):
        """Initialize a :class:`MultipleResultsQuery` object.

        For class and instance variables description please refer to class docstrings.

        :param location: Query content for geocode or reverse geocoding
        :param Optional[str] url: Overwrite for default provider service url
        :param Optional[str] key: API Key data for provider usage, if required. Passed
            to :func:`_get_api_key`, which result passed to :func:`_build_headers` and
            :func:`_build_params`, and may be passed to other custom provider's
            implementation methods. Check exact provider docs.
        :param Union[None, float, Tuple[float, float], Tuple[float, None]] timeout:
            Max request answer wait time
        :param Optional[MutableMapping[str, str]] proxies:
            Proxies for :func:`requests.request`
        :param Optional[requests.Session] session: Custom :class:`requests.Session` for
            request
        :param Optional[MutableMapping[str, str]] headers: Additional headers for
            :func:`requests.request`
        :param Optional[dict] params: Additional query parameters
        :param kwargs: Any other keyword arguments, that will be passed to internal
            :func:`_build_headers`, :func:`_build_params`, :func:`_before_initialize` or
            other custom provider's implementation methods. Check exact provider docs

        :raises ValueError: When provided custom :attr:`url` is not well-formatted
        :raises ValueError: If api key was not provided, but mandatory for provider use
        """
        super(MultipleResultsQuery, self).__init__()
        self.results_list = []

        # Check url if it was changed on instance creation
        if url and not self._is_valid_url(url):
            raise ValueError(f"url not valid. Got {url}")
        self.url = url or self._URL

        # check validity of provider key
        provider_key = self._KEY = self._get_api_key(key=key)

        # point to geocode, as a string or coordinates
        self.location = location

        # set attributes to manage query. Can be overwritten in __call__
        self.timeout = timeout or self._TIMEOUT
        self.proxies = proxies
        self.session = session

        # headers can be overwritten in _build_headers,
        # headers can be extended with headers keyword argument
        self.headers = self._build_headers(provider_key, **kwargs).copy()
        self.headers.update(headers or {})
        # params can be overwritten in _build_params
        # params can be extended with params keyword argument
        # OrderedDict in order to preserve the order of the url query parameters
        self.params = OrderedDict(self._build_params(location, provider_key, **kwargs))
        self.params.update(params or {})

        # results of query (set by __call__ and _connect)
        self.status_code = None
        self.raw_response = None
        self.raw_json = None
        self.error = None
        self.is_called = False

        # pointer to result where to delegate calls
        self.current_result = None
        self._before_initialize(location, **kwargs)

    def __getitem__(self, key):
        """Special method implementation for custom :class:`MutableSequence` subclass

        Not expected to be nested or changed in subclasses.
        """
        return self.results_list[key]

    def __setitem__(self, key, value):
        """Special method implementation for custom :class:`MutableSequence` subclass

        Not expected to be nested or changed in subclasses.
        """
        self.results_list[key] = value

    def __delitem__(self, key):
        """Special method implementation for custom :class:`MutableSequence` subclass

        Not expected to be nested or changed in subclasses.
        """
        del self.results_list[key]

    def __len__(self):
        """Special method implementation for custom :class:`MutableSequence` subclass

        Not expected to be nested or changed in subclasses.
        """
        return len(self.results_list)

    def insert(self, index, value):
        """Special method implementation for custom :class:`MutableSequence` subclass

        Not expected to be nested or changed in subclasses.
        """
        self.results_list.insert(index, value)

    def add(self, value):
        """Special method implementation for custom :class:`MutableSequence` subclass

        Not expected to be nested or changed in subclasses.
        """
        self.results_list.append(value)

    def __repr__(self) -> str:
        """Display :class:`MultipleResultsQuery` debug console representation"""
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
        """Generate default query headers for provider

        :param provider_key: Finalized api_key, from :func:`_get_api_key` method
        :param kwargs: All kwargs from :func:`__init__` method
        """
        return {}

    def _build_params(self, location, provider_key, **kwargs) -> dict:
        """Generate default query parameters mapping for provider

        :param location: Query content for geocode or reverse geocoding
        :param provider_key: Finalized api_key, from :func:`_get_api_key` method
        :param kwargs: All kwargs from :func:`__init__` method
        """
        return {}

    def _before_initialize(self, location, **kwargs):
        """Hook for children class to finalize their setup before the query

        :param location: Query content for geocode or reverse geocoding
        :param kwargs: All kwargs from :func:`__init__` method
        """
        pass

    def __call__(
        self,
        timeout: Union[None, float, Tuple[float, float], Tuple[float, None]] = None,
        proxies: Optional[MutableMapping[str, str]] = None,
        session: Optional[requests.Session] = None,
    ):
        """Query remote server and parse results

        Any keyword argument of :func:`__call__` will have precedence over same argument
        in :func:`__init__` method.

        :param Union[None, float, Tuple[float, float], Tuple[float, None]] timeout:
            Max request answer wait time
        :param Optional[MutableMapping[str, str]] proxies:
            Proxies for :func:`requests.request`
        :param Optional[requests.Session] session: Custom :class:`requests.Session` for
            request
        """
        self.is_called = True
        if self._GEOCODER3_READY is False:
            logger.warning(
                "This provider behaviour not tested in geocoder3, results may be "
                "incorrect, or not all features available."
            )
        # Allow in call overwrite of connection settings
        self.timeout = timeout or self.timeout
        self.proxies = proxies or self.proxies
        self.session = session or self.session or requests.Session()

        # query URL and get valid JSON (also stored in self.raw_json)
        json_response = self._connect()

        # catch errors and debug warnings
        has_error = (
            self._catch_errors(json_response) if json_response is not None else True
        )
        if self.url not in self.raw_response.url:
            logger.warning(
                "Expected request url (%s) and final request url (%s) do not match. "
                "Probably redirects was made.",
                self.url,
                self.raw_response.url,
            )

        # creates instance for results
        if not has_error:
            self._parse_results(json_response)

        return self

    def _connect(self) -> Union[list, dict, None]:
        """Responsible for handling external request and connection errors"""
        try:
            # make request and get response
            self.raw_response = self.rate_limited_get(
                self.url,
                params=self.params,
                headers=self.headers,
                timeout=self.timeout,
                proxies=self.proxies,
            )
            logger.info("Requested %s", self.raw_response.url)

            # check that response is ok
            self.status_code = self.raw_response.status_code
            self.raw_response.raise_for_status()

            # rely on json method to get non-empty well formatted JSON
            self.raw_json = self.raw_response.json()
        except requests.exceptions.RequestException as err:
            # store real status code and error
            self.error = f"ERROR - {str(err)}"
            logger.error(
                "Status code %s from %s: %s", self.status_code, self.url, self.error
            )
            return None

        # return response within its JSON format
        return self.raw_json

    def rate_limited_get(self, url, **kwargs):
        """By default, simply wraps a :func:`requests.get` request"""
        return self.session.get(url, **kwargs)

    def _adapt_results(self, json_response) -> Union[dict, List[dict]]:
        """Allow children classes to format json_response into
        :func:`_parse_results` expected format

        This required for correct iteration in :func:`_parse_results`

        :param json_response: Raw json from provider, usually same as in
            :attr:`raw_json`, by default invoked inside :func:`_parse_results`
        """
        return json_response

    def _parse_results(self, json_response: Union[dict, List[dict]]):
        """Responsible for parsing original json and separating it to
        :class:`OneResult` objects
        """
        for json_dict in self._adapt_results(json_response):
            self.add(self._RESULT_CLASS(json_dict))

        # set default result to use for delegation
        self.current_result = len(self) > 0 and self[0]

    def _catch_errors(self, json_response):
        """Checks the JSON returned from the provider and flag errors if necessary"""
        return self.error

    @property
    def has_data(self) -> bool:
        """Status of geocoding if request was made

        :raises RuntimeError: When external request was not made before property call
        """
        if not self.is_called:
            raise RuntimeError(
                "Cannot detect data presence. External request was not made. "
                "Use instance __call__() method to retrieve data."
            )
        return len(self) > 0

    @property
    def status(self) -> str:
        """Specify current summary status of instance

        **Possible statuses:**

        - "External request was not made"
        - "OK" - when request was made, and any result retrieved
        - :mod:`requests` error text representation, if request faced error
        - "ERROR - No results found"
        - "ERROR - Unhandled Exception"
        """
        if not self.is_called:
            return "External request was not made"
        elif self.has_data:
            return "OK"
        elif self.error:
            return self.error
        elif len(self) == 0:
            return "ERROR - No results found"
        else:
            return "ERROR - Unhandled Exception"

    @property
    def geojson(self) -> dict:
        """Output all answers as GeoJSON FeatureCollection"""
        geojson_results = [result.geojson for result in self]
        return {"type": "FeatureCollection", "features": geojson_results}

    def debug(self) -> list:
        """Display debug information for instance of :class:`MultipleResultsQuery`"""
        logger.debug(repr(self))
        logger.debug(f"results: {len(self)}")
        logger.debug(f"code: {self.status_code}")
        logger.debug(f"url:  {self.url}")

        stats = []

        if self.is_called and self.has_data:
            for index, result in enumerate(self):
                logger.debug(f"Details for result #{index + 1}")
                logger.debug("---")
                stats.append(result.debug())
        else:
            logger.debug(self.status)

        return stats

    def __getattr__(self, name: str):  # sourcery skip: swap-if-expression
        """Allow direct access to :attr:`MultipleResultsQuery.current_result`
        attributes from direct calling of :class:`MultipleResultsQuery`

        Called when an attribute lookup has not found the attribute in the usual
        places (i.e. it is not an instance attribute nor is it found in the class tree
        for self).

        .. note:: If the attribute is found through the normal mechanism,
            :func:`__getattr__` is not called.

        :param name: Attribute name for lookup
        :raises RuntimeError: If provider query was not made and
            :attr:`current_result` is still empty. (From :func:`has_data`)
        """
        return None if not self.has_data else getattr(self.current_result, name)
