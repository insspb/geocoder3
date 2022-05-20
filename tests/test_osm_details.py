import vcr

import geocoder

requests_recorder_ro = vcr.VCR(
    serializer="json",
    cassette_library_dir="tests/cassettes/",
    filter_headers=["Authorization"],
    filter_query_parameters=["key"],
    record_mode="none",
    match_on=["method", "path", "query"],
    decode_compressed_response=True,
)


@requests_recorder_ro.use_cassette("osm_details.json")
def test_detailed_query():
    g = geocoder.osm("", postalcode="45326", street="Ellernstraße", method="details")
    assert g.postal == "45326"
    assert "ellern" in g.street.lower()
    assert g.has_data
