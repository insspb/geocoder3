import geocoder

location = "8.8.8.8"


def test_maxmind():
    g = geocoder.maxmind(location)
    assert g.has_data
    osm_count, fields_count = g.debug()[0]
    assert osm_count >= 1
    assert fields_count >= 13
