from geocoder.distance import Distance
from geocoder.providers import (
    FreeGeoIPQuery,
    IpfinderQuery,
    IpinfoQuery,
    OsmQuery,
    OsmQueryDetail,
    OsmReverse,
)
from geocoder.providers.addresses import (
    ArcgisQuery,
    BaiduQuery,
    BingBatchForward,
    BingQuery,
    BingQueryDetail,
    CanadapostQuery,
    ElevationQuery,
    GaodeQuery,
    GeocodeFarmQuery,
    GeocodeXYZQuery,
    GeolyticaQuery,
    GeonamesChildren,
    GeonamesDetails,
    GeonamesHierarchy,
    GeonamesQuery,
    GisgraphyQuery,
    GoogleQuery,
    HereQuery,
    KomootQuery,
    LocationIQQuery,
    MapboxQuery,
    MapquestBatch,
    MapquestQuery,
    MapzenQuery,
    MaxmindQuery,
    OpenCageQuery,
    OttawaQuery,
    PlacesQuery,
    TamuQuery,
    TgosQuery,
    TomtomQuery,
    USCensusBatch,
    USCensusQuery,
    W3WQuery,
    YahooQuery,
    YandexQuery,
)
from geocoder.providers.reverse import (
    ArcgisReverse,
    BaiduReverse,
    BingBatchReverse,
    BingReverse,
    GaodeReverse,
    GeocodeFarmReverse,
    GisgraphyReverse,
    GoogleReverse,
    HereReverse,
    KomootReverse,
    LocationIQReverse,
    MapboxReverse,
    MapquestReverse,
    MapzenReverse,
    OpenCageReverse,
    USCensusReverse,
    W3WReverse,
    YandexReverse,
)
from geocoder.providers.timezone import GeonamesTimezone, GoogleTimezone

options = {
    "osm": {
        "geocode": OsmQuery,
        "details": OsmQueryDetail,
        "reverse": OsmReverse,
    },
    "tgos": {
        "geocode": TgosQuery,
    },
    "here": {
        "geocode": HereQuery,
        "reverse": HereReverse,
    },
    "baidu": {
        "geocode": BaiduQuery,
        "reverse": BaiduReverse,
    },
    "gaode": {
        "geocode": GaodeQuery,
        "reverse": GaodeReverse,
    },
    "yahoo": {
        "geocode": YahooQuery,
    },
    "tomtom": {
        "geocode": TomtomQuery,
    },
    "arcgis": {
        "geocode": ArcgisQuery,
        "reverse": ArcgisReverse,
    },
    "ottawa": {
        "geocode": OttawaQuery,
    },
    "mapbox": {
        "geocode": MapboxQuery,
        "reverse": MapboxReverse,
    },
    "maxmind": {
        "geocode": MaxmindQuery,
    },
    "ipinfo": {
        "geocode": IpinfoQuery,
    },
    "geonames": {
        "geocode": GeonamesQuery,
        "details": GeonamesDetails,
        "timezone": GeonamesTimezone,
        "children": GeonamesChildren,
        "hierarchy": GeonamesHierarchy,
    },
    "freegeoip": {
        "geocode": FreeGeoIPQuery,
    },
    "w3w": {
        "geocode": W3WQuery,
        "reverse": W3WReverse,
    },
    "yandex": {
        "geocode": YandexQuery,
        "reverse": YandexReverse,
    },
    "mapquest": {
        "geocode": MapquestQuery,
        "reverse": MapquestReverse,
        "batch": MapquestBatch,
    },
    "geolytica": {
        "geocode": GeolyticaQuery,
    },
    "canadapost": {
        "geocode": CanadapostQuery,
    },
    "opencage": {
        "geocode": OpenCageQuery,
        "reverse": OpenCageReverse,
    },
    "bing": {
        "geocode": BingQuery,
        "details": BingQueryDetail,
        "reverse": BingReverse,
        "batch": BingBatchForward,
        "batch_reverse": BingBatchReverse,
    },
    "google": {
        "geocode": GoogleQuery,
        "reverse": GoogleReverse,
        "timezone": GoogleTimezone,
        "elevation": ElevationQuery,
        "places": PlacesQuery,
    },
    "mapzen": {
        "geocode": MapzenQuery,
        "reverse": MapzenReverse,
    },
    "komoot": {
        "geocode": KomootQuery,
        "reverse": KomootReverse,
    },
    "tamu": {
        "geocode": TamuQuery,
    },
    "geocodefarm": {
        "geocode": GeocodeFarmQuery,
        "reverse": GeocodeFarmReverse,
    },
    "uscensus": {
        "geocode": USCensusQuery,
        "reverse": USCensusReverse,
        "batch": USCensusBatch,
    },
    "locationiq": {
        "geocode": LocationIQQuery,
        "reverse": LocationIQReverse,
    },
    "gisgraphy": {
        "geocode": GisgraphyQuery,
        "reverse": GisgraphyReverse,
    },
    "geocodexyz": {
        "geocode": GeocodeXYZQuery,
    },
    "ipfinder": {
        "geocode": IpfinderQuery,
    },
}


