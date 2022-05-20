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
ottawa = (45.4215296, -75.6971930)


@requests_recorder_ro.use_cassette("osm_reverse.json")
def test_osm_reverse():
    g = geocoder.osm(ottawa, method="reverse")
    assert g.has_data
