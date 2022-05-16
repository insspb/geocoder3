import geocoder

ottawa = (45.4215296, -75.6971930)


def test_osm_reverse():
    g = geocoder.osm(ottawa, method="reverse")
    assert g.ok