def get_results(query, provider: str = "osm", method: str = "geocode", **kwargs):
    """Return geocoding result for query request

    :param query: Location, locations list, or ip you want to geocode.
    :param provider: The geocoding engine you want to use.
    :param method: Any provider's supported request method.
    :param kwargs: Any other provider related options.
    """
    provider = provider.lower().strip()
    method = method.lower().strip()

    if not isinstance(query, str) and method == "geocode":
        raise ValueError("Query should be a string")

    if provider not in options:
        raise ValueError("Invalid provider")

    if method not in options[provider]:
        raise ValueError("Invalid method")

    provider_instance = options[provider][method](query, **kwargs)
    return provider_instance()


def distance(*locations, units: str = "kilometers", **kwargs):
    """Distance tool measures the distance between two or multiple points.

    Supported units values:
        * kilometers
        * miles
        * feet
        * meters

    :param locations: (min 2x locations) Your search location you want geocoded.
    :param units: Unit of measurement, defaults to ``kilometers``.
    """
    return Distance(*locations, units, **kwargs)


def google(query, method: str = "geocode", **kwargs):
    """Google Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``
        * ``places``
        * ``timezone``
        * ``elevation``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="google", method=method, **kwargs)


def mapbox(query, method: str = "geocode", **kwargs):
    """Mapbox Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param proximity: Search nearby [lat, lng]
    """
    return get_results(query, provider="mapbox", method=method, **kwargs)


def yandex(query, method: str = "geocode", **kwargs):
    """Yandex Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param apikey: YANDEX API KEY
    :param max_results: (default=1) Max number of results to fetch
    :param lang: Chose the following language:
        * ru-RU — Russian (by default)
        * uk-UA — Ukrainian
        * be-BY — Belarusian
        * en-US — American English
        * en-BR — British English
        * tr-TR — Turkish (only for maps of Turkey)
    :param kind: Type of toponym (only for reverse geocoding):
        * house - house or building
        * street - street
        * metro - subway station
        * district - city district
        * locality - locality (city, town, village, etc.)
    """
    return get_results(query, provider="yandex", method=method, **kwargs)


def w3w(query, method: str = "geocode", **kwargs):
    """what3words Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: W3W API key.
    """
    return get_results(query, provider="w3w", **kwargs)


def baidu(query, method: str = "geocode", **kwargs):
    """Baidu Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: Baidu API key.
    :param referer: Baidu API referer website.
    """
    return get_results(query, provider="baidu", method=method, **kwargs)


def gaode(query, method: str = "geocode", **kwargs):
    """Gaode Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: Gaode API key.
    :param referer: Gaode API referer website.
    """
    return get_results(query, provider="gaode", method=method, **kwargs)


def komoot(query, method: str = "geocode", **kwargs):
    """Ottawa Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="komoot", method=method, **kwargs)


def ottawa(query, method: str = "geocode", **kwargs):
    """Ottawa Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="ottawa", method=method, **kwargs)


def bing(query, method: str = "geocode", **kwargs):
    """Bing Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``
        * ``details``
        * ``batch``
        * ``batch_reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: (optional) use your own API Key from Bing.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="bing", method=method, **kwargs)


def yahoo(query, method: str = "geocode", **kwargs):
    """Yahoo Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="yahoo", method=method, **kwargs)


def geolytica(query, method: str = "geocode", **kwargs):
    """Geolytica (Geocoder.ca) Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="geolytica", method=method, **kwargs)


def geocodexyz(query, method: str = "geocode", **kwargs):
    """Geocode.xyz Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="geocodexyz", method=method, **kwargs)


def opencage(query, method: str = "geocode", **kwargs):
    """Opencage Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: (optional) use your own API Key from OpenCage.
    """
    return get_results(query, provider="opencage", method=method, **kwargs)


def arcgis(query, method: str = "geocode", **kwargs):
    """ArcGIS Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :arg query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="arcgis", method=method, **kwargs)


def here(query, method: str = "geocode", **kwargs):
    """HERE Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param app_code: (optional) use your own Application Code from HERE.
    :param app_id: (optional) use your own Application ID from HERE.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="here", method=method, **kwargs)


def tomtom(query, method: str = "geocode", **kwargs):
    """TomTom Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: (optional) use your own API Key from TomTom.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="tomtom", method=method, **kwargs)


