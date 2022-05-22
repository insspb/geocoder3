import pytest

import geocoder


@pytest.mark.parametrize(
    "location",
    (
        ("45.4215296, -75.6971931"),
        {"y": 45.4215296, "x": -75.6971931},
        {"lat": 45.4215296, "lng": -75.6971931},
        [45.4215296, -75.6971931],
    ),
    ids=(
        "Tuple input",
        "Dictionary input",
        "XY Dictionary input",
        "List input",
    ),
)
def test_location(location):
    g = geocoder.Location(location)
    assert g.ok
    assert g.latlng == [45.4215296, -75.6971931]
    assert g.latitude == 45.4215296
    assert g.longitude == -75.6971931
    assert g.xy == [-75.6971931, 45.4215296]
