import geocoder

location = "Ottawa"


def test_ottawa():
    g = geocoder.ottawa(location)
    assert g.has_data
    osm_count, fields_count = g.debug()[0]
    assert osm_count >= 3
    assert fields_count >= 10


def test_multi_results():
    g = geocoder.ottawa(location, max_results=3)
    assert len(g) == 3
