__all__ = [
    "GoogleResult",
    "GoogleQuery",
    "GoogleElevationResult",
    "GoogleElevationQuery",
    "GooglePlacesResult",
    "GooglePlacesQuery",
    "GoogleReverseResult",
    "GoogleReverse",
    "GoogleTimezoneResult",
    "GoogleTimezone",
]
import base64
import hashlib
import hmac
import time
from collections import OrderedDict
from typing import List, Optional
from urllib.parse import urlencode, urlparse

import ratelim

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import google_client, google_client_secret, google_key
from geocoder.location import BBox, Location


class GoogleResult(OneResult):
    def __init__(self, json_content):
        # flatten geometry
        geometry = json_content.get("geometry", {})
        self._location = geometry.get("location", {})
        self._location_type = geometry.get("location_type", {})
        self._viewport = geometry.get("viewport", {})

        # Parse address components with short & long names
        for item in json_content["address_components"]:
            for category in item["types"]:
                json_content.setdefault(category, {})
                json_content[category]["long_name"] = item["long_name"]
                json_content[category]["short_name"] = item["short_name"]

        # proceed with super.__init__
        super(GoogleResult, self).__init__(json_content)

    @property
    def lat(self):
        return self._location.get("lat")

    @property
    def lng(self):
        return self._location.get("lng")

    @property
    def place(self):
        return self.object_raw_json.get("place_id")

    @property
    def quality(self):
        quality = self.object_raw_json.get("types")
        if quality:
            return quality[0]

    @property
    def accuracy(self):
        return self._location_type

    @property
    def bbox(self) -> List[float]:
        """Output answer as GeoJSON bbox if it can be calculated/retrieved."""
        south = self._viewport.get("southwest", {}).get("lat")
        west = self._viewport.get("southwest", {}).get("lng")
        north = self._viewport.get("northeast", {}).get("lat")
        east = self._viewport.get("northeast", {}).get("lng")
        return (
            [float(west), float(south), float(east), float(north)]
            if all([west, south, east, north])
            else []
        )

    @property
    def address(self):
        return self.object_raw_json.get("formatted_address")

    @property
    def postal(self):
        return self.object_raw_json.get("postal_code", {}).get("short_name")

    @property
    def subpremise(self):
        return self.object_raw_json.get("subpremise", {}).get("short_name")

    @property
    def house_number(self):
        return self.object_raw_json.get("street_number", {}).get("short_name")

    @property
    def street(self):
        return self.object_raw_json.get("route", {}).get("short_name")

    @property
    def street_long(self):
        return self.object_raw_json.get("route", {}).get("long_name")

    @property
    def road_long(self):
        return self.street_long

    @property
    def neighborhood(self):
        return self.object_raw_json.get("neighborhood", {}).get("short_name")

    @property
    def sublocality(self):
        return self.object_raw_json.get("sublocality", {}).get("short_name")

    @property
    def city(self):
        return (
            self.object_raw_json.get("locality", {}).get("short_name")
            or self.postal_town
        )

    @property
    def city_long(self):
        return (
            self.object_raw_json.get("locality", {}).get("long_name")
            or self.postal_town_long
        )

    @property
    def postal_town(self):
        return self.object_raw_json.get("postal_town", {}).get("short_name")

    @property
    def postal_town_long(self):
        return self.object_raw_json.get("postal_town", {}).get("long_name")

    @property
    def county(self):
        return self.object_raw_json.get("administrative_area_level_2", {}).get(
            "short_name"
        )

    @property
    def state(self):
        return self.object_raw_json.get("administrative_area_level_1", {}).get(
            "short_name"
        )

    @property
    def state_long(self):
        return self.object_raw_json.get("administrative_area_level_1", {}).get(
            "long_name"
        )

    @property
    def province_long(self):
        return self.state_long

    @property
    def country(self):
        return self.object_raw_json.get("country", {}).get("short_name")

    @property
    def country_long(self):
        return self.object_raw_json.get("country", {}).get("long_name")


