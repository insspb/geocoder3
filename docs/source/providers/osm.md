# OpenStreetMap(Nominatim)

Nominatim (from the Latin, 'by name') is a tool to search OSM data by name and
address and to generate synthetic addresses of OSM points (reverse geocoding). Using
Geocoder you can retrieve OSM's geocoded data from Nominatim.

## Simple usage

OpenStreetMap does not require any keys for work. So you can begin without any setup.

```python
import geocoder

g = geocoder.osm('New York city')
print(g.latlng)
# [40.7127281, -74.0060152]
print(g[0].latlng)
# Same as g.latlng: [40.7127281, -74.0060152]
```

This provider may return multiple results by setting the parameter `max_results` to the
desired number. By default, 1 entry retrieved. Multiple results contained as
internal sequence. You can check any result, by direct member object calling like in
normal lists. Without member number mention, object with index 0 is always called.

```python
import geocoder

g = geocoder.osm('New York city', max_results=3)
print(g[0].latlng)
# [40.7127281, -74.0060152]
print(g.latlng)
# Same as g[0].latlng: [40.7127281, -74.0060152]
print(g[1].latlng)
# Other result: [40.75126905, -73.98482021795536]
```

## Custom or Local Nominatim Server

Setting up your own local offline Nominatim server is possible, using the following the
[Nominatim Install] instructions. This enables you to request as much geocoding as
your need.

Also, usage of any custom Nominatim Server is possible with setting `url` parameter.
`url` should point to direct `/search` endpoint, check example below.

```python
import geocoder

g = geocoder.osm("New York City", url="http://localhost/nominatim/search")
print(g[0].latlng)
# [40.7127281, -74.0060152]
```

## OSM Addresses

The [addr tag] is the prefix for several `addr:*` keys to describe addresses.

This format is meant to be saved as a CSV and imported into JOSM.

```python
import geocoder
g = geocoder.osm('11 Wall Street, New York')
print(g.osm)
# {
#     "x": -74.010865,
#     "y": 40.7071407,
#     "addr:country": "United States of America",
#     "addr:state": "New York",
#     "addr:housenumber": "11",
#     "addr:postal": "10005",
#     "addr:city": "NYC",
#     "addr:street": "Wall Street"
# }
```

## Command Line Interface

```bash
geocode 'New York city' --provider osm --out geojson | jq .
geocode 'New York city' -p osm -o osm
geocode 'New York city' -p osm --url localhost
```

## Helper method parameters

Helper method is recommended way to use providers, if no class extension required.
During project modification this public API will be last thing for non-compatible
changes.

```{eval-rst}
.. autofunction:: geocoder.osm
   :noindex:
```

## Working class API

```{eval-rst}
.. autoclass:: geocoder.providers.OsmQuery
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
```

## Returned object properties

```{eval-rst}
.. autoclass:: geocoder.providers.OsmResult
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
```

## References

- [Nominatim Project](http://wiki.openstreetmap.org/wiki/Nominatim)
- [Nominatim Install]
- [addr tag]

[_addr tag]: http://wiki.openstreetmap.org/wiki/Key:addr
[Nominatim Install]: https://nominatim.org/release-docs/latest/admin/Installation/
