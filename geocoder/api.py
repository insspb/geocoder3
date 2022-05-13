from geocoder.distance import Distance
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
    OsmQuery,
    OsmQueryDetail,
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
from geocoder.providers.ip import FreeGeoIPQuery, IpfinderQuery, IpinfoQuery
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
    OsmReverse,
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


def get_result(query, provider: str = "osm", method: str = "geocode", **kwargs):
    """Return geocoding result for query request

    :param query: Location, locations list, or ip you want to geocode.
    :param provider: The geocoding engine you want to use.
    :param method: Define the method (geocode, method).
    """
    provider = provider.lower().strip()
    method = method.lower().strip()

    if not isinstance(query, str) and method == "geocode":
        raise ValueError("Location should be a string")

    if provider not in options:
        raise ValueError("Invalid provider")

    if method not in options[provider]:
        raise ValueError("Invalid method")

    return options[provider][method](query, **kwargs)


def distance(*args, **kwargs):
    """Distance tool measures the distance between two or multiple points.

    :param location: (min 2x locations) Your search location you want geocoded.
    :param units: (default=kilometers) Unit of measurement.
        > kilometers
        > miles
        > feet
        > meters
    """
    return Distance(*args, **kwargs)


def google(query, method: str = "geocode", **kwargs):
    """Google Provider

    :param query: Your search location you want geocoded.
    :param method: (default=geocode) Use the following:
        > geocode
        > places
        > reverse
        > batch
        > timezone
        > elevation
    """
    return get_result(query, provider="google", method=method, **kwargs)


def mapbox(query, method: str = "geocode", **kwargs):
    """Mapbox Provider

    :param query: Your search location you want geocoded.
    :param proximity: Search nearby [lat, lng]
    :param method: (default=geocode) Use the following:
        > geocode
        > reverse
        > batch
    """
    return get_result(query, provider="mapbox", method=method, **kwargs)


def yandex(query, method: str = "geocode", **kwargs):
    """Yandex Provider

    :param query: Your search location you want geocoded.
    :param apikey: YANDEX API KEY
    :param maxRows: (default=1) Max number of results to fetch
    :param lang: Chose the following language:
        > ru-RU — Russian (by default)
        > uk-UA — Ukrainian
        > be-BY — Belarusian
        > en-US — American English
        > en-BR — British English
        > tr-TR — Turkish (only for maps of Turkey)
    :param kind: Type of toponym (only for reverse geocoding):
        > house - house or building
        > street - street
        > metro - subway station
        > district - city district
        > locality - locality (city, town, village, etc.)
    """
    return get_result(query, provider="yandex", method=method, **kwargs)


def w3w(query, method: str = "geocode", **kwargs):
    """what3words Provider

    :param query: Your search location you want geocoded.
    :param key: W3W API key.
    :param method: Chose a method (geocode, method)
    """
    return get_result(query, provider="w3w", **kwargs)


def baidu(query, method: str = "geocode", **kwargs):
    """Baidu Provider

    :param query: Your search location you want geocoded.
    :param key: Baidu API key.
    :param referer: Baidu API referer website.
    """
    return get_result(query, provider="baidu", method=method, **kwargs)


def gaode(query, method: str = "geocode", **kwargs):
    """Gaode Provider

    :param query: Your search location you want geocoded.
    :param key: Gaode API key.
    :param referer: Gaode API referer website.
    """
    return get_result(query, provider="gaode", method=method, **kwargs)


def komoot(query, method: str = "geocode", **kwargs):
    """Ottawa Provider

    :param query: Your search location you want geocoded.
    """
    return get_result(query, provider="komoot", method=method, **kwargs)


def ottawa(query, method: str = "geocode", **kwargs):
    """Ottawa Provider

    :param query: Your search location you want geocoded.
    :param maxRows: (default=1) Max number of results to fetch
    """
    return get_result(query, provider="ottawa", method=method, **kwargs)


def bing(query, method: str = "geocode", **kwargs):
    """Bing Provider

    :param query: Your search location you want geocoded.
    :param key: (optional) use your own API Key from Bing.
    :param maxRows: (default=1) Max number of results to fetch
    :param method: (default=geocode) Use the following:
        > geocode
        > reverse
    """
    return get_result(query, provider="bing", method=method, **kwargs)


