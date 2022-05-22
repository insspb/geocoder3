<!-- markdownlint-disable -->
<h1 align="center" style="margin:1em">
  <a href="https://geocoder3.readthedocs.org/">
    <img src="https://github.com/insspb/geocoder3/raw/master/docs/source/_static/geocoder.png"
         alt="Markdownify"
         width="200"></a>
  <br />
  Python Geocoder
</h1>

<h4 align="center">
  Simple and consistent geocoding library written in Python.
</h4>

<p align="center">
    <img src="https://github.com/insspb/geocoder3/actions/workflows/checks.yml/badge.svg?branch=master" alt="Tests" />
  <a href="http://geocoder3.readthedocs.io/?badge=master">
    <img src="https://readthedocs.org/projects/geocoder3/badge/?version=master"
         alt="RDT">
  </a>
  <a href="https://pypi.python.org/pypi/geocoder3">
    <img src="https://img.shields.io/pypi/v/geocoder3.svg"
         alt="PyPi">
  </a>
  <a href="https://codecov.io/gh/insspb/geocoder3">
    <img src="https://codecov.io/gh/insspb/geocoder3/branch/master/graph/badge.svg?token=HoUly1aQHN"
         alt="Codecov" />
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg"
         alt="Code Style" />
  </a>
</p>
<br>

Table of content
----------------

<!-- TOC -->