class GoogleQuery(MultipleResultsQuery):
    """
    Google Geocoding API

    Geocoding is the process of converting addresses into geographic
    coordinates (like latitude 37.423021 and longitude -122.083739),
    which you can use to place markers or position the map.

    API Reference: https://developers.google.com/maps/documentation/geocoding

    For ambiguous queries or 'nearby' type queries, use the Places Text Search instead.
    https://developers.google.com/maps/documentation/geocoding/best-practices#automated-system
    """

    _PROVIDER = "google"
    _METHOD = "geocode"
    _URL = "https://maps.googleapis.com/maps/api/geocode/json"
    _RESULT_CLASS = GoogleResult
    _KEY = google_key
    _KEY_MANDATORY = True

    def _build_params(self, location, provider_key, **kwargs):
        params = self._location_init(location, **kwargs)
        params["language"] = kwargs.get("language", "")
        self.rate_limit = kwargs.get("rate_limit", True)

        # adapt params to authentication method
        # either with client / secret
        self.client = kwargs.get("client", google_client)
        self.client_secret = kwargs.get("client_secret", google_client_secret)

        if self.client and self.client_secret:
            params["client"] = self.client
            return self._encode_params(params)
        # or API key
        else:
            # provider_key is computed in base.py:
            # either cls._KEY (google_key) or kwargs['key'] if provided
            params["key"] = provider_key
            return params

    def _location_init(self, location, **kwargs):
        return {
            "address": location,
            "bounds": kwargs.get("bounds", ""),
            "components": kwargs.get("components", ""),
            "region": kwargs.get("region", ""),
        }

    def _encode_params(self, params):
        # turn non-empty params into sorted list in order to maintain signature validity
        # Requests will honor the order.
        ordered_params = sorted([(k, v) for (k, v) in params.items() if v])
        params = OrderedDict(ordered_params)

        # the signature parameter needs to come in the end of the url
        params["signature"] = self._sign_url(
            self.url, ordered_params, self.client_secret
        )

        return params

    def _sign_url(self, base_url=None, params=None, client_secret=None):
        """Sign a request URL with a Crypto Key.
        Usage:
        from urlsigner import sign_url
        signed_url = sign_url(base_url=my_url,
                              params=url_params,
                              client_secret=CLIENT_SECRET)
        Args:
        base_url - The trunk of the URL to sign. E.g.
                https://maps.googleapis.com/maps/api/geocode/json
        params - List of tuples of URL parameters INCLUDING YOUR CLIENT ID
        ('client','gme-...')
        client_secret - Your Crypto Key from Google for Work
        Returns:
        The signature as a dictionary #signed request URL
        """
        # Return if any parameters aren't given
        if not base_url or not self.client_secret or not self.client:
            return None

        # assuming parameters will be submitted to Requests in identical order!
        url = urlparse(f"{base_url}?{urlencode(params)}")

        # We only need to sign the path+query part of the string
        url_to_sign = f"{url.path}?{url.query}".encode("utf-8")

        # Decode the private key into its binary format
        # We need to decode the URL-encoded private key
        decoded_key = base64.urlsafe_b64decode(client_secret)

        # Create a signature using the private key and the URL-encoded
        # string using HMAC SHA1. This signature will be binary.
        signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)

        return base64.urlsafe_b64encode(signature.digest())

    def rate_limited_get(self, *args, **kwargs):
        if not self.rate_limit:
            return super(GoogleQuery, self).rate_limited_get(*args, **kwargs)
        elif self.client and self.client_secret:
            return self.rate_limited_get_for_work(*args, **kwargs)
        else:
            return self.rate_limited_get_for_dev(*args, **kwargs)

    @ratelim.greedy(2500, 60 * 60 * 24)
    @ratelim.greedy(10, 1)
    def rate_limited_get_for_dev(self, *args, **kwargs):
        return super(GoogleQuery, self).rate_limited_get(*args, **kwargs)

    @ratelim.greedy(100000, 60 * 60 * 24)  # Google for Work daily limit
    @ratelim.greedy(50, 1)  # Google for Work limit per second
    def rate_limited_get_for_work(self, *args, **kwargs):
        return super(GoogleQuery, self).rate_limited_get(*args, **kwargs)

    def _catch_errors(self, json_response):
        status = json_response.get("status")
        if status != "OK":
            self.error = status

        return self.error

    def _adapt_results(self, json_response):
        return json_response.get("results", [])


