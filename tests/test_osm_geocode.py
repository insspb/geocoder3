import geocoder

location = "Ottawa, Ontario"


def test_osm():
    g = geocoder.osm(location)
    assert g.ok
    osm_count, fields_count = g.debug()[0]
    assert osm_count >= 3
    assert fields_count >= 21


def test_multi_results():
    g = geocoder.osm(location, maxRows="5")
    assert len(g) == 5
