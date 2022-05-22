import geocoder

location = "Ottawa"


def test_tomtom():
    g = geocoder.tomtom(location)
    assert g.has_data
    osm_count, fields_count = g.debug()[0]
    assert osm_count >= 2
    assert fields_count >= 12


def test_multi_results():
    g = geocoder.tomtom(location, max_results=3)
    assert len(g) == 3