class GoogleElevationResult(OneResult):
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
    def address(self) -> Optional[str]:
        """Object simple string address.

        TODO: Implement during geocode3 migration.
        """
        raise NotImplementedError(
            f"Provider {self.__class__.__name__} does not support address property."
        )

    @property
    def status(self):
        return "OK" if self.elevation else "ERROR - No Elevation found"

    @property
    def ok(self):
        return bool(self.elevation)

    @property
    def meters(self):
        if self.elevation:
            return round(self.elevation, 1)

    @property
    def feet(self):
        if self.elevation:
            return round(self.elevation * 3.28084, 1)

    @property
    def elevation(self):
        return self.object_raw_json.get("elevation")

    @property
    def resolution(self):
        return self.object_raw_json.get("resolution")


class GoogleElevationQuery(MultipleResultsQuery):
    """
    Google Elevation API

    The Elevation API provides elevation data for all locations on the surface of the
    earth, including depth locations on the ocean floor (which return negative values).
    In those cases where Google does not possess exact elevation measurements at the
    precise location you request, the service will interpolate and return an averaged
    value using the four nearest locations.

    API Reference: https://developers.google.com/maps/documentation/elevation/
    """

    _PROVIDER = "google"
    _METHOD = "elevation"
    _URL = "https://maps.googleapis.com/maps/api/elevation/json"
    _RESULT_CLASS = GoogleElevationResult
    _KEY = google_key

    def _build_params(self, location, provider_key, **kwargs):
        return {
            # required
            "key": provider_key,
            "locations": str(Location(location)),
        }

    def _adapt_results(self, json_response):
        return json_response["results"]


class GooglePlacesResult(OneResult):
    def __init__(self, json_content):
        # flatten geometry
        geometry = json_content.get("geometry", {})
        self._location = geometry.get("location", {})
        json_content["northeast"] = geometry.get("viewport", {}).get("northeast", {})
        json_content["southwest"] = geometry.get("viewport", {}).get("southwest", {})

        # proceed with super.__init__
        super(GooglePlacesResult, self).__init__(json_content)

    @property
    def lat(self):
        return self._location.get("lat")

    @property
    def lng(self):
        return self._location.get("lng")

    @property
    def id(self):
        return self.object_raw_json.get("id")

    @property
    def reference(self):
        return self.object_raw_json.get("reference")

    @property
    def place_id(self):
        return self.object_raw_json.get("place_id")

    @property
    def type(self):
        type = self.object_raw_json.get("types")
        if type:
            return type[0]

    @property
    def address(self):
        return self.object_raw_json.get("formatted_address")

    @property
    def icon(self):
        return self.object_raw_json.get("icon")

    @property
    def name(self):
        return self.object_raw_json.get("name")

    @property
    def vicinity(self):
        return self.object_raw_json.get("vicinity")

    @property
    def price_level(self):
        return self.object_raw_json.get("price_level")

    @property
    def rating(self):
        return self.object_raw_json.get("rating")


