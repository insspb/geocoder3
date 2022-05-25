__all__ = ["YandexResult", "YandexQuery", "YandexReverse", "YandexReverseResult"]
from geocoder.base import MultipleResultsQuery, OneResult
from geocoder.keys import yandex_key
from geocoder.location import Location


class YandexResult(OneResult):
    def __init__(self, json_content):
        self._meta_data = json_content["metaDataProperty"]["GeocoderMetaData"]
        super(YandexResult, self).__init__(json_content)

    @property
    def lat(self):
        pos = self.object_raw_json.get("Point", {}).get("pos")
        if pos:
            return pos.split(" ")[1]

    @property
    def lng(self):
        pos = self.object_raw_json.get("Point", {}).get("pos")
        if pos:
            return pos.split(" ")[0]

    @property
    def bbox(self):
        envelope = self._meta_data.get("boundedBy", {}).get("Envelope", {})
        if envelope:
            east, north = envelope.get("upperCorner", "").split(" ")
            west, south = envelope.get("lowerCorner", "").split(" ")
            try:
                return self._get_bbox(south, west, north, east)
            except Exception:
                pass

    @property
    def description(self):
        return self.object_raw_json.get("description")

    @property
    def address(self):
        return self._meta_data.get("text")

    @property
    def quality(self):
        return self._meta_data.get("kind")

    @property
    def accuracy(self):
        return self._meta_data.get("precision")

    @property
    def _country(self):
        return self._meta_data.get("AddressDetails", {}).get("Country", {})

    @property
    def country(self):
        return self._country.get("CountryName")

    @property
    def country_code(self):
        return self._country.get("CountryNameCode")

    @property
    def _administrativeArea(self):
        return self._country.get("AdministrativeArea", {})

    @property
    def state(self):
        return self._administrativeArea.get("AdministrativeAreaName")

    @property
    def _subAdministrativeArea(self):
        return self._administrativeArea.get("SubAdministrativeArea", {})

    @property
    def county(self):
        return self._subAdministrativeArea.get("SubAdministrativeAreaName")

    @property
    def _locality(self):
        return self._subAdministrativeArea.get("Locality") or {}

    @property
    def city(self):
        return self._locality.get("LocalityName")

    @property
    def _thoroughfare(self):
        return self._locality.get("Thoroughfare", {})

    @property
    def street(self):
        return self._thoroughfare.get("ThoroughfareName")

    @property
    def _premise(self):
        return self._thoroughfare.get("Premise", {})

    @property
    def house_number(self):
        return self._premise.get("PremiseNumber")


class YandexQuery(MultipleResultsQuery):
    """
    Yandex

    Yandex (Russian: Яндекс) is a Russian Internet company
    which operates the largest search engine in Russia with
    about 60% market share in that country.

    The Yandex home page has been rated as the most popular website in Russia.

    API Reference: http://api.yandex.com/maps/doc/geocoder/desc/concepts/
    input_params.xml
    """

    _PROVIDER = "yandex"
    _METHOD = "geocode"
    _URL = "https://geocode-maps.yandex.ru/1.x/"
    _RESULT_CLASS = YandexResult
    _KEY = yandex_key

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        return {
            "geocode": location,
            "lang": kwargs.get("lang", "en-US"),
            "kind": kwargs.get("kind", ""),
            "format": "json",
            "apikey": provider_key,
            "results": max_results,
        }

    def _adapt_results(self, json_response):
        return [
            item["GeoObject"]
            for item in json_response["response"]["GeoObjectCollection"][
                "featureMember"
            ]
        ]


class YandexReverseResult(YandexResult):
    @property
    def ok(self):
        return bool(self.address)


class YandexReverse(YandexQuery):
    """
    Yandex

    Yandex (Russian: Яндекс) is a Russian Internet company
    which operates the largest search engine in Russia with
    about 60% market share in that country.
    The Yandex home page has been rated as the most popular website in Russia.

    API Reference: http://api.yandex.com/maps/doc/geocoder/desc/concepts/
    input_params.xml
    """

    _PROVIDER = "yandex"
    _METHOD = "reverse"
    _RESULT_CLASS = YandexReverseResult

    def _build_params(
        self,
        location,
        provider_key,
        max_results: int = 1,
        **kwargs,
    ):
        x, y = Location(location).xy
        self.location = f"{x}, {y}"
        return {
            "geocode": self.location,
            "lang": kwargs.get("lang", "en-US"),
            "kind": kwargs.get("kind", ""),
            "format": "json",
            "apikey": provider_key,
            "results": max_results,
        }
