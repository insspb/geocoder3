__all__ = [
    "OpenCageResult",
    "OpenCageQuery",
    "OpenCageReverseResult",
    "OpenCageReverse",
]
from typing import List

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import opencage_key
from geocoder.location import Location


class OpenCageResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._geometry = json_content.get("geometry", {})
        self._components = json_content.get("components", {})
        self._annotations = json_content.get("annotations", {})
        self._bounds = json_content.get("bounds", {})

        # proceed with super.__init__
        super(OpenCageResult, self).__init__(json_content)

    @property
    def lat(self):
        return self._geometry.get("lat")

    @property
    def lng(self):
        return self._geometry.get("lng")

    @property
    def address(self):
        return self.object_raw_json.get("formatted")

    @property
    def house_number(self):
        return self._components.get("house_number")

    @property
    def house_aliases(self):
        house = self._components.get("house")
        building = self._components.get("building")
        public_building = self._components.get("public_building")
        if house:  # Priority can be rearranged
            return house
        elif building:
            return building
        elif public_building:
            return public_building

    @property
    def house(self):
        house = self._components.get("house")
        return house or self.house_aliases

    @property
    def building(self):
        building = self._components.get("building")
        return building or self.house_aliases

    @property
    def public_building(self):
        public_building = self._components.get("public_building")
        return public_building or self.house_aliases

    @property
    def street_aliases(self):
        street = self._components.get("street")
        road = self._components.get("road")
        footway = self._components.get("footway")
        street_name = self._components.get("street_name")
        residential = self._components.get("residential")
        path = self._components.get("path")
        pedestrian = self._components.get("pedestrian")
        if street:
            return street
        elif road:
            return road
        elif footway:
            return footway
        elif street_name:
            return street_name
        elif residential:
            return residential
        elif path:
            return path
        elif pedestrian:
            return pedestrian

    @property
    def street(self):
        street = self._components.get("street")
        return street or self.street_aliases

    @property
    def footway(self):
        footway = self._components.get("footway")
        return footway or self.street_aliases

    @property
    def road(self):
        road = self._components.get("road")
        return road or self.street_aliases

    @property
    def street_name(self):
        street_name = self._components.get("street_name")
        return street_name or self.street_aliases

    @property
    def residential(self):
        residential = self._components.get("residential")
        return residential or self.street_aliases

    @property
    def path(self):
        path = self._components.get("path")
        return path or self.street_aliases

    @property
    def pedestrian(self):
        pedestrian = self._components.get("pedestrian")
        return pedestrian or self.street_aliases

    @property
    def neighbourhood_aliases(self):
        neighbourhood = self._components.get("neighbourhood")
        suburb = self._components.get("suburb")
        city_district = self._components.get("city_district")
        if neighbourhood:  # Priority can be rearranged
            return neighbourhood
        elif suburb:
            return suburb
        elif city_district:
            return city_district

    @property
    def neighbourhood(self):
        neighbourhood = self._components.get("neighbourhood")
        return neighbourhood or self.neighbourhood_aliases

    @property
    def suburb(self):
        suburb = self._components.get("suburb")
        return suburb or self.neighbourhood_aliases

    @property
    def city_district(self):
        city_district = self._components.get("city_district")
        return city_district or self.neighbourhood_aliases

    @property
    def city_aliases(self):
        city = self._components.get("city")
        town = self._components.get("town")
        if city:  # Priority can be rearranged
            return city
        elif town:
            return town
        else:  # if nothing in city_aliases, then return village aliases
            return self.village_aliases

    @property
    def city(self):
        city = self._components.get("city")
        return city or self.city_aliases

    @property
    def town(self):
        town = self._components.get("town")
        return town or self.city_aliases

    @property
    def county(self):
        return self._components.get("county")

    @property
    def village_aliases(self):
        village = self._components.get("village")
        hamlet = self._components.get("hamlet")
        locality = self._components.get("locality")

        if village:  # Priority can be rearranged
            return village
        elif hamlet:
            return hamlet
        elif locality:
            return locality

    @property
    def village(self):
        village = self._components.get("village")
        return village or self.village_aliases

    @property
    def hamlet(self):
        hamlet = self._components.get("hamlet")
        return hamlet or self.village_aliases

    @property
    def locality(self):
        locality = self._components.get("locality")
        return locality or self.village_aliases

    @property
    def state_aliases(self):
        state = self._components.get("state")
        province = self._components.get("province")
        state_code = self._components.get("state_code")

        if state:  # Priority can be rearranged
            return state
        elif province:
            return province
        elif state_code:
            return state_code

    @property
    def state(self):
        state = self._components.get("state")
        return state or self.state_aliases

    @property
    def province(self):
        province = self._components.get("province")
        return province or self.state_aliases

    @property
    def state_code(self):
        state_code = self._components.get("state_code")
        return state_code or self.state_aliases

    @property
    def state_district(self):
        return self._components.get("state_district")

    @property
    def country(self):
        country = self._components.get("country")
        return country or self._components.get("country_name")

    @property
    def country_code(self):
        return self._components.get("country_code")

    @property
    def postal(self):
        return self._components.get("postcode")

    @property
    def postcode(self):
        return self._components.get("postcode")

    @property
    def continent(self):
        return self._components.get("continent")

    @property
    def island(self):
        return self._components.get("island")

    @property
    def region(self):
        return self._components.get("region")

    @property
    def confidence(self):
        return self.object_raw_json.get("confidence")

    @property
    def w3w(self):
        return self._annotations.get("what3words", {}).get("words")

    @property
    def mgrs(self):
        return self._annotations.get("MGRS")

    @property
    def geohash(self):
        return self._annotations.get("geohash")

    @property
    def callingcode(self):
        return self._annotations.get("callingcode")

    @property
    def Maidenhead(self):
        return self._annotations.get("Maidenhead")

    @property
    def DMS(self):
        return self._annotations.get("DMS")

    @property
    def Mercator(self):
        return self._annotations.get("Mercator")

    @property
    def bbox(self) -> List[float]:
        """Output answer as GeoJSON bbox if it can be calculated/retrieved."""
        south = self._bounds.get("southwest", {}).get("lat")
        north = self._bounds.get("northeast", {}).get("lat")
        west = self._bounds.get("southwest", {}).get("lng")
        east = self._bounds.get("northeast", {}).get("lng")
        return (
            [float(west), float(south), float(east), float(north)]
            if all([west, south, east, north])
            else []
        )


