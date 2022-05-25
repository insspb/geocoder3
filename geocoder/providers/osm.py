__all__ = ["OsmResult", "OsmQuery", "OsmQueryDetail", "OsmReverse"]

from typing import Optional

from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.location import Location


class OsmResult(OneResult):
    def __init__(self, json_content):
        # create safe shortcuts
        self._address = json_content.get("address", {})

        # proceed with super.__init__
        super(OsmResult, self).__init__(json_content)

    # ============================ #
    # Geometry - Points & Polygons #
    # ============================ #

    @property
    def lat(self) -> Optional[float]:
        lat = self.object_raw_json.get("lat")
        return float(lat) if lat else None

    @property
    def lng(self) -> Optional[float]:
        lng = self.object_raw_json.get("lon")
        return float(lng) if lng else None

    @property
    def bbox(self) -> dict:
        _boundingbox = self.object_raw_json.get("boundingbox")
        if _boundingbox:
            south = _boundingbox[0]
            west = _boundingbox[2]
            north = _boundingbox[1]
            east = _boundingbox[3]
            return self._get_bbox(south, west, north, east)

    # ========================== #
    # Tags for individual houses #
    # ========================== #

    @property
    def address(self) -> Optional[str]:
        """Full comma-separated address"""
        return self.object_raw_json.get("display_name")

    @property
    def house_number(self) -> Optional[str]:
        return self._address.get("house_number")

    @property
    def street(self) -> Optional[str]:
        return self._address.get("road")

    @property
    def postal(self) -> Optional[str]:
        return self._address.get("postcode")

    # ============================ #
    # Populated settlements, urban #
    # ============================ #

    @property
    def neighborhood(self) -> Optional[str]:
        """place=neighborhood

        A named part of a place=village, a place=town or a place=city. Smaller
        than place=suburb and place=quarter.

        The tag can be used for any kind of landuse or mix of landuse (such as
        residential, commercial, industrial etc). Usage of this term depends
        greatly on local history, culture, politics, economy and organization
        of settlements. More specific rules are intentionally avoided.

        Note: the British English spelling is used rather than the
              American English spelling of neighborhood.
        """
        return self._address.get("neighbourhood")

    @property
    def suburb(self) -> Optional[str]:
        """place=suburb

        A distinct section of an urban settlement (city, town, etc.) with its
        own name and identity. e.g.

        - annexed towns or villages which were formerly independent,
        - independent (or dependent) municipalities within a city or next to a
          much bigger town
        - historical districts of settlements
        - industrial districts or recreation areas within a settlements with
          specific names.
        """
        return self._address.get("suburb")

    @property
    def quarter(self) -> Optional[str]:
        """place=quarter

        A named part of a bigger settlement where this part is smaller than
        a suburb and bigger than a neighbourhood. This does not have to be
        an administrative entity.

        The term quarter is sometimes used synonymously for neighbourhood.
        """
        return self._address.get("quarter")

    # ====================================== #
    # Populated settlements, urban and rural #
    # ====================================== #

    @property
    def allotments(self) -> Optional[str]:
        """place=allotments

        Dacha or cottage settlement, which is located outside other
        inhabited locality. This value is used mainly in Russia and other
        countries of the former Soviet Union, where a lot of such unofficial
        settlements exist
        """
        return self._address.get("hamlet")

    @property
    def farm(self) -> Optional[str]:
        """place=farm

        A farm that has its own name. If the farm is not a part of bigger
        settlement use place=isolated_dwelling. See also landuse=farmyard
        """
        return self._address.get("hamlet")

    @property
    def locality(self) -> Optional[str]:
        """place=isolated_dwelling

        For an unpopulated named place.
        """
        return self._address.get("locality")

    @property
    def isolated_dwelling(self) -> Optional[str]:
        """place=isolated_dwelling

        Smallest kind of human settlement. No more than 2 households.
        """
        return self._address.get("hamlet")

    @property
    def hamlet(self) -> Optional[str]:
        """place=hamlet

        A smaller rural community typically with less than 100-200 inhabitants,
        few infrastructure.
        """
        return self._address.get("hamlet")

    @property
    def village(self) -> Optional[str]:
        """place=village

        A smaller distinct settlement, smaller than a town with few facilities
        available with people traveling to nearby towns to access these.
        Populations of villages vary widely in different territories but will
        nearly always be less than 10,000 people, often a lot less.

        See place=neighbourhood on how to tag divisions within a larger village
        """
        return self._address.get("village")

    @property
    def town(self) -> Optional[str]:
        """place=town

        A second tier urban settlement of local importance, often with a
        population of 10,000 people and good range of local facilities
        including schools, medical facilities etc and traditionally a market.
        In areas of low population, towns may have significantly
        lower populations.

        See place=neighbourhood and possibly also place=suburb on how to tag
        divisions within a town.
        """
        return self._address.get("town")

    @property
    def island(self) -> Optional[str]:
        """place=island

        Identifies the coastline of an island (> 1 km2), also consider
        place=islet for very small islandsIdentifies the coastline of an
        island (> 1 km2), also consider place=islet for very small islands
        """
        return self._address.get("island")

    @property
    def city(self) -> Optional[str]:
        """place=city

        The largest urban settlements in the territory, normally including the
        national, state and provincial capitals. These are defined by charter
        or other governmental designation in some territories and are a matter
        of judgement in others. Should normally have a population of at
        least 100,000 people and be larger than nearby towns.

        See place=suburb and place=neighbourhood on how to tag divisions
        within a city. The outskirts of urban settlements may or may not match
        the administratively declared boundary of the city.
        """
        return self._address.get("city")

    # ================================ #
    # Administratively declared places #
    # ================================ #

    @property
    def municipality(self) -> Optional[str]:
        """admin_level=8"""
        return self._address.get("municipality")

    @property
    def county(self) -> Optional[str]:
        """admin_level=6"""
        return self._address.get("county")

    @property
    def district(self) -> Optional[str]:
        """admin_level=5/6"""
        return self._address.get("city_district")

    @property
    def state(self) -> Optional[str]:
        """admin_level=4"""
        return self._address.get("state")

    @property
    def region(self) -> Optional[str]:
        """admin_level=3"""
        return self._address.get("state")

    @property
    def country(self) -> Optional[str]:
        """admin_level=2"""
        return self._address.get("country")

    @property
    def country_code(self) -> Optional[str]:
        """admin_level=2"""
        return self._address.get("country_code")

    # ======================== #
    # Quality Control & Others #
    # ======================== #

    @property
    def accuracy(self) -> Optional[str]:
        return self.importance

    @property
    def quality(self) -> Optional[str]:
        return self.type

    @property
    def population(self) -> Optional[str]:
        return self.object_raw_json.get("population")

    @property
    def license(self) -> Optional[str]:
        return self.object_raw_json.get("license")

    @property
    def type(self) -> Optional[str]:
        return self.object_raw_json.get("type")

    @property
    def importance(self) -> Optional[str]:
        return self.object_raw_json.get("importance")

    @property
    def icon(self) -> Optional[str]:
        return self.object_raw_json.get("icon")

    @property
    def osm_type(self) -> Optional[str]:
        return self.object_raw_json.get("osm_type")

    @property
    def osm_id(self) -> Optional[str]:
        return self.object_raw_json.get("osm_id")

    @property
    def place_id(self) -> Optional[str]:
        return self.object_raw_json.get("place_id")

    @property
    def place_rank(self) -> Optional[str]:
        return self.object_raw_json.get("place_rank")


class OsmQuery(MultipleResultsQuery):
    """
    Nominatim API Reference: https://nominatim.org/release-docs/develop/api/Overview/
    """

    _PROVIDER = "osm"
    _METHOD = "geocode"
    _URL = "https://nominatim.openstreetmap.org/search"
    _RESULT_CLASS = OsmResult
    _KEY_MANDATORY = False

    def _build_params(
        self,
        location,
        provider_key: str,
        max_results: int = 1,
        **kwargs,
    ) -> dict:
        return {
            "q": location,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": max_results,
        }


class OsmQueryDetail(OsmQuery):

    _METHOD = "details"

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ) -> dict:
        query = {
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": max_results,
        }
        query.update(kwargs)
        return query


class OsmReverse(OsmQuery):

    _METHOD = "reverse"

    def _build_params(
        self,
        location,
        provider_key: str,
        max_results: int = 1,
        **kwargs,
    ) -> dict:
        params = {
            "q": str(Location(location)),
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": max_results,
        }
        if "lang_code" in kwargs:
            params["accept-language"] = kwargs.get("lang_code")
        return params
