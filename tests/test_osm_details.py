import geocoder


def test_detailed_query():
    g = geocoder.osm("", postalcode="45326", street="Ellernstraße", method="details")
    assert g.postal == "45326"
    assert "ellern" in g.street.lower()
    assert g.ok