- [Table of content](#table-of-content)
- [Overview](#overview)
- [A glimpse at the API](#a-glimpse-at-the-api)
    - [Forward](#forward)
    - [Multiple queries ('batch' geocoding)](#multiple-queries-batch-geocoding)
    - [Multiple results](#multiple-results)
    - [Reverse](#reverse)
    - [House Addresses](#house-addresses)
    - [IP Addresses](#ip-addresses)
    - [Bounding Box](#bounding-box)
- [Command Line Interface](#command-line-interface)
- [Providers](#providers)
- [Installation](#installation)
    - [PyPi Install](#pypi-install)
    - [GitHub Install](#github-install)
    - [Snap Install](#snap-install)
- [Feedback](#feedback)
- [Contribution](#contribution)
    - [Documenting](#documenting)
    - [Coding](#coding)
- [ChangeLog](#changelog)

<!-- /TOC -->

## Overview

Many online providers such as Google & Bing have geocoding services,
these providers do not include Python libraries and have different
JSON responses between each other.

It can be very difficult sometimes to parse a particular geocoding provider
since each one of them have their own JSON schema.

Here is a typical example of retrieving a Lat & Lng from Google using Python,
things shouldn't be this hard.

```python
import requests
url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'sensor': 'false', 'address': 'Mountain View, CA'}
r = requests.get(url, params=params)
results = r.json()['results']
location = results[0]['geometry']['location']
location['lat'], location['lng']
# (37.3860517, -122.0838511)
```

Now lets use Geocoder to do the same task

```python
import geocoder
g = geocoder.google('Mountain View, CA', key='YOUR_GOOGLE_API_KEY')
g.latlng
# (37.3860517, -122.0838511)
```

## A glimpse at the API

Many properties are available once the geocoder object is created.

### Forward

```python
import geocoder

g = geocoder.google('Mountain View, CA', key='YOUR_GOOGLE_API_KEY')
g.geojson
g.object_json
g.wkt
g.osm
```

### Multiple queries ('batch' geocoding)

```python
import geocoder
g = geocoder.mapquest(['Mountain View, CA', 'Boulder, Co'], method='batch')
for result in g:
    print(result.address, result.latlng)
# ('Mountain View', [37.39008, -122.08139])
# ('Boulder', [40.015831, -105.27927])
```

### Multiple results

```python
import geocoder
g = geocoder.geonames('Mountain View, CA', maxRows=5)
print(len(g))
# 5
for result in g:
    print(result.address, result.latlng)
# Mountain View ['37.38605', '-122.08385']
# Mountain View Elementary School ['34.0271', '-117.59116']
# Best Western Plus Mountainview Inn and Suites ['51.79516', '-114.62793']
# Best Western Mountainview Inn ['49.3338', '-123.1446']
# Mountain View Post Office ['37.393', '-122.07774']
```


> The providers currently supporting multiple results are listed in the table
> [below](#providers).

### Reverse

```python
import geocoder
g = geocoder.google([45.15, -75.14], method='reverse', key='YOUR_GOOGLE_API_KEY')
g.city
g.state
g.state_long
g.country
g.country_long
```

### House Addresses

```python
import geocoder

g = geocoder.google("453 Booth Street, Ottawa ON", key='YOUR_GOOGLE_API_KEY')
g.house_number
g.postal
g.street
g.street_long
```

### IP Addresses

```python
import geocoder
g = geocoder.freegeoip('199.7.157.0')
g.latlng
# [43.7154, -79.3896]
g.city
# Toronto
```

### Bounding Box

Accessing the JSON & GeoJSON attributes will be different

```python
import geocoder
g = geocoder.osm("Ottawa")
g.bbox
# {'northeast': [45.5569506, -75.5251593], 'southwest': [45.2369506, -75.8451593]}

g.southwest
# [45.2369506, -75.8451593]
```

## Command Line Interface

```bash
geocode "Ottawa, ON"  >> ottawa.geojson
geocode "Ottawa, ON" --provider osm --output geojson --method geocode
```

## Providers

| Geocoder3 ready | Provider                       | Optimal   | Usage Policy                    | Multiple results | Reverse | Proximity | Batch |
|-----------------|:-------------------------------|:----------|:--------------------------------|:-----------------|:--------|:----------|:------|
|                 | [ArcGIS][ArcGIS]               | World     |                                 | yes              | yes     |           |       |
|                 | [Baidu][Baidu]                 | China     | API key                         |                  | yes     |           |       |
|                 | [Bing][Bing]                   | World     | API key                         | yes              | yes     |           | yes   |
|                 | [CanadaPost][CanadaPost]       | Canada    | API key                         | yes              |         |           |       |
|                 | [FreeGeoIP][FreeGeoIP]         | World     | Rate Limit, [Policy][FreeGeoip-Policy]                |                  |         |           |       |
|                 | [Gaode][Gaode]                 | China     | API key                         |                  | yes     |           |       |
|                 | [Geocoder.ca][Geocoder.ca] (Geolytica) | CA & US | Rate Limit                |                  |         |           |       |
|                 | [GeocodeFarm][GeocodeFarm]     | World     | [Policy][GeocodeFarm-Policy]    | yes              | yes     |           |       |
|                 | [GeoNames][GeoNames]           | World     | Username                        | yes              |         | yes       |       |
|                 | [GeoOttawa][GeoOttawa]         | Ottawa    |                                 | yes              |         |           |       |
|                 | [Gisgraphy][Gisgraphy]         | World     | API key                         | yes              | yes     | yes       |       |
|                 | [Google][Google]               | World     | Rate Limit, [Policy][G-Policy]  | yes              | yes     | yes       |       |
|                 | [HERE][HERE]                   | World     | API key                         | yes              | yes     |           |       |
|                 | [IPInfo][IPInfo]               | World     | Rate Limit, [Plans][IP-Plans]   |                  |         |           |       |
|                 | [Komoot][Komoot] (OSM powered) | World     |                                 | yes              | yes     |           |       |
|                 | [LocationIQ][LocationIQ]       | World     | API Key                         | yes              | yes     |           |       |
|                 | [Mapbox][Mapbox]               | World     | API key                         | yes              | yes     | yes       |       |
|                 | [MapQuest][MapQuest]           | World     | API key                         | yes              | yes     |           | yes   |
|                 | [~~Mapzen~~][Mapzen]           | Shutdown  | API key                         | yes              | yes     |           |       |
|                 | [MaxMind][MaxMind]             | World     |                                 |                  |         |           |       |
|                 | [OpenCage][OpenCage]           | World     | API key                         | yes              | yes     |           |       |
| YES             | [OpenStreetMap][OpenStreetMap] | World     | [Policy][OpenStreetMap-Policy]  | yes              | yes     |           |       |
|                 | [Tamu][Tamu]                   | US        | API key                         |                  |         |           |       |
|                 | [TGOS][TGOS]                   | Taiwan    |                                 |                  |         |           |       |
|                 | [TomTom][TomTom]               | World     | API key                         | yes              |         |           |       |
|                 | [USCensus][USCensus]           | US        |                                 |                  | yes     |           | yes   |
|                 | [What3Words][What3Words]       | World     | API key                         |                  | yes     |           |       |
|                 | [Yahoo][Yahoo]                 | World     |                                 |                  |         |           |       |
|                 | [Yandex][Yandex]               | Russia    |                                 | yes              | yes     |           |       |
|                 | [IPFinder][IPFinder]           | World     | Rate Limit, [Plans][IPFinder]   | yes              | yes     |           |       |


## Installation

### PyPi Install

To install Geocoder3, simply:

```bash
pip install geocoder3
```

### GitHub Install

Installing the latest version from Github:

```bash
git clone https://github.com/insspb/geocoder3
cd geocoder3
python setup.py install
```

## Feedback

Please feel free to give any feedback on this module. just create an
[issue](https://github.com/insspb/geocoder3/issues) on GitHub

## Contribution

If you find any bugs or any enhancements to recommend please send some of your
comments/suggestions to the
[Github Issues Page](https://github.com/insspb/geocoder3/issues).

Some way to contribute, from the most generic to the most detailed:

### Documenting

If you are not comfortable with development, you can still contribute with the
documentation.

- Review the documentation of a specific provider. Most of the time it require more
  details.
- Review the parameters for a specific method, compared to what is supported by the
  provider
- Review documentation for command line

If you miss any feature, just create an
[issue](https://github.com/insspb/geocoder3/issues) accordingly.
Be sure to describe your use case clearly, and to provide links to the correct sources.

### Coding

- Add support for a new provider. _Documentation TBD_, starting point possible with
- [wip_guide](https://geocoder3.readthedocs.io/wip_guide.html).
- Extend methods for an existing support, i.e support an additional API).
- Extend support of an existing API, i.e, support more (json) fields from the
  response, or more parameters.


## ChangeLog

See [Releases](https://github.com/insspb/geocoder3/releases)


[TGOS]: http://geocoder.readthedocs.org/providers/TGOS.html
[Mapbox]: http://geocoder.readthedocs.org/providers/Mapbox.html
[Google]: http://geocoder.readthedocs.org/providers/Google.html
[G-Policy]: https://developers.google.com/maps/documentation/geocoding/usage-limits
[Bing]: http://geocoder.readthedocs.org/providers/Bing.html
[LocationIQ]: http://geocoder.readthedocs.org/providers/LocationIQ.html
[OpenStreetMap]: http://geocoder.readthedocs.org/providers/OpenStreetMap.html
[OpenStreetMap-Policy]: https://operations.osmfoundation.org/policies/nominatim/
[HERE]: http://geocoder.readthedocs.org/providers/HERE.html
[TomTom]: http://geocoder.readthedocs.org/providers/TomTom.html
[MapQuest]: http://geocoder.readthedocs.org/providers/MapQuest.html
[OpenCage]: http://geocoder.readthedocs.org/providers/OpenCage.html
[Yahoo]: http://geocoder.readthedocs.org/providers/Yahoo.html
[ArcGIS]: http://geocoder.readthedocs.org/providers/ArcGIS.html
[Yandex]: http://geocoder.readthedocs.org/providers/Yandex.html
[Geocoder.ca]: http://geocoder.readthedocs.org/providers/Geocoder-ca.html
[Baidu]: http://geocoder.readthedocs.org/providers/Baidu.html
[GeoOttawa]: http://geocoder.readthedocs.org/providers/GeoOttawa.html
[FreeGeoIP]: http://geocoder.readthedocs.org/providers/FreeGeoIP.html
[FreeGeoip-Policy]: https://github.com/apilayer/freegeoip#readme
[MaxMind]: http://geocoder.readthedocs.org/providers/MaxMind.html
[Mapzen]: https://mapzen.com/blog/shutdown
[What3Words]: http://geocoder.readthedocs.org/providers/What3Words.html
[CanadaPost]: http://geocoder.readthedocs.org/providers/CanadaPost.html
[GeoNames]: http://geocoder.readthedocs.org/providers/GeoNames.html
[IPInfo]: http://geocoder.readthedocs.org/providers/IPInfo.html
[Tamu]: http://geoservices.tamu.edu/Services/Geocode/WebService/
[GeocodeFarm]: https://geocode.farm/
[GeocodeFarm-Policy]: https://geocode.farm/geocoding/free-api-documentation/
[Gaode]: http://geocoder.readthedocs.org/providers/.html
[IP-Plans]: http://ipinfo.io/pricing
[Komoot]: http://photon.komoot.de
[USCensus]: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
[Gisgraphy]: https://premium.gisgraphy.com/
[IPFinder]: https://ipfinder.io/
