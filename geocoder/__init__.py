"""
Geocoder
~~~~~~~~

Simple and consistent geocoding library written in Python.

Many online providers such as Google & Bing have geocoding services,
these providers do not include Python libraries and have different
JSON responses between each other.

Consistant JSON responses from various providers.

    >>> import geocoder
    >>> g = geocoder.google('New York City')
    >>> g.latlng
    [40.7127837, -74.0059413]
    >>> g.state
    'New York'
    >>> g.json
    ...

"""

__title__ = "geocoder3"
__author__ = "Andrey Shpak"
__author_email__ = "ashpak@ashpak.ru"
__version__ = "2.0.0"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 Andrey Shpak"

from geocoder.api import (  # noqa
    arcgis,
    baidu,
    bing,
    canadapost,
    distance,
    freegeoip,
    gaode,
    geocodefarm,
    geocodexyz,
    geolytica,
    geonames,
    get_result,
    gisgraphy,
    google,
    here,
    ipfinder,
    ipinfo,
    komoot,
    locationiq,
    mapbox,
    mapquest,
    mapzen,
    maxmind,
    opencage,
    osm,
    ottawa,
    tamu,
    tgos,
    tomtom,
    uscensus,
    w3w,
    yahoo,
    yandex,
)
from geocoder.cli import cli  # noqa
from geocoder.location import Location  # noqa