class GooglePlacesQuery(MultipleResultsQuery):
    """
    Google Places API

    The Google Places API Web Service allows you to query for place information on a
    variety of categories, such as: establishments, prominent points of interest,
    geographic locations, and more.

    You can search for places either by proximity or a text string.
    A Place Search returns a list of places along with summary information about each
    place; additional information is available via a Place Details query.

    At this time, only the "Text Search" is supported by this library.  "Text Search"
    can be used when you don't have pristine formatted addresses required by the regular
    Google Maps Geocoding API or when you want to do 'nearby' searches like
    'restaurants near Sydney'.

    The Geocoding best practices reference indicates that when you have 'ambiguous
    queries in an automated system you would be better served using the Places API
    Text Search than the Maps Geocoding API
    https://developers.google.com/maps/documentation/geocoding/best-practices

    API Reference:

    https://developers.google.com/places/web-service/intro
    https://developers.google.com/places/web-service/search

    l = geocoder.google('Elm Plaza Shopping Center, Enfield, CT 06082', method='places')
    l = geocoder.google('food near white house', method='places')
    l = geocoder.google('1st and main', method='places')

    :param location: Your search location or phrase you want geocoded.
    :param key: Your Google developers free key.

    :param proximity: (optional) lat,lng point around which results will be given
                            preference
    :param radius: (optional) in meters, used with proximity
    :param language: (optional) 2-letter code of preferred language of returned address
                            elements.
    :param minprice: (optional) 0 (most affordable) to 4 (most expensive)
    :param maxprice: (optional) 0 (most affordable) to 4 (most expensive)
    :param opennow: (optional) value is ignored. when present, closed places and places
                            without opening hours will be omitted
    :param pagetoken: (optional) get next 20 results from previously run search.
                            when set, other criteria are ignored
    :param type: (optional) restrict results to one type of place

    todo: Paging (pagetoken) is not fully supported since we only return the first
      result. Need to return all results to the user so paging will make sense
    todo: Add support for missing results fields html_attributions, opening_hours,
      photos, scope, alt_ids, types [not just the first one]
    todo: Add support for nearbysearch and radarsearch variations of the Google Places
      API
    """

    _PROVIDER = "google"
    _METHOD = "places"
    _URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    _RESULT_CLASS = GooglePlacesResult
    _KEY = google_key

    def __init__(self, location, **kwargs):
        super(GooglePlacesQuery, self).__init__(location, **kwargs)

        self.next_page_token = None

    def _build_params(self, location, provider_key, **kwargs):
        # handle specific case of proximity (aka 'location' for google)
        bbox = kwargs.get("proximity", "")
        if bbox:
            bbox = BBox.factory(bbox)
            # do not forget to convert bbox to google expectations...
            bbox = bbox.latlng

        # define all
        params = {
            # required
            "query": location,
            "key": provider_key,
            # optional
            "location": bbox,
            "radius": kwargs.get("radius", ""),
            "language": kwargs.get("language", ""),
            "minprice": kwargs.get("minprice", ""),
            "maxprice": kwargs.get("maxprice", ""),
            "type": kwargs.get("type", ""),
        }

        # optional, don't send unless needed
        if "opennow" in kwargs:
            params["opennow"] = ""

        # optional, don't send unless needed
        if "pagetoken" in kwargs:
            params["pagetoken"] = kwargs["pagetoken"]

        return params

    def _parse_results(self, json_response):
        super(GooglePlacesQuery, self)._parse_results(json_response)

        # store page token if any
        self.next_page_token = json_response.get("next_page_token")

    def _adapt_results(self, json_response):
        return json_response["results"]

    @property
    def query(self):
        return self.location


class GoogleReverseResult(GoogleResult):
    @property
    def ok(self):
        return bool(self.address)


class GoogleReverse(GoogleQuery):
    """
    Google Geocoding API

    Geocoding is the process of converting addresses (like "1600 Amphitheatre
    Parkway, Mountain View, CA") into geographic coordinates (like latitude
    37.423021 and longitude -122.083739), which you can use to place markers or
    position the map.

    API Reference: https://developers.google.com/maps/documentation/geocoding/
    """

    _PROVIDER = "google"
    _METHOD = "reverse"

    def _location_init(self, location, **kwargs):
        return {
            "latlng": str(Location(location)),
            "sensor": "false",
        }


class GoogleTimezoneResult(OneResult):
    def __repr__(self):
        return f"<[{self.status}] [{self.timeZoneName}]>"

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
        return bool(self.timeZoneName)

    @property
    def timeZoneId(self):
        return self.object_raw_json.get("timeZoneId")

    @property
    def timeZoneName(self):
        return self.object_raw_json.get("timeZoneName")

    @property
    def rawOffset(self):
        return self.object_raw_json.get("rawOffset")

    @property
    def dstOffset(self):
        return self.object_raw_json.get("dstOffset")


class GoogleTimezone(MultipleResultsQuery):
    """
    Google Time Zone API

    The Time Zone API provides time offset data for locations on the surface of the
    earth.
    Requesting the time zone information for a specific Latitude/Longitude pair will
    return the name of that time zone, the time offset from UTC, and the Daylight
    Savings offset.

    API Reference: https://developers.google.com/maps/documentation/timezone/
    """

    _PROVIDER = "google"
    _METHOD = "timezone"
    _URL = "https://maps.googleapis.com/maps/api/timezone/json"
    _RESULT_CLASS = GoogleTimezoneResult
    _KEY = google_key

    def _build_params(self, location, provider_key, **kwargs):
        return {
            # required
            "key": provider_key,
            "location": str(Location(location)),
            "timestamp": kwargs.get("timestamp", time.time()),
        }

    def _adapt_results(self, json_response):
        return [json_response]
