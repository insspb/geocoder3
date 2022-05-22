# flake8: noqa
from geocoder.providers.addresses import (
    BingBatch,
    BingBatchForward,
    BingBatchResult,
    BingQuery,
    BingQueryDetail,
    BingResult,
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
    GeonamesResult,
    GisgraphyQuery,
    GisgraphyResult,
    GoogleQuery,
    GoogleResult,
    HereQuery,
    HereResult,
    KomootQuery,
    KomootResult,
    LocationIQQuery,
    MapboxQuery,
    MapboxResult,
    MapquestBatch,
    MapquestQuery,
    MapquestResult,
    MapzenQuery,
    MapzenResult,
    MaxmindQuery,
    OpenCageQuery,
    OpenCageResult,
    OttawaQuery,
    PlacesQuery,
    TamuQuery,
    TgosQuery,
    TomtomQuery,
    USCensusBatch,
    USCensusQuery,
    W3WQuery,
    W3WResult,
    YahooQuery,
    YandexQuery,
    YandexResult,
)
<<<<<<< HEAD
from geocoder.providers.arcgis import ArcgisQuery, ArcgisReverse
=======
from geocoder.providers.baidu import BaiduQuery, BaiduReverse
>>>>>>> 50d7915 (Merge baidu and baidu_reverse and move to core providers)
from geocoder.providers.freegeoip import FreeGeoIPQuery
from geocoder.providers.ipfinder import IpfinderQuery
from geocoder.providers.ipinfo import IpinfoQuery
from geocoder.providers.osm import OsmQuery, OsmQueryDetail, OsmResult, OsmReverse
from geocoder.providers.reverse import (
<<<<<<< HEAD
    BaiduReverse,
=======
    ArcgisReverse,
>>>>>>> 50d7915 (Merge baidu and baidu_reverse and move to core providers)
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