def mapquest(query, method: str = "geocode", **kwargs):
    """MapQuest Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``
        * ``batch``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: (optional) use your own API Key from MapQuest.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="mapquest", method=method, **kwargs)


def osm(query, method: str = "geocode", **kwargs) -> OsmQuery:
    """OSM Provider

    Provider supported methods:
        * ``geocode``
        * ``details``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param url: Custom OSM Server URL location
               (ex: http://nominatim.openstreetmap.org/search)
    """
    return get_results(query, provider="osm", method=method, **kwargs)


def maxmind(query="me", method: str = "geocode", **kwargs):
    """MaxMind Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search IP Address you want geocoded.
        If left blank will return your current IP address's location.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="maxmind", method=method, **kwargs)


def ipinfo(query="", method: str = "geocode", **kwargs):
    """IP Info.io Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search IP Address you want geocoded.
        If left blank will return your current IP address's location.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="ipinfo", method=method, **kwargs)


def freegeoip(query, method: str = "geocode", **kwargs):
    """FreeGeoIP Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search IP Address you want geocoded.
        If left blank will return your current IP address's location.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="freegeoip", method=method, **kwargs)


def canadapost(query, method: str = "geocode", **kwargs):
    """CanadaPost Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: (optional) API Key from CanadaPost Address Complete.
    :param language: (default=en) Output language preference.
    :param country: (default=ca) Geofenced query by country.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="canadapost", method=method, **kwargs)


def geonames(query, method: str = "geocode", **kwargs):
    """GeoNames Provider

    Provider supported methods:
        * ``geocode``
        * ``details``
        * ``timezone``
        * ``children``
        * ``hierarchy``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param geonameid: The place you want children / hierarchy for.
    :param key: (required) geonames *username*: needs to be passed with each request
    :param max_results: (default=1) Max number of results to fetch
    :param proximity: Search within given area (bbox, bounds, or around latlng)
    """
    return get_results(query, provider="geonames", method=method, **kwargs)


def mapzen(query, method: str = "geocode", **kwargs):
    """Mapzen Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param max_results: (default=1) Max number of results to fetch
    """
    return get_results(query, provider="mapzen", method=method, **kwargs)


def tamu(query, method: str = "geocode", **kwargs):
    """TAMU Provider

    Provider supported methods:
        * ``geocode``

    :param query: The street address of the location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param city: The city of the location to geocode.
    :param state: The state of the location to geocode.
    :param zipcode: The zipcode of the location to geocode.
    :param key: The API key (use API key "demo" for testing).

    API Reference: https://geoservices.tamu.edu/Services/Geocode/WebService
    """
    return get_results(query, provider="tamu", method=method, **kwargs)


def geocodefarm(query, method: str = "geocode", **kwargs):
    """GeocodeFarm Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: The string to search for. Usually a street address.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: (optional) API Key. Only Required for Paid Users.
    :param lang: (optional) 2 digit language code to return results in.
                Currently only "en"(English) or "de"(German) supported.
    :param country: (optional) The country to return results in. Used for biasing
                purposes and may not fully filter results to this specific country.
    :param max_results: (default=1) Max number of results to fetch

    API Reference: https://geocode.farm/geocoding/free-api-documentation/
    """
    return get_results(query, provider="geocodefarm", method=method, **kwargs)


def tgos(query, method: str = "geocode", **kwargs):
    """TGOS Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param language: (default=taiwan) Use the following:
        * taiwan
        * english
        * chinese

    API Reference: http://api.tgos.nat.gov.tw/TGOS_MAP_API/Web/Default.aspx
    """
    return get_results(query, provider="tgos", method=method, **kwargs)


def uscensus(query, method: str = "geocode", **kwargs):
    """US Census Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``
        * ``batch``

    :param query: Your search location(s) you want geocoded.
    :param method: One of provider supported methods, defaults to ``geocode``
    :param benchmark: (default=4) Use the following:
        * Public_AR_Current or 4
        * Public_AR_ACSYYYY or 8
        * Public_AR_Census2010 or 9
    :param vintage: (default=4, not available with batch method) Use the following:
        * Current_Current or 4
        * Census2010_Current or 410
        * ACS2013_Current or 413
        * ACS2014_Current or 414
        * ACS2015_Current or 415
        * Current_ACS2015 or 8
        * Census2010_ACS2015 or 810
        * ACS2013_ACS2015 or 813
        * ACS2014_ACS2015 or 814
        * ACS2015_ACS2015 or 815
        * Census2010_Census2010 or 910
        * Census2000_Census2010 or 900

    API Reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
    """
    return get_results(query, provider="uscensus", method=method, **kwargs)


def locationiq(query, method: str = "geocode", **kwargs):
    """LocationIQ Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.

    API Reference: https://locationiq.org/
    """
    return get_results(query, provider="locationiq", method=method, **kwargs)


def gisgraphy(query, method: str = "geocode", **kwargs):
    """Gisgraphy Provider

    Provider supported methods:
        * ``geocode``
        * ``reverse``

    :param query: Your search location you want geocoded.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    """
    return get_results(query, provider="gisgraphy", method=method, **kwargs)


def ipfinder(query="", method: str = "geocode", **kwargs):
    """IPFinder.io Provider

    Provider supported methods:
        * ``geocode``

    :param query: Your search IP Address you want geocoded.
        If left blank will return your current IP address's location.
    :param method: One of provider's supported methods, defaults to ``geocode``.
    :param key: API Key from IPFinder (optional). Blank will use the free API KEY.
    """
    return get_results(query, provider="ipfinder", method=method, **kwargs)
