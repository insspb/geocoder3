import pytest
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
location = "Ottawa, Ontario"


@requests_recorder_ro.use_cassette("osm_geocode.json")
def test__osm__simple_query__return_correct_result():
    g = geocoder.osm(location)
    assert g.ok
    osm_count, fields_count = g.debug()[0]
    assert osm_count == 4
    assert fields_count == 24


@requests_recorder_ro.use_cassette("osm_geocode.json")
@pytest.mark.parametrize("max_results", [1, 5])
def test__osm__simple_query__respect_max_results_setting(max_results):
    g = geocoder.osm(location, maxRows=max_results)
    assert len(g) == max_results