def yahoo(query, method: str = "geocode", **kwargs):
    """Yahoo Provider

    :param query: Your search location you want geocoded.
    """
    return get_result(query, provider="yahoo", method=method, **kwargs)


def geolytica(query, method: str = "geocode", **kwargs):
    """Geolytica (Geocoder.ca) Provider

    :param query: Your search location you want geocoded.
    """
    return get_result(query, provider="geolytica", method=method, **kwargs)


def geocodexyz(query, method: str = "geocode", **kwargs):
    """Geocode.xyz Provider
    :param query: Your search location you want geocoded.
    """
    return get_result(query, provider="geocodexyz", method=method, **kwargs)


def opencage(query, method: str = "geocode", **kwargs):
    """Opencage Provider

    :param query: Your search location you want geocoded.
    :param key: (optional) use your own API Key from OpenCage.
    """
    return get_result(query, provider="opencage", method=method, **kwargs)


def arcgis(query, method: str = "geocode", **kwargs):
    """ArcGIS Provider

    :arg query: Your search location you want geocoded.
    :param method: Some
    """
    return get_result(query, provider="arcgis", method=method, **kwargs)


def here(query, method: str = "geocode", **kwargs):
    """HERE Provider

    :param query: Your search location you want geocoded.
    :param app_code: (optional) use your own Application Code from HERE.
    :param app_id: (optional) use your own Application ID from HERE.
    :param maxRows: (default=1) Max number of results to fetch
    :param method: (default=geocode) Use the following:
        > geocode
        > reverse
    """
    return get_result(query, provider="here", method=method, **kwargs)


def tomtom(query, method: str = "geocode", **kwargs):
    """TomTom Provider

    :param query: Your search location you want geocoded.
    :param key: (optional) use your own API Key from TomTom.
    :param maxRows: (default=1) Max number of results to fetch
    """
    return get_result(query, provider="tomtom", method=method, **kwargs)


def mapquest(query, method: str = "geocode", **kwargs):
    """MapQuest Provider

    :param query: Your search location you want geocoded.
    :param key: (optional) use your own API Key from MapQuest.
    :param maxRows: (default=1) Max number of results to fetch
    :param method: (default=geocode) Use the following:
        > geocode
        > reverse
    """
    return get_result(query, provider="mapquest", method=method, **kwargs)


def osm(query, method: str = "geocode", **kwargs):
    """OSM Provider

    :param query: Your search location you want geocoded.
    :param url: Custom OSM Server URL location
               (ex: http://nominatim.openstreetmap.org/search)
    """
    return get_result(query, provider="osm", method=method, **kwargs)


def maxmind(query="me", method: str = "geocode", **kwargs):
    """MaxMind Provider

    :param query: Your search IP Address you want geocoded.
    :param location: (optional) if left blank will return your
                                current IP address's location.
    """
    return get_result(query, provider="maxmind", method=method, **kwargs)


def ipinfo(query="", method: str = "geocode", **kwargs):
    """IP Info.io Provider

    :param query: Your search IP Address you want geocoded.
                  If left blank will return your current IP address's location.
    """
    return get_result(query, provider="ipinfo", method=method, **kwargs)


def freegeoip(query, method: str = "geocode", **kwargs):
    """FreeGeoIP Provider

    :param query: Your search IP Address you want geocoded.
                  If left blank will return your current IP address's location.
    """
    return get_result(query, provider="freegeoip", method=method, **kwargs)


def canadapost(query, method: str = "geocode", **kwargs):
    """CanadaPost Provider

    :param query: Your search location you want geocoded.
    :param key: (optional) API Key from CanadaPost Address Complete.
    :param language: (default=en) Output language preference.
    :param country: (default=ca) Geofenced query by country.
    :param maxRows: (default=1) Max number of results to fetch
    """
    return get_result(query, provider="canadapost", method=method, **kwargs)


