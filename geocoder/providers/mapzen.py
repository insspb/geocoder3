__all__ = ["MapzenResult", "MapzenQuery", "MapzenReverseResult", "MapzenReverse"]
from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import mapzen_key
from geocoder.location import Location


class MapzenResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._geometry = json_content.get("geometry", {})
        self._properties = json_content.get("properties", {})

        # proceed with super.__init__
        super(MapzenResult, self).__init__(json_content)

    @property
    def lat(self):
        return self._geometry["coordinates"][1]

    @property
    def lng(self):
        return self._geometry["coordinates"][0]

    @property
    def address(self):
        return self._properties.get("label")

    @property
    def house_number(self):
        return self._properties.get("housenumber")

    @property
    def street(self):
        return self._properties.get("street")

    @property
    def neighbourhood(self):
        return self._properties.get("neighbourhood")

    @property
    def city(self):
        return self._properties.get("locality")

    @property
    def state(self):
        return self._properties.get("region")

    @property
    def country(self):
        return self._properties.get("country")

    @property
    def postal(self):
        return self._properties.get("postalcode")

    @property
    def gid(self):
        return self._properties.get("gid")

    @property
    def id(self):
        return self._properties.get("id")


class MapzenQuery(MultipleResultsQuery):
    """
    Mapzen REST API

    API Reference: https://mapzen.com/documentation/search/search/
    """

    _PROVIDER = "mapzen"
    _METHOD = "geocode"
    _URL = "https://search.mapzen.com/v1/search"
    _RESULT_CLASS = MapzenResult
    _KEY = mapzen_key

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "text": location,
            "api_key": provider_key,
            "size": max_results,
        }

    def _adapt_results(self, json_response):
        return json_response["features"]


class MapzenReverseResult(MapzenResult):
    @property
    def ok(self):
        return bool(self.address)


class MapzenReverse(MapzenQuery):
    """
    Mapzen REST API

    API Reference: https://mapzen.com/documentation/search/reverse/
    """

    _PROVIDER = "mapzen"
    _METHOD = "reverse"
    _URL = "https://search.mapzen.com/v1/reverse"
    _RESULT_CLASS = MapzenReverseResult

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        location = Location(location)
        return {
            "point.lat": location.lat,
            "point.lon": location.lng,
            "size": max_results,
            "layers": kwargs.get("layers"),
            "source": kwargs.get("sources"),
            "boundary.country": kwargs.get("country"),
            "api_key": provider_key,
        }
