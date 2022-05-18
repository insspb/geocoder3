import pytest
import vcr

import geocoder
from geocoder.api import options

requests_recorder_ro = vcr.VCR(
    serializer="json",
    cassette_library_dir="tests/cassettes/",
    filter_headers=["Authorization"],
    filter_query_parameters=["key"],
    record_mode="none",
    match_on=["method", "path", "query"],
    decode_compressed_response=True,
)


@requests_recorder_ro.use_cassette("api_py.json")
@pytest.mark.parametrize(
    "query, provider, method, expected_error_text",
    [
        (2, "osm", "geocode", "Query should be a string"),
        ("fake address", "no_provider", "geocode", "Invalid provider"),
        ("fake address", "osm", "fake_method", "Invalid method"),
    ],
    ids=[
        "Test for wrong query type",
        "Test for wrong provider",
        "Test for wrong method",
    ],
)
def test__get_results__on_wrong_arguments__return_expected_value_error(
    query,
    provider,
    method,
    expected_error_text,
):
    with pytest.raises(ValueError) as error:
        geocoder.get_results(query, provider, method)
        assert error.value == expected_error_text


@requests_recorder_ro.use_cassette("api_py.json")
def test__get_results__on_default_arguments__return_correct_value():
    result = geocoder.get_results("New York")
    assert result.ok
    assert result.latlng == [40.7127281, -74.0060152]


@requests_recorder_ro.use_cassette("api_py.json")
@pytest.mark.parametrize(
    "provider, method",
    [
        ("Osm", "Geocode"),
        (" osm ", " geocode "),
        (" OsM ", " GeocodE "),
    ],
)
def test__get_results__on_partly_correct_arguments__do_strip_and_lower(
    provider,
    method,
):
    result = geocoder.get_results("New York", provider=provider, method=method)
    assert result.ok
    assert result.latlng == [40.7127281, -74.0060152]


@pytest.mark.parametrize(
    "method_name, method_class",
    [y for x in options.values() for y in list(x.items())],
)
def test__options__correctly_configured(method_name, method_class):
    """This test responsible for checking correctness of options dict setup."""

    assert method_name == method_class._METHOD
    assert options[method_class._PROVIDER][method_class._METHOD] == method_class