def geonames(query, method: str = "geocode", **kwargs):
    """GeoNames Provider

    :param query: Your search location you want geocoded.
    :param geonameid: The place you want children / hierarchy for.
    :param key: (required) geonames *username*: needs to be passed with each request
    :param maxRows: (default=1) Max number of results to fetch
    :param proximity: Search within given area (bbox, bounds, or around latlng)
    :param method: (default=geocode) Use the following:
        > geocode
        > details (mainly for administrive data and timezone)
        > timezone (alias for details)
        > children
        > hierarchy
    """
    return get_result(query, provider="geonames", method=method, **kwargs)


def mapzen(query, method: str = "geocode", **kwargs):
    """Mapzen Provider

    :param query: Your search location you want geocoded.
    :param maxRows: (default=1) Max number of results to fetch
    """
    return get_result(query, provider="mapzen", method=method, **kwargs)


def tamu(query, method: str = "geocode", **kwargs):
    """TAMU Provider

    :param query: The street address of the location you want geocoded.
    :param city: The city of the location to geocode.
    :param state: The state of the location to geocode.
    :param zipcode: The zipcode of the location to geocode.
    :param key: The API key (use API key "demo" for testing).

    API Reference: https://geoservices.tamu.edu/Services/Geocode/WebService
    """
    return get_result(query, provider="tamu", method=method, **kwargs)


def geocodefarm(query, method: str = "geocode", **kwargs):
    """GeocodeFarm Provider

    :param query: The string to search for. Usually a street address.
    :param key: (optional) API Key. Only Required for Paid Users.
    :param lang: (optional) 2 digit language code to return results in.
                Currently only "en"(English) or "de"(German) supported.
    :param country: (optional) The country to return results in. Used for biasing
                purposes and may not fully filter results to this specific country.
    :param maxRows: (default=1) Max number of results to fetch

    API Reference: https://geocode.farm/geocoding/free-api-documentation/
    """
    return get_result(query, provider="geocodefarm", method=method, **kwargs)


def tgos(query, method: str = "geocode", **kwargs):
    """TGOS Provider

    :param query: Your search location you want geocoded.
    :param language: (default=taiwan) Use the following:
        > taiwan
        > english
        > chinese
    :param method: (default=geocode) Use the following:
        > geocode

    API Reference: http://api.tgos.nat.gov.tw/TGOS_MAP_API/Web/Default.aspx
    """
    return get_result(query, provider="tgos", method=method, **kwargs)


def uscensus(query, method: str = "geocode", **kwargs):
    """US Census Provider

    :param query: Your search location(s) you want geocoded.
    :param benchmark: (default=4) Use the following:
        > Public_AR_Current or 4
        > Public_AR_ACSYYYY or 8
        > Public_AR_Census2010 or 9
    :param vintage: (default=4, not available with batch method) Use the following:
        > Current_Current or 4
        > Census2010_Current or 410
        > ACS2013_Current or 413
        > ACS2014_Current or 414
        > ACS2015_Current or 415
        > Current_ACS2015 or 8
        > Census2010_ACS2015 or 810
        > ACS2013_ACS2015 or 813
        > ACS2014_ACS2015 or 814
        > ACS2015_ACS2015 or 815
        > Census2010_Census2010 or 910
        > Census2000_Census2010 or 900
    :param method: (default=geocode) Use the following:
        > geocode
        > reverse
        > batch

    API Reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
    """
    return get_result(query, provider="uscensus", method=method, **kwargs)


def locationiq(query, method: str = "geocode", **kwargs):
    """LocationIQ Provider

    :param query: Your search location you want geocoded.
    :param method: (default=geocode) Use the following:
        > geocode
        > reverse

    API Reference: https://locationiq.org/
    """
    return get_result(query, provider="locationiq", method=method, **kwargs)


def gisgraphy(query, method: str = "geocode", **kwargs):
    """Gisgraphy Provider

    :param query: Your search location you want geocoded.
    """
    return get_result(query, provider="gisgraphy", method=method, **kwargs)


def ipfinder(query="", method: str = "geocode", **kwargs):
    """IPFinder.io Provider

    :param query: Your search IP Address you want geocoded.
                        (optional) if left blank will return your current IP address's
                        location.
    :param key: API Key from IPFinder (optional). Blank will use the free API KEY.
    """
    return get_result(query, provider="ipfinder", method=method, **kwargs)