class OpenCageQuery(MultipleResultsQuery):
    """
    OpenCage Geocoding Services

    OpenCage Geocoder simple, easy, and open geocoding for the entire world
    Our API combines multiple geocoding systems in the background.
    Each is optimized for different parts of the world and types of requests.
    We aggregate the best results from open data sources and algorithms, so you don't
    have to.
    Each is optimized for different parts of the world and types of requests.

    API Reference: https://geocoder.opencagedata.com/api
    """

    _PROVIDER = "opencage"
    _METHOD = "geocode"
    _URL = "http://api.opencagedata.com/geocode/v1/json"
    _RESULT_CLASS = OpenCageResult
    _KEY = opencage_key

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        base_params = {
            "query": location,
            "key": provider_key,
            "limit": max_results,
        }
        language = kwargs.get("language")
        if language:
            base_params["language"] = language

        countrycode = kwargs.get("countrycode")
        if countrycode:
            base_params["countrycode"] = countrycode

        return base_params

    def _catch_errors(self, json_response):
        status = json_response.get("status")
        if status and status.get("code") != 200:
            self.status_code = status.get("code")
            self.error = status.get("message")

        return self.error

    def _adapt_results(self, json_response):
        # special license attribute
        self.license = json_response["licenses"]
        # Shows the limit and how many remaining calls you have on your
        # API Key. Optional for paid OpenCage accounts
        if json_response.get("rate"):
            self.remaining_api_calls = json_response["rate"]["remaining"]
            self.limit_api_calls = json_response["rate"]["limit"]
        else:
            self.remaining_api_calls = 999999
            self.limit_api_calls = 999999

        # return geo results
        return json_response["results"]


class OpenCageReverseResult(OpenCageResult):
    @property
    def ok(self):
        return bool(self.address)


class OpenCageReverse(OpenCageQuery):
    """
    OpenCage Geocoding Services

    OpenCage Geocoder simple, easy, and open geocoding for the entire world
    Our API combines multiple geocoding systems in the background.
    Each is optimized for different parts of the world and types of requests.
    We aggregate the best results from open data sources and algorithms, so you don't
    have to.
    Each is optimized for different parts of the world and types of requests.

    API Reference: https://geocoder.opencagedata.com/api
    """

    _PROVIDER = "opencage"
    _METHOD = "reverse"
    _URL = "http://api.opencagedata.com/geocode/v1/json"
    _RESULT_CLASS = OpenCageReverseResult

    def _build_params(self, location, provider_key, **kwargs):
        location = Location(location)
        return {
            "query": location,
            "key": provider_key,
        }
